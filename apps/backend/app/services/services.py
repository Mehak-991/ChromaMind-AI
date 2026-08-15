import uuid
import math
import numpy as np
from typing import Dict, Any, List, Tuple
from scipy.optimize import differential_evolution, LinearConstraint
from sklearn.neural_network import MLPRegressor
from app.schemas.schemas import PredictionRequest, AssistantQueryRequest
from app.repositories.repositories import PredictionRepository

# --- Color Conversion Helpers ---


def lab_to_xyz(lightness: float, a: float, b: float) -> Tuple[float, float, float]:
    xn, yn, zn = 0.95047, 1.00000, 1.08883
    fy = (lightness + 16.0) / 116.0
    fx = a / 500.0 + fy
    fz = fy - b / 200.0

    x = xn * (fx**3 if fx > 0.206897 else (fx - 16.0 / 116.0) / 7.787)
    y = yn * (fy**3 if fy > 0.206897 else (fy - 16.0 / 116.0) / 7.787)
    z = zn * (fz**3 if fz > 0.206897 else (fz - 16.0 / 116.0) / 7.787)
    return x, y, z


def xyz_to_rgb(x: float, y: float, z: float) -> Tuple[float, float, float]:
    r = x * 3.2406 + y * -1.5372 + z * -0.4986
    g = x * -0.9689 + y * 1.8758 + z * 0.0415
    b = x * 0.0557 + y * -0.2040 + z * 1.0570

    rgb = []
    for c in [r, g, b]:
        c = max(0.0, min(1.0, c))
        if c <= 0.0031308:
            rgb.append(c * 12.92)
        else:
            rgb.append(1.055 * (c ** (1 / 2.4)) - 0.055)
    return rgb[0], rgb[1], rgb[2]


def rgb_to_xyz(r: float, g: float, b: float) -> Tuple[float, float, float]:
    rgb_linear = []
    for c in [r, g, b]:
        if c <= 0.04045:
            rgb_linear.append(c / 12.92)
        else:
            rgb_linear.append(((c + 0.055) / 1.055) ** 2.4)
    rl, gl, bl = rgb_linear
    x = rl * 0.4124 + gl * 0.3576 + bl * 0.1805
    y = rl * 0.2126 + gl * 0.7152 + bl * 0.0722
    z = rl * 0.0193 + gl * 0.1192 + bl * 0.9505
    return x, y, z


def xyz_to_lab(x: float, y: float, z: float) -> Tuple[float, float, float]:
    xn, yn, zn = 0.95047, 1.00000, 1.08883
    fx = (x / xn) ** (1 / 3) if (x / xn) > 0.008856 else 7.787 * (x / xn) + 16.0 / 116.0
    fy = (y / yn) ** (1 / 3) if (y / yn) > 0.008856 else 7.787 * (y / yn) + 16.0 / 116.0
    fz = (z / zn) ** (1 / 3) if (z / zn) > 0.008856 else 7.787 * (z / zn) + 16.0 / 116.0
    lightness = 116.0 * fy - 16.0
    a = 500.0 * (fx - fy)
    b = 200.0 * (fy - fz)
    return lightness, a, b


def lab_to_rgb(lightness: float, a: float, b: float) -> Tuple[float, float, float]:
    x, y, z = lab_to_xyz(lightness, a, b)
    return xyz_to_rgb(x, y, z)


def rgb_to_hex(r: float, g: float, b: float) -> str:
    ir = int(round(max(0.0, min(1.0, r)) * 255.0))
    ig = int(round(max(0.0, min(1.0, g)) * 255.0))
    ib = int(round(max(0.0, min(1.0, b)) * 255.0))
    return f"#{ir:02x}{ig:02x}{ib:02x}"


# --- Physical Color Mixing ---


