```python
"""
ME‑deconvolution for SHOA‑Chrono: reconstructs quantum field Ψ_C(r)
from experimental coincidence counts P_exp.
Author: Konstantin Fedotov
Reference: SHOA‑Chrono v2 (DOI: 10.5281/zenodo.20350345)
"""

import numpy as np
from scipy.optimize import minimize
from typing import Dict, Tuple, List

def me_deconvolution(P_exp: Dict[Tuple[int, int], float],
                     library_ME: List[np.ndarray],
                     detector_vectors: Dict[int, np.ndarray],
                     defect_positions: np.ndarray,
                     Psi_thermal: float = 1.0,
                     N_photons: int = 10,
                     lambda_reg: float = 0.1,
                     Z: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
    """
    Maximum‑Entropy deconvolution for SHOA‑Chrono protocol.

    Parameters
    ----------
    P_exp : dict
        Experimental normalized coincidence counts. Keys = (detector_i, detector_j).
    library_ME : list of 3D arrays
        Basis patterns φ_k(r) (e.g., Hermite‑Gauss modes).
    detector_vectors : dict
        Momentum vectors for each detector: {detector_id: np.ndarray(2,)}.
    defect_positions : np.ndarray
        Positions of quantum dots / defects, shape (N_defects, 2).
    Psi_thermal : float, optional
        Thermal field amplitude for tanh saturation.
    N_photons : int, optional
        Number of Grape photons (not used in current version, kept for future).
    lambda_reg : float, optional
        Regularisation strength (entropy term).
    Z : float, optional
        Partition function normalisation (estimated from data).

    Returns
    -------
    c_opt : np.ndarray
        Optimal expansion coefficients for each basis mode.
    Psi_reconstructed : np.ndarray
        Reconstructed field Ψ_C(r), same shape as library_ME[0].
    """
    K = len(library_ME)
    # Work on copies to avoid modifying original data
    lib_normed = [np.copy(mode) for mode in library_ME]
    for k in range(K):
        norm = np.sqrt(np.sum(lib_normed[k]**2))
        if norm > 0:
            lib_normed[k] /= norm

    # Number of defect positions (for phase factor)
    N_def = defect_positions.shape[0]

    def compute_P_theory(c: np.ndarray) -> Dict[Tuple[int, int], float]:
        # Reconstructed field
        Psi_model = np.sum([c[k] * lib_normed[k] for k in range(K)], axis=0)
        # Non‑linear saturation (analogy with neuron firing)
        w = np.tanh(Psi_model / Psi_thermal)
        P_theory = {}
        for (i, j) in P_exp.keys():
            q_i = detector_vectors[i]
            q_j = detector_vectors[j]
            # Phase factor for each defect and sum over all defects
            phase = np.exp(1j * (q_i + q_j).dot(defect_positions.T))  # shape (N_def,)
            amplitude = np.abs(np.sum(w * phase))**2
            P_theory[(i, j)] = amplitude / Z
        return P_theory

    def total_loss(c: np.ndarray) -> float:
        P_theory = compute_P_theory(c)
        chi2 = 0.0
        for pair in P_exp:
            chi2 += (P_exp[pair] - P_theory[pair])**2
        # Entropy regularisation using coefficients squared (energy)
        entropy = -np.sum((c**2) * np.log(c**2 + 1e-12))
        return chi2 + lambda_reg * entropy

    # Initial guess: zero coefficients
    c0 = np.zeros(K)
    # Bounds: each coefficient between -10 and 10
    bounds = [(-10.0, 10.0) for _ in range(K)]

    result = minimize(total_loss, c0, method='L-BFGS-B', bounds=bounds)
    c_opt = result.x
    Psi_reconstructed = np.sum([c_opt[k] * lib_normed[k] for k in range(K)], axis=0)

    return c_opt, Psi_reconstructed


# -------------------- Example (synthetic) --------------------
if __name__ == "__main__":
    # Create a dummy library: 3 modes, each 10x10 grid
    K = 3
    grid_size = 10
    lib = []
    for k in range(K):
        mode = np.random.randn(grid_size, grid_size)
        lib.append(mode)

    # Dummy detector vectors (2 detectors)
    det_vectors = {0: np.array([1.0, 0.0]), 1: np.array([0.0, 1.0])}
    # Dummy defect positions (10 points)
    r_defects = np.random.randn(10, 2)

    # Simulated experimental data (only one pair for test)
    P_exp_dummy = {(0,1): 0.75}

    c_opt, Psi_recon = me_deconvolution(P_exp_dummy, lib, det_vectors, r_defects,
                                        Psi_thermal=1.0, lambda_reg=0.01)

    print("Optimised coefficients:", c_opt)
    print("Reconstructed field shape:", Psi_recon.shape)
