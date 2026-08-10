import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
# pyrefly: ignore [missing-import]
import xgboost as xgb  
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np 
import joblib 
from typing import Tuple

class PyTorchMLP(nn.Module):
    def __init__(self, input_dim: int, output_dim: int):
        super(PyTorchMLP, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, output_dim),
            nn.Softmax(dim=-1)  # Enforce sum = 1.0 constraint
        )

    def forward(self, x):
        return self.network(x)


class ModelTrainer:
    def __init__(self, data_path: str, model_dir: str = "./saved_models"):
        self.data_path = data_path
        self.model_dir = model_dir
        os.makedirs(self.model_dir, exist_ok=True)

    def load_data(self) -> Tuple[np.ndarray, np.ndarray]:
        df = pd.read_csv(self.data_path)
        X = df[["mixed_L", "mixed_a", "mixed_b_coord"]].values
        # Targets are base ratios
        Y = df[["ratio_red", "ratio_blue", "ratio_white", "ratio_yellow", "ratio_black"]].values
        return X, Y

    def train_xgb(self, X_train, Y_train, X_test, Y_test):
        model = xgb.XGBRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42
        )
        # Multi-output regression
        model.fit(X_train, Y_train)
        preds = model.predict(X_test)
        mse = mean_squared_error(Y_test, preds)
        
        # Save model
        joblib.dump(model, os.path.join(self.model_dir, "xgb_model.joblib"))
        print(f"XGBoost Model Trained. Test MSE: {mse:.6f}")

    def train_pytorch(self, X_train, Y_train, X_test, Y_test, epochs: int = 10):
        # Convert to tensors
        train_dataset = TensorDataset(
            torch.tensor(X_train, dtype=torch.float32),
            torch.tensor(Y_train, dtype=torch.float32)
        )
        loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

        model = PyTorchMLP(input_dim=3, output_dim=5)
        optimizer = optim.Adam(model.parameters(), lr=0.005)
        criterion = nn.MSELoss()

        model.train()
        for epoch in range(epochs):
            for batch_x, batch_y in loader:
                optimizer.zero_grad()
                out = model(batch_x)
                loss = criterion(out, batch_y)
                loss.backward()
                optimizer.step()

        # Evaluate
        model.eval()
        with torch.no_grad():
            test_x = torch.tensor(X_test, dtype=torch.float32)
            test_y = torch.tensor(Y_test, dtype=torch.float32)
            preds = model(test_x)
            mse = criterion(preds, test_y).item()

        # Save model
        torch.save(model.state_dict(), os.path.join(self.model_dir, "mlp_model.pt"))
        print(f"PyTorch MLP Trained. Test MSE: {mse:.6f}")

    def execute_all(self):
        X, Y = self.load_data()
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        self.train_xgb(X_train, Y_train, X_test, Y_test)
        self.train_pytorch(X_train, Y_train, X_test, Y_test)
