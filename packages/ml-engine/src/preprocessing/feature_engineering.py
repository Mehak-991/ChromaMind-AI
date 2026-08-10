import pandas as pd
import numpy as np
from typing import List

class FeatureEngineer:
    def __init__(self, base_cols: List[str]):
        self.base_cols = base_cols

    def extract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        processed_df = df.copy()
        
        # Calculate stats across base ratios
        ratio_cols = [f"ratio_{b}" for b in self.base_cols]
        processed_df["ratio_mean"] = df[ratio_cols].mean(axis=1)
        processed_df["ratio_std"] = df[ratio_cols].std(axis=1)
        processed_df["num_active_colors"] = (df[ratio_cols] > 0.01).sum(axis=1)
        
        # Calculate mixed color magnitude
        processed_df["mixed_magnitude"] = np.sqrt(
            df["mixed_L"]**2 + df["mixed_a"]**2 + df["mixed_b_coord"]**2
        )
        return processed_df