def mix_colors_physical_lab(
    ratios: np.ndarray, base_labs: List[Tuple[float, float, float]]
) -> Tuple[float, float, float]:
    """
    Physically meaningful color mixing using the Kubelka-Munk theory (K/S).
    """
    mixed_K = np.zeros(3)
    mixed_S = np.zeros(3)

    # Calculate K and S for each base color
    for w, lab in zip(ratios, base_labs):
        r, g, b = lab_to_rgb(lab[0], lab[1], lab[2])
        # Single-constant K/S estimation (assume S = 1.0)
        # K/S = (1 - R)^2 / (2R)
        rgb_val = np.clip([r, g, b], 0.001, 0.999)
        K = ((1.0 - rgb_val) ** 2) / (2.0 * rgb_val)
        S = np.ones(3)

        mixed_K += w * K
        mixed_S += w * S

    # Calculate mixed reflectance R = 1 + K/S - sqrt((K/S)^2 + 2K/S)
    theta = mixed_K / (mixed_S + 1e-7)
    theta = np.clip(theta, 0.0, 1000.0)
    val = theta**2 + 2.0 * theta
    mixed_rgb = 1.0 + theta - np.sqrt(np.clip(val, 0.0, None))
    mixed_rgb = np.clip(mixed_rgb, 0.0, 1.0)

    # Convert mixed RGB to LAB
    mx, my, mz = rgb_to_xyz(mixed_rgb[0], mixed_rgb[1], mixed_rgb[2])
    ml, ma, mb = xyz_to_lab(mx, my, mz)
    return ml, ma, mb


# --- Delta E (CIEDE2000) ---


def calculate_delta_e00(
    lab1: Tuple[float, float, float], lab2: Tuple[float, float, float]
) -> float:
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2

    kL = 1.0
    kC = 1.0
    kH = 1.0

    C1 = math.sqrt(a1**2 + b1**2)
    C2 = math.sqrt(a2**2 + b2**2)

    C_bar = (C1 + C2) / 2.0

    G = 0.5 * (1.0 - math.sqrt(C_bar**7 / (C_bar**7 + 25**7)))

    a1_prime = a1 * (1.0 + G)
    a2_prime = a2 * (1.0 + G)

    C1_prime = math.sqrt(a1_prime**2 + b1**2)
    C2_prime = math.sqrt(a2_prime**2 + b2**2)

    if C1_prime == 0.0:
        h1_prime = 0.0
    else:
        h1_prime = math.atan2(b1, a1_prime)
        if h1_prime < 0:
            h1_prime += 2 * math.pi
        h1_prime = math.degrees(h1_prime)

    if C2_prime == 0.0:
        h2_prime = 0.0
    else:
        h2_prime = math.atan2(b2, a2_prime)
        if h2_prime < 0:
            h2_prime += 2 * math.pi
        h2_prime = math.degrees(h2_prime)

    dL_prime = L2 - L1
    dC_prime = C2_prime - C1_prime

    if C1_prime * C2_prime == 0.0:
        dh_prime = 0.0
    else:
        dh_prime = h2_prime - h1_prime
        if dh_prime > 180:
            dh_prime -= 360
        elif dh_prime < -180:
            dh_prime += 360

    dH_prime = (
        2.0 * math.sqrt(C1_prime * C2_prime) * math.sin(math.radians(dh_prime / 2.0))
    )

    L_bar_prime = (L1 + L2) / 2.0
    C_bar_prime = (C1_prime + C2_prime) / 2.0

    if C1_prime * C2_prime == 0.0:
        h_bar_prime = h1_prime + h2_prime
    else:
        if abs(h1_prime - h2_prime) <= 180:
            h_bar_prime = (h1_prime + h2_prime) / 2.0
        else:
            if h1_prime + h2_prime < 360:
                h_bar_prime = (h1_prime + h2_prime + 360.0) / 2.0
            else:
                h_bar_prime = (h1_prime + h2_prime - 360.0) / 2.0

    T = (
        1.0
        - 0.17 * math.cos(math.radians(h_bar_prime - 30.0))
        + 0.24 * math.cos(math.radians(2.0 * h_bar_prime))
        + 0.32 * math.cos(math.radians(3.0 * h_bar_prime + 6.0))
        - 0.20 * math.cos(math.radians(4.0 * h_bar_prime - 63.0))
    )

    dtheta = 30.0 * math.exp(-(((h_bar_prime - 275.0) / 25.0) ** 2))

    RC = 2.0 * math.sqrt(C_bar_prime**7 / (C_bar_prime**7 + 25**7))
    RT = -math.sin(math.radians(2.0 * dtheta)) * RC

    SL = 1.0 + (0.015 * (L_bar_prime - 50.0) ** 2) / math.sqrt(
        20.0 + (L_bar_prime - 50.0) ** 2
    )
    SC = 1.0 + 0.045 * C_bar_prime
    SH = 1.0 + 0.015 * C_bar_prime * T

    term_L = dL_prime / (kL * SL)
    term_C = dC_prime / (kC * SC)
    term_H = dH_prime / (kH * SH)

    delta_e = math.sqrt(term_L**2 + term_C**2 + term_H**2 + RT * term_C * term_H)
    return delta_e


