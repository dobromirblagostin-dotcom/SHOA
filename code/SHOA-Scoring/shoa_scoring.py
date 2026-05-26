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
