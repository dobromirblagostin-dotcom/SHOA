```python
import numpy as np

class SHOAScoringModel:
    """
    SHOA-Scoring prototype: evaluates business "anti-fragility" using 10 sensors.
    """
    def __init__(self):
        self.thresholds = {
            'current_liquidity': 2.0, 'debt_to_ebitda': 3.0,
            'revenue_growth': 15.0, 'operating_cash_flow': 0.0,
            'nps_score': 50.0, 'asset_renewal': 30.0,
            'supplier_diversity': 0.7, 'loyalty_rate': 0.8,
            'safety_margin': 0.3, 'adaptability_index': 0.7
        }
        self.weights = {
            'current_liquidity': 0.10, 'debt_to_ebitda': 0.12,
            'revenue_growth': 0.12, 'operating_cash_flow': 0.12,
            'nps_score': 0.08, 'asset_renewal': 0.10,
            'supplier_diversity': 0.08, 'loyalty_rate': 0.10,
            'safety_margin': 0.10, 'adaptability_index': 0.08
        }

    def _evaluate_sensor(self, name, value):
        if name in ['current_liquidity', 'revenue_growth', 'nps_score',
                     'asset_renewal', 'supplier_diversity', 'loyalty_rate',
                     'safety_margin', 'adaptability_index']:
            return min(1.0, value / self.thresholds[name])
        else:
            return min(1.0, self.thresholds[name] / value)

    def calculate_shoa_score(self, metrics):
        if len(metrics) != 10:
            raise ValueError("Exactly 10 metrics are required")
        sensor_scores = {s: self._evaluate_sensor(s, metrics[s]) for s in metrics}
        weighted_score = sum(sensor_scores[s] * self.weights[s] for s in sensor_scores)
        failing_sensors = sum(1 for s in sensor_scores.values() if s < 0.5)
        emergent_penalty = -0.15 if failing_sensors >= 3 else (-0.05 if failing_sensors >= 1 else 0.0)
        final_score = max(0.0, min(1.0, weighted_score + emergent_penalty))
        status = self._get_status(final_score)
        return final_score, status, sensor_scores

    def _get_status(self, score):
        if score >= 0.9: return "SHOA-resilient (quantum immunity)"
        elif 0.7 <= score < 0.9: return "Conditionally resilient (monitoring required)"
        elif 0.5 <= score < 0.7: return "Vulnerable (cascading failure risk)"
        else: return "Critical (self-healing impossible)"

# --- Test drive ---
if __name__ == "__main__":
    model = SHOAScoringModel()
    test_company = {
        'current_liquidity': 2.5, 'debt_to_ebitda': 1.5,
        'revenue_growth': 25.0, 'operating_cash_flow': 500000,
        'nps_score': 65.0, 'asset_renewal': 35.0,
        'supplier_diversity': 0.9, 'loyalty_rate': 0.85,
        'safety_margin': 0.4, 'adaptability_index': 0.8
    }
    score, status, _ = model.calculate_shoa_score(test_company)
    print f"SHOA-Score: {score:.3f} | Status: {status}"
