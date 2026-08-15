import numpy as np
from src.preprocessing.color_math import ColorConverter
from src.optimization.de_solver import DifferentialEvolutionSolver


def test_rgb_to_lab_conversion():
    # Verify pure white conversion
    L, a, b = ColorConverter.rgb_to_lab(1.0, 1.0, 1.0)
    assert np.isclose(L, 100.0, atol=0.5)
    assert np.isclose(a, 0.0, atol=0.5)
    assert np.isclose(b, 0.0, atol=0.5)


def test_de_solver_ratios_sum():
    pigment_properties = {
        "base_red": {"K": [0.9, 0.05, 0.05], "S": [0.1, 0.9, 0.9]},
        "base_blue": {"K": [0.05, 0.05, 0.9], "S": [0.9, 0.9, 0.1]},
        "base_white": {"K": [0.01, 0.01, 0.01], "S": [0.99, 0.99, 0.99]},
    }
    solver = DifferentialEvolutionSolver(pigment_properties)
    bases = ["base_red", "base_blue", "base_white"]
    target_lab = (50.0, 10.0, -10.0)
    seed = [0.33, 0.33, 0.33]

    optimized = solver.optimize(target_lab, bases, seed)
    assert np.isclose(sum(optimized), 1.0, atol=1e-3)
    assert all(0.0 <= w <= 1.0 for w in optimized)