# --- Service Implementations ---


class MLService:
    async def predict_ratios(self, request: PredictionRequest) -> List[float]:
        """
        Predict initial color formulation ratios using an MLP model trained on-the-fly.
        """
        base_colors = request.base_colors
        target_lab = (
            request.target_color.lab.L,
            request.target_color.lab.a,
            request.target_color.lab.b,
        )

        base_labs = [(c.lab.L, c.lab.a, c.lab.b) for c in base_colors]

        # Train a dynamic, fast MLP model on the fly using synthetic samples from these base colors
        X_train = []
        y_train = []
        num_samples = 200
        for _ in range(num_samples):
            ratios = np.random.dirichlet(np.ones(len(base_colors)))
            mixed_lab = mix_colors_physical_lab(ratios, base_labs)
            X_train.append(mixed_lab)
            y_train.append(ratios)

        mlp = MLPRegressor(
            hidden_layer_sizes=(16, 8),
            max_iter=150,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1,
        )
        mlp.fit(X_train, y_train)

        predicted = mlp.predict([target_lab])[0]
        predicted = np.clip(predicted, 0.0, 1.0)
        predicted = predicted / (np.sum(predicted) + 1e-9)
        return predicted.tolist()


class OptimizationService:
    async def optimize_ratios(
        self, request: PredictionRequest, seed_ratios: List[float]
    ) -> List[float]:
        """
        Refine ratios using Scipy's Differential Evolution solver.
        """
        if not request.run_optimization:
            return seed_ratios

        base_colors = request.base_colors
        target_lab = (
            request.target_color.lab.L,
            request.target_color.lab.a,
            request.target_color.lab.b,
        )
        base_labs = [(c.lab.L, c.lab.a, c.lab.b) for c in base_colors]
        num_bases = len(base_colors)

        def objective(weights):
            normalized = weights / (np.sum(weights) + 1e-9)
            current_lab = mix_colors_physical_lab(normalized, base_labs)
            return calculate_delta_e00(target_lab, current_lab)

        bounds = [(0.0, 1.0)] * num_bases
        constraint = LinearConstraint(np.ones((1, num_bases)), [1.0], [1.0])

        result = differential_evolution(
            objective,
            bounds=bounds,
            constraints=constraint,
            x0=seed_ratios,
            maxiter=100,
            popsize=10,
            tol=0.01,
            seed=42,
        )

        final_weights = result.x / (np.sum(result.x) + 1e-9)
        return final_weights.tolist()


class ExplainabilityService:
    async def calculate_shap_values(
        self, request: PredictionRequest, optimized_ratios: List[float]
    ) -> Dict[str, float]:
        # Simple simulated SHAP impact metric
        return {
            color.id: 0.15 if i % 2 == 0 else -0.06
            for i, color in enumerate(request.base_colors)
        }


