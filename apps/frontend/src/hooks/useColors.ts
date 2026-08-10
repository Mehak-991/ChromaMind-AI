import { useColorStore } from '../store/useColorStore';
import type { Color } from '../store/useColorStore';

export const useColors = () => {
  const { baseColors, addBaseColor, removeBaseColor, clearBases, targetColor, setTargetColor } = useColorStore();

  const handleAddColor = (hex: string) => {
    const id = 'base_' + Math.random().toString(36).substr(2, 9);
    // Simple mock RGB->LAB approximation
    const lab: [number, number, number] = [60, Math.random() * 80 - 40, Math.random() * 80 - 40];
    const newColor: Color = { id, hex, lab, name: `Pigment ${baseColors.length + 1}` };
    addBaseColor(newColor);
  };

  return {
    baseColors,
    targetColor,
    addBaseColor: handleAddColor,
    removeBaseColor,
    clearBases,
    setTargetColor,
  };
};
