import { create } from 'zustand';

export interface Color {
  id: string;
  hex: string;
  lab: [number, number, number];
  name?: string;
}

export interface FormulationResult {
  predictionId: string;
  ratios: Array<{ pigment: string; ratio: number; weightGrams: number }>;
  deltaE: number;
  confidenceScore: number;
  predictedRgb: [number, number, number];
  predictedHex: string;
  predictedLab: [number, number, number];
  status: string;
  explanation: {
    shapValues: Record<string, number>;
    summary: string;
  };
}

interface ColorState {
  targetColor: { hex: string; lab: [number, number, number] };
  baseColors: Color[];
  predictionResult: FormulationResult | null;
  isLoading: boolean;
  error: string | null;
  setTargetColor: (hex: string, lab: [number, number, number]) => void;
  addBaseColor: (color: Color) => void;
  removeBaseColor: (id: string) => void;
  clearBases: () => void;
  setPredictionResult: (result: FormulationResult | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useColorStore = create<ColorState>((set) => ({
  targetColor: { hex: '#3a86c8', lab: [52.4, -5.3, -41.2] },
  baseColors: [
    { id: 'base_red', hex: '#FF0000', lab: [53.2, 80.1, 67.2], name: 'Red Oxide' },
    { id: 'base_blue', hex: '#0000FF', lab: [32.3, 79.2, -108.3], name: 'Phthalo Blue' },
    { id: 'base_white', hex: '#FFFFFF', lab: [100.0, 0.0, 0.0], name: 'Titanium White' },
    { id: 'base_yellow', hex: '#FFFF00', lab: [97.1, -16.0, 94.3], name: 'Medium Yellow' }
  ],
  predictionResult: null,
  isLoading: false,
  error: null,
  setTargetColor: (hex, lab) => set({ targetColor: { hex, lab } }),
  addBaseColor: (color) => set((state) => {
    if (state.baseColors.length >= 8) return state;
    if (state.baseColors.some((c) => c.hex.toLowerCase() === color.hex.toLowerCase())) return state;
    return { baseColors: [...state.baseColors, color] };
  }),
  removeBaseColor: (id) => set((state) => ({
    baseColors: state.baseColors.filter((c) => c.id !== id)
  })),
  clearBases: () => set({ baseColors: [] }),
  setPredictionResult: (result) => set({ predictionResult: result }),
  setLoading: (loading) => set({ isLoading: loading }),
  setError: (error) => set({ error }),
}));
