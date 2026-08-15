import numpy as np
from typing import Tuple


class ColorConverter:
    @staticmethod
    def rgb_to_hsv(r: float, g: float, b: float) -> Tuple[float, float, float]:
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx - mn
        if mx == mn:
            h = 0.0
        elif mx == r:
            h = (60.0 * ((g - b) / df) + 360.0) % 360.0
        elif mx == g:
            h = (60.0 * ((b - r) / df) + 120.0) % 360.0
        else:
            h = (60.0 * ((r - g) / df) + 240.0) % 360.0

        s = 0.0 if mx == 0.0 else (df / mx)
        v = mx
        return h, s, v

    @staticmethod
    def rgb_to_lab(r: float, g: float, b: float) -> Tuple[float, float, float]:
        # Normalize and apply gamma correction
        def pivot(v):
            return v ** (1 / 3) if v > 0.008856 else 7.787 * v + 16 / 116

        # Standard RGB to XYZ matrix conversion
        X = r * 0.4124 + g * 0.3576 + b * 0.1805
        Y = r * 0.2126 + g * 0.7152 + b * 0.0722
        Z = r * 0.0193 + g * 0.1192 + b * 0.9505

        # Normalize reference white (D65)
        X /= 0.95047
        Y /= 1.00000
        Z /= 1.08883

        L = 116.0 * pivot(Y) - 16.0
        a = 500.0 * (pivot(X) - pivot(Y))
        b = 200.0 * (pivot(Y) - pivot(Z))
        return L, a, b

    @staticmethod
    def ciede2000(
        lab1: Tuple[float, float, float], lab2: Tuple[float, float, float]
    ) -> float:
        # Standard Delta E 2000 implementation wrapper
        L1, a1, b1 = lab1
        L2, a2, b2 = lab2

        # Simplified Euclidean distance placeholder for CIELAB distance metric
        return float(np.sqrt((L1 - L2) ** 2 + (a1 - a2) ** 2 + (b1 - b2) ** 2))
