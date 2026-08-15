from google.protobuf.internal.well_known_types import Any
import os
import numpy as np
import pandas as pd
from typing import Tuple, List, Dict


class SyntheticDatasetGenerator:
    def __init__(self, output_dir: str = "./datasets"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        # Mock base pigments: absorption (K) and scattering (S) approximations per RGB channel
        self.pigment_properties = {
            "red": {"K": [0.9, 0.05, 0.05], "S": [0.1, 0.9, 0.9]},
            "blue": {"K": [0.05, 0.05, 0.9], "S": [0.9, 0.9, 0.1]},
            "white": {"K": [0.01, 0.01, 0.01], "S": [0.99, 0.99, 0.99]},
            "yellow": {"K": [0.1, 0.8, 0.05], "S": [0.9, 0.1, 0.9]},
            "black": {"K": [0.99, 0.99, 0.99], "S": [0.01, 0.01, 0.01]},
        }

    def simulate_mixture(
        self, ratios: List[float], bases: List[str]
    ) -> Tuple[List[float], List[float]]:
        # Simplified Kubelka-Munk mixing model: R = S / (K + S) approximation
        mixed_K = np.zeros(3)
        mixed_S = np.zeros(3)
        for r, base in zip(ratios, bases):
            mixed_K += r * np.array(self.pigment_properties[base]["K"])
            mixed_S += r * np.array(self.pigment_properties[base]["S"])

        # Calculate reflectance approximation
        reflectance = mixed_S / (mixed_K + mixed_S + 1e-5)
        # Clip to valid RGB ranges
        rgb = np.clip(reflectance, 0.0, 1.0)

        # Approximate LAB conversion from RGB
        L = 116.0 * (rgb[1] ** (1 / 3)) - 16.0 if rgb[1] > 0.008856 else 903.3 * rgb[1]
        a = 500.0 * ((rgb[0] ** (1 / 3)) - (rgb[1] ** (1 / 3)))
        b = 200.0 * ((rgb[1] ** (1 / 3)) - (rgb[2] ** (1 / 3)))

        return list(rgb), [L, a, b]

    def generate_samples(self, count: int = 100000) -> pd.DataFrame:
        data = []
        bases = list(self.pigment_properties.keys())

        for i in range(count):
            # Generate random ratios summing to 1.0
            raw_ratios = np.random.dirichlet(np.ones(len(bases)))
            rgb, lab = self.simulate_mixture(raw_ratios.tolist(), bases)

            row = {
                "sample_id": f"sample_{i}",
                "ratio_red": raw_ratios[0],
                "ratio_blue": raw_ratios[1],
                "ratio_white": raw_ratios[2],
                "ratio_yellow": raw_ratios[3],
                "ratio_black": raw_ratios[4],
                "mixed_r": rgb[0],
                "mixed_g": rgb[1],
                "mixed_b": rgb[2],
                "mixed_L": lab[0],
                "mixed_a": lab[1],
                "mixed_b_coord": lab[2],
            }
            data.append(row)

        df = pd.DataFrame(data)
        output_path = os.path.join(self.output_dir, "synthetic_dataset.csv")
        df.to_csv(output_path, index=False)
        return df

    def validate_dataset(self, df: pd.DataFrame) -> Dict[str, Any]:
        # Validate data checks
        report = {
            "total_rows": len(df),
            "missing_values": int(df.isnull().sum().sum()),
            "outliers_rgb": int(((df["mixed_r"] < 0) | (df["mixed_r"] > 1)).sum()),
            "ratio_sum_check": float(
                np.abs(
                    df[[f"ratio_{b}" for b in self.pigment_properties.keys()]].sum(
                        axis=1
                    )
                    - 1.0
                ).max()
            ),
        }
        return report


if __name__ == "__main__":
    gen = SyntheticDatasetGenerator()
    df = gen.generate_samples(100)
    print("Generation complete. Validation:", gen.validate_dataset(df))
