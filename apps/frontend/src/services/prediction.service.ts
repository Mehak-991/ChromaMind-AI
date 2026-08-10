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
      ratios: response.data.formulation.base_ratios.map((item: any) => ({
        baseId: item.id,
        ratio: item.ratio,
        weightGrams: item.weight_grams,
      })),
      deltaE: response.data.formulation.delta_e,
      confidenceScore: response.data.formulation.confidence_score,
      explanation: {
        shapValues: response.data.explanation.shap_values,
        summary: response.data.explanation.summary,
      },
    };
  },
};
