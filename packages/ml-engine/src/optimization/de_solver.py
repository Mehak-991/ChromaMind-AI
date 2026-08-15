import numpy as np
from scipy.optimize import differential_evolution, LinearConstraint
from typing import List, Tuple


class DifferentialEvolutionSolver:
    def __init__(self, pigment_properties: dict):
        self.pigment_properties = pigment_properties

    def mix_colors_physical(
        self, weights: np.ndarray, bases: List[str]
    ) -> Tuple[float, float, float]:
        # K/S approximation model
        mixed_K = np.zeros(3)
        mixed_S = np.zeros(3)
        for w, base in zip(weights, bases):
            mixed_K += w * np.array(self.pigment_properties[base]["K"])
            mixed_S += w * np.array(self.pigment_properties[base]["S"])

        reflectance = mixed_S / (mixed_K + mixed_S + 1e-5)
        rgb = np.clip(reflectance, 0.0, 1.0)

        # LAB approximation coordinates
        L = 116.0 * (rgb[1] ** (1 / 3)) - 16.0 if rgb[1] > 0.008856 else 903.3 * rgb[1]
        a = 500.0 * ((rgb[0] ** (1 / 3)) - (rgb[1] ** (1 / 3)))
        b = 200.0 * ((rgb[1] ** (1 / 3)) - (rgb[2] ** (1 / 3)))
        return float(L), float(a), float(b)

    def optimize(
        self,
        target_lab: Tuple[float, float, float],
        bases: List[str],
        seed_weights: List[float],
    ) -> List[float]:
        num_bases = len(bases)

        # Define objective function: minimizing Euclidean distance in LAB
        def objective(weights):
            normalized = weights / np.sum(weights)
            current_lab = self.mix_colors_physical(normalized, bases)
            return np.sqrt(
                (target_lab[0] - current_lab[0]) ** 2
                + (target_lab[1] - current_lab[1]) ** 2
                + (target_lab[2] - current_lab[2]) ** 2
            )

        # Bounds: ratios between 0.0 and 1.0
        bounds = [(0.0, 1.0)] * num_bases

        # Constraint: sum(weights) = 1.0
        # A @ x = sum(weights). Matrix A is all ones.
        constraint = LinearConstraint(np.ones((1, num_bases)), [1.0], [1.0])

        # Execute solver
        result = differential_evolution(
            objective,
            bounds=bounds,
            constraints=constraint,
            x0=seed_weights,  # Use neural net prediction as initial seed
            maxiter=500,
            popsize=15,
            tol=0.01,
        )

        final_weights = result.x / np.sum(result.x)
        return final_weights.tolist()
