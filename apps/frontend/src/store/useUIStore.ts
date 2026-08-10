import { create } from 'zustand';

interface UIState {
  theme: 'dark' | 'light';
  language: string;
  isSidebarOpen: boolean;
  deltaEThreshold: number;
  optimizerIterations: number;
  modelSelection: string;
  toggleTheme: () => void;
  setLanguage: (lang: string) => void;
  setSidebarOpen: (open: boolean) => void;
  setSettings: (settings: { deltaEThreshold?: number; optimizerIterations?: number; modelSelection?: string }) => void;
}

export const useUIStore = create<UIState>((set) => ({
  theme: 'dark',
  language: 'en',
  isSidebarOpen: true,
  deltaEThreshold: 1.0,
  optimizerIterations: 1000,
  modelSelection: 'NeuralNet-Ensemble-v1',
  toggleTheme: () => set((state) => ({ theme: state.theme === 'dark' ? 'light' : 'dark' })),
  setLanguage: (language) => set({ language }),
  setSidebarOpen: (isSidebarOpen) => set({ isSidebarOpen }),
  setSettings: (settings) => set((state) => ({ ...state, ...settings })),
}));
