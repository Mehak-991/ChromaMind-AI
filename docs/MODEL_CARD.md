# Model Card - ChromaMind AI MLP

This model card provides details on the core Neural Network formulation model deployed within the ChromaMind AI pipeline.

---

## 1. Model Details
- **Developer**: ChromaMind AI Corp
- **Model Type**: Deep Multi-Layer Perceptron (MLP) Regressor
- **Architecture**: 4 fully connected layers with ReLU activations and a Softmax output layer to guarantee that ratio weights sum to exactly 1.0.
- **Inputs**: Target $L^*a^*b^*$ coordinate vector (size 3) + available base pigment coordinates (size $8 \times 3$).
- **Outputs**: Allocation percentages mapping to selected bases (size 8).

---

## 2. Intended Use
- **Primary Use**: Industrial coatings, paint mixing, and print ink formulation prediction.
- **Out of Scope**: High-precision spectrophotometer calibration or rendering of color on uncalibrated hardware monitors.

---

## 3. Training & Evaluation
- **Dataset**: 100,000 synthetic formulations generated using the Kubelka-Munk reflectance model.
- **Epochs / Batch**: 50 Epochs, batch size of 64.
- **Tuning**: Optuna trial optimizations mapping learning rates between 0.001 and 0.01.
- **Evaluation Metric**: Mean Squared Error (MSE) on allocation ratios and Delta E ($\Delta E_{00}$) on resulting mixtures.

---

## 4. Limitations & Bias
- Model behaves linearly when mixing pigments. Physical anomalies like chemical reactions, binder shifts, or wet-to-dry color shifts are not captured by the synthetic reflectance model and must be corrected using empirical database feedback.
