# pyrefly: ignore [missing-import]
import optuna 
# pyrefly: ignore [missing-import]
import xgboost as xgb 
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np 

class HyperparameterOptimizer:
    def __init__(self, data_path: str):
        self.data_path = data_path

    def load_data(self):
        df = pd.read_csv(self.data_path)
        X = df[["mixed_L", "mixed_a", "mixed_b_coord"]].values
        Y = df[["ratio_red", "ratio_blue", "ratio_white", "ratio_yellow", "ratio_black"]].values
        return train_test_split(X, Y, test_size=0.2, random_state=42)

    def optimize_xgb(self, n_trials: int = 10) -> dict:
        X_train, X_test, Y_train, Y_test = self.load_data()

        def objective(trial):
            params = {
                "n_estimators": trial.suggest_int("n_estimators", 50, 200),
                "max_depth": trial.suggest_int("max_depth", 3, 9),
                "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.2),
                "random_state": 42
            }
            model = xgb.XGBRegressor(**params)
            model.fit(X_train, Y_train)
            preds = model.predict(X_test)
            return mean_squared_error(Y_test, preds)

        study = optuna.create_study(direction="minimize")
        study.optimize(objective, n_trials=n_trials)
        return study.best_params
