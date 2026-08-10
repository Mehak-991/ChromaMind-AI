import os
import json
from typing import Dict, Any

class ModelRegistry:
    def __init__(self, registry_dir: str = "./model_registry"):
        self.registry_dir = registry_dir
        os.makedirs(self.registry_dir, exist_ok=True)

    def register_model(
        self,
        model_name: str,
        version: str,
        metrics: Dict[str, float],
        hyperparameters: Dict[str, Any]
    ) -> str:
        metadata = {
            "model_name": model_name,
            "version": version,
            "metrics": metrics,
            "hyperparameters": hyperparameters,
            "registered_at": "2026-08-07T02:50:00Z"
        }
        
        output_file = os.path.join(self.registry_dir, f"{model_name}_v{version}.json")
        with open(output_file, "w") as f:
            json.dump(metadata, f, indent=4)
        
        # MLflow mock registration log
        print(f"Model {model_name} v{version} registered in MLflow registry.")
        return output_file