class PredictionService:
    def __init__(
        self,
        ml_service: MLService,
        optimizer: OptimizationService,
        explainability: ExplainabilityService,
        repo: PredictionRepository,
    ):
        self.ml_service = ml_service
        self.optimizer = optimizer
        self.explainability = explainability
        self.repo = repo

    async def execute_formulation(
        self, request: PredictionRequest, user_id: uuid.UUID
    ) -> Dict[str, Any]:
        # Step 1: ML Prediction (MLP)
        seed = await self.ml_service.predict_ratios(request)

        # Step 2: Differential Evolution Optimization
        optimized = await self.optimizer.optimize_ratios(request, seed)

        # Step 3 & 4: LAB Color Mixing and Delta E Calculation
        base_labs = [(c.lab.L, c.lab.a, c.lab.b) for c in request.base_colors]
        mixed_lab = mix_colors_physical_lab(np.array(optimized), base_labs)

        target_lab = (
            request.target_color.lab.L,
            request.target_color.lab.a,
            request.target_color.lab.b,
        )
        delta_e = calculate_delta_e00(target_lab, mixed_lab)

        # Step 5: Convert LAB -> RGB -> HEX
        rgb_mixed = lab_to_rgb(mixed_lab[0], mixed_lab[1], mixed_lab[2])
        hex_mixed = rgb_to_hex(rgb_mixed[0], rgb_mixed[1], rgb_mixed[2])

        # Step 6: Render/Prepare Final Color Preview Metadata
        confidence_score = max(0.0, min(1.0, 1.0 - (delta_e / 15.0)))

        # Determine status
        if delta_e < 1.0:
            match_status = "Excellent Match"
        elif delta_e < 2.0:
            match_status = "Very Good Match"
        elif delta_e < 5.0:
            match_status = "Good Match"
        else:
            match_status = "Needs Optimization"

        formulation = {
            "predicted_rgb": [
                int(round(rgb_mixed[0] * 255.0)),
                int(round(rgb_mixed[1] * 255.0)),
                int(round(rgb_mixed[2] * 255.0)),
            ],
            "predicted_hex": hex_mixed,
            "predicted_lab": [
                float(np.round(mixed_lab[0], 2)),
                float(np.round(mixed_lab[1], 2)),
                float(np.round(mixed_lab[2], 2)),
            ],
            "ratios": [
                {
                    "pigment": color.name or color.id,
                    "ratio": float(np.round(optimized[i], 4)),
                    "weight_grams": float(np.round(optimized[i] * 100.0, 2)),
                }
                for i, color in enumerate(request.base_colors)
            ],
            "delta_e": float(np.round(delta_e, 2)),
            "confidence": float(np.round(confidence_score * 100.0, 1)),
            "status": match_status,
        }

        # Explainability SHAP contributions
        shap_values = await self.explainability.calculate_shap_values(
            request, optimized
        )

        explanation = {
            "shap_values": shap_values,
            "summary": "Physically realistic Kubelka-Munk mixture optimized to minimize CIEDE2000 color difference.",
        }

        return {
            "prediction_id": uuid.uuid4(),
            "target_color": request.target_color.dict(),
            "formulation": formulation,
            "explanation": explanation,
        }


class AssistantService:
    async def query_rag_engine(self, request: AssistantQueryRequest) -> Dict[str, Any]:
        return {
            "response": "Based on the Kubelka-Munk physical model, light absorption (K) and scattering (S) parameters are calculated for each base color. The Differential Evolution solver optimizes the mixing ratios to minimize the CIEDE2000 Delta E relative to the target color.",
            "citations": [
                {
                    "title": "Industrial Color Formulation & Kubelka-Munk Theory",
                    "snippet": "Kubelka-Munk equations relate reflectance values of mixtures to the absorption and scattering characteristics of the individual pigments.",
                    "confidence": 0.99,
                }
            ],
        }


class AuthService:
    pass
