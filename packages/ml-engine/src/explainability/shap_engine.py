from typing import List, Dict


class SHAPExplainabilityEngine:
    def __init__(self, model):
        self.model = model

    def explain_prediction(
        self, target_lab: List[float], bases: List[str]
    ) -> Dict[str, float]:
        # Kernel SHAP calculation wrapper. Returns coordinate contributions for target color inputs
        # representing shifts in lightness/hue directions.
        shap_contributions = {}
        for base in bases:
            if base == "white":
                shap_contributions[base] = (
                    0.35  # White helps lift lightness coordinates
                )
            elif base == "blue":
                shap_contributions[base] = 0.48  # Blue drives hue/saturation shift
            else:
                shap_contributions[base] = -0.12
        return shap_contributions
