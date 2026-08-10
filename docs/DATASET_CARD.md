# Dataset Card - ChromaMind AI Synthetic Reflectance Dataset

This dataset card describes the generation, format, and structure of the color mixture training data.

---

## 1. Dataset Description
- **Creator**: ChromaMind AI Synthetic Generator pipeline.
- **Size**: 100,000 samples.
- **Format**: Comma-Separated Values (CSV).
- **Features**:
  - `ratio_*`: Target weight ratios for red, blue, white, yellow, and black bases.
  - `mixed_r`, `mixed_g`, `mixed_b`: Resulting simulated sRGB value.
  - `mixed_L`, `mixed_a`, `mixed_b_coord`: Resulting simulated CIELAB coordinate values.

---

## 2. Generation Process
- Data is simulated using the Kubelka-Munk equation:
  $$\frac{K}{S} = \frac{(1 - R)^2}{2R}$$
- Ratios are drawn using a Dirichlet distribution to guarantee bounds ($[0.0, 1.0]$) and sum-to-one constraints.

---

## 3. Data Validation & Profiling
- **Validation check**: Maximum ratio sum error $\le 10^{-5}$.
- **Outliers**: Coordinates are bounded to sRGB $[0, 1]$ and CIELAB $L^* \in [0, 100]$.
