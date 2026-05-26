```python
"""
SHOA-Scoring: Business anti‑fragility model based on quantum emergence.
Author: Konstantin Fedotov
Reference: SHOA-Scoring v2 (DOI: 10.5281/zenodo.20362727)
"""

import numpy as np
from typing import Dict, Tuple, Optional

class SHOAScoringModel:
    """
    Evaluates a company's resilience using 10 hierarchical sensors.
    Implements weighted scoring + emergent penalty (Spiked Voting).
    """

    def __init__(self, custom_thresholds: Optional[Dict[str, float]] = None,
                 custom_weights: Optional[Dict[str, float]] = None):
        # Default thresholds (higher is better for all except debt/ebitda)
        self.thresholds = {
            'current_liquidity': 2.0,      # >=2.0 → 1.0
            'debt_to_ebitda': 3.0,         # <=3.0 → 1.0
            'revenue_growth': 15.0,        # percent
            'operating_cash_flow': 0.0,    # >=0 → 1.0
            'nps_score': 50.0,
            'asset_renewal': 30.0,         # percent
            'supplier_diversity': 0.7,     # 0..1
            'loyalty_rate': 0.8,
            'safety_margin': 0.3,
            'adaptability_index': 0.7
        }
        self.weights = {
            'current_liquidity': 0.10,
            'debt_to_ebitda': 0.12,
            'revenue_growth': 0.12,
            'operating_cash_flow': 0.12,
            'nps_score': 0.08,
            'asset_renewal': 0.10,
            'supplier_diversity': 0.08,
            'loyalty_rate': 0.10,
            'safety_margin': 0.10,
            'adaptability_index': 0.08
        }

        if custom_thresholds:
            self.thresholds.update(custom_thresholds)
        if custom_weights:
            self.weights.update(custom_weights)

    def _evaluate_sensor(self, name: str, value: float) -> float:
        """Normalize sensor value to [0,1]. Lower‑is‑better for debt/ebitda."""
        if name in ['current_liquidity', 'revenue_growth', 'nps_score',
                    'asset_renewal', 'supplier_diversity', 'loyalty_rate',
                    'safety_margin', 'adaptability_index']:
            return min(1.0, value / self.thresholds[name])
        else:  # debt_to_ebitda, operating_cash_flow (flow: negative = bad)
            if name == 'operating_cash_flow':
                return 1.0 if value >= 0 else 0.0
            return min(1.0, self.thresholds[name] / value)

    def calculate_shoa_score(self, metrics: Dict[str, float]) -> Tuple[float, str, Dict[str, float]]:
        """
        Calculate SHOA score and resilience status.
        Returns: (final_score, status_text, sensor_scores)
        """
        if set(metrics.keys()) != set(self.thresholds.keys()):
            raise ValueError(f"Need exactly these keys: {list(self.thresholds.keys())}")

        sensor_scores = {s: self._evaluate_sensor(s, metrics[s]) for s in metrics}
        weighted = sum(sensor_scores[s] * self.weights[s] for s in sensor_scores)

        failing = sum(1 for v in sensor_scores.values() if v < 0.5)
        if failing >= 3:
            penalty = -0.15
        elif failing >= 1:
            penalty = -0.05
        else:
            penalty = 0.0

        final = np.clip(weighted + penalty, 0.0, 1.0)
        status = self._get_status(final)
        return final, status, sensor_scores

    @staticmethod
    def _get_status(score: float) -> str:
        if score >= 0.9:
            return "SHOA-resilient (quantum immunity)"
        if score >= 0.7:
            return "Conditionally resilient (monitoring required)"
        if score >= 0.5:
            return "Vulnerable (cascading failure risk)"
        return "Critical (self-healing impossible)"


if __name__ == "__main__":
    model = SHOAScoringModel()

    # Example: Tesla (2025) – healthy
    tesla = {
        'current_liquidity': 2.5, 'debt_to_ebitda': 1.5,
        'revenue_growth': 25.0, 'operating_cash_flow': 500000,
        'nps_score': 65.0, 'asset_renewal': 35.0,
        'supplier_diversity': 0.9, 'loyalty_rate': 0.85,
        'safety_margin': 0.4, 'adaptability_index': 0.8
    }
    score, status, _ = model.calculate_shoa_score(tesla)
    print(f"Tesla → SHOA-Score: {score:.3f} | {status}")

    # Example: Hertz (2024, before bankruptcy) – cascading failure
    hertz = {
        'current_liquidity': 0.8, 'debt_to_ebitda': 8.0,
        'revenue_growth': -15.0, 'operating_cash_flow': -200000,
        'nps_score': 20.0, 'asset_renewal': 5.0,
        'supplier_diversity': 0.2, 'loyalty_rate': 0.3,
        'safety_margin': 0.05, 'adaptability_index': 0.2
    }
    score, status, _ = model.calculate_shoa_score(hertz)
    print(f"Hertz   → SHOA-Score: {score:.3f} | {status}")
