import apiClient from './apiClient';
import type { FormulationResult } from '../store/useColorStore';

export interface PredictPayload {
  target_color: {
    hex: string;
    lab: { L: number; a: number; b: number };
  };
  base_colors: Array<{
    id: string;
    hex: string;
    lab: { L: number; a: number; b: number };
  }>;
  run_optimization?: boolean;
}

export const predictionService = {
  async predict(payload: PredictPayload): Promise<FormulationResult> {
    const response = await apiClient.post('/formulator/predict', payload);
    return {
      predictionId: response.data.prediction_id,
      ratios: response.data.formulation.ratios.map((item: any) => ({
        pigment: item.pigment,
        ratio: item.ratio,
        weightGrams: item.weight_grams,
      })),
      deltaE: response.data.formulation.delta_e,
      confidenceScore: response.data.formulation.confidence,
      predictedRgb: response.data.formulation.predicted_rgb,
      predictedHex: response.data.formulation.predicted_hex,
      predictedLab: response.data.formulation.predicted_lab,
      status: response.data.formulation.status,
      explanation: {
        shapValues: response.data.explanation.shap_values,
        summary: response.data.explanation.summary,
      },
    };
  },
};
