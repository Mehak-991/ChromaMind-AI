import React, { useState } from 'react';
import { useColors } from '../hooks/useColors';
import { usePrediction } from '../hooks/usePrediction';
import { ColorSpace3D } from '../components/color/ColorSpace3D';
import { HexColorPicker } from 'react-colorful';
import { Plus, Trash, Wand2 } from 'lucide-react';
import { useColorStore } from '../store/useColorStore';

export const Dashboard: React.FC = () => {
  const { baseColors, targetColor, addBaseColor, removeBaseColor, setTargetColor } = useColors();
  const { runPrediction, isLoading } = usePrediction();
  const { predictionResult, error } = useColorStore();
  const [newColorHex, setNewColorHex] = useState('#ff5555');

  const handleAddBase = () => {
    addBaseColor(newColorHex);
  };

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-extrabold tracking-tight">Formulation Console</h1>
        <p className="text-slate-400 text-sm">Configure target properties and generate optimal pigment recipes.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Configuration Controls */}
        <div className="space-y-6 lg:col-span-2">
          {/* Target Color Selection & 3D Sphere */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="glass p-6 rounded-xl border border-slate-900 flex flex-col items-center justify-center gap-4">
              <h2 className="text-sm font-semibold self-start">Target Color Picker</h2>
              <HexColorPicker
                color={targetColor.hex}
                onChange={(hex) => setTargetColor(hex, [50, 0, 0])}
                className="w-full max-w-[200px]"
              />
              <div className="flex gap-4 items-center justify-between w-full mt-2">
                <div className="flex items-center gap-2">
                  <div
                    className="w-10 h-10 rounded border border-slate-800"
                    style={{ backgroundColor: targetColor.hex }}
                  />
                  <div>
                    <p className="text-xs font-semibold">{targetColor.hex.toUpperCase()}</p>
                    <p className="text-[10px] text-slate-500">Target RGB / LAB</p>
                  </div>
                </div>
              </div>
            </div>

            {/* 3D Visualizer */}
            <div className="glass p-6 rounded-xl border border-slate-900 flex flex-col">
              <h2 className="text-sm font-semibold mb-4">3D CIELAB Coordinates</h2>
              <ColorSpace3D />
            </div>
          </div>

          {/* Base Pigments Selection Panel */}
          <div className="glass p-6 rounded-xl border border-slate-900 space-y-6">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <div>
                <h2 className="text-sm font-semibold">Available Base Colors ({baseColors.length}/8)</h2>
                <p className="text-[10px] text-slate-500">Provide 3 to 8 pigments to use for formulation mixing</p>
              </div>

              {baseColors.length < 8 && (
                <div className="flex gap-2 items-center">
                  <input
                    type="color"
                    value={newColorHex}
                    onChange={(e) => setNewColorHex(e.target.value)}
                    className="w-8 h-8 rounded border border-slate-800 bg-transparent cursor-pointer"
                  />
                  <button
                    onClick={handleAddBase}
                    className="px-3 py-1.5 bg-slate-900 border border-slate-800 text-xs font-semibold rounded-lg hover:bg-slate-800 transition-all flex items-center gap-1.5"
                  >
                    <Plus size={14} />
                    Add Base
                  </button>
                </div>
              )}
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {baseColors.map((color) => (
                <div
                  key={color.id}
                  className="p-3 bg-slate-900/60 border border-slate-800/80 rounded-lg flex flex-col justify-between h-28 hover:border-slate-700/80 transition-all"
                >
                  <div className="flex justify-between items-start">
                    <div
                      className="w-6 h-6 rounded border border-slate-800/50"
                      style={{ backgroundColor: color.hex }}
                    />
                    <button
                      onClick={() => removeBaseColor(color.id)}
                      className="text-slate-500 hover:text-red-400 p-1 rounded-full hover:bg-slate-800 transition-colors"
                    >
                      <Trash size={12} />
                    </button>
                  </div>
                  <div>
                    <p className="text-xs font-semibold truncate">{color.name || 'Pigment'}</p>
                    <p className="text-[10px] text-slate-500 uppercase">{color.hex}</p>
                  </div>
                </div>
              ))}
            </div>

            {error && <p className="text-xs text-red-400">{error}</p>}

            <button
              onClick={runPrediction}
              disabled={isLoading || baseColors.length < 3}
              className="w-full py-3 bg-brand-500 hover:bg-brand-600 disabled:bg-slate-900 disabled:text-slate-500 disabled:border-slate-800/60 disabled:cursor-not-allowed border border-brand-500/20 text-white font-bold rounded-lg text-sm transition-all shadow-lg shadow-brand-500/20 flex items-center justify-center gap-2"
            >
              <Wand2 size={16} />
              {isLoading ? 'Running Global Optimizer...' : 'Formulate Target Color'}
            </button>
          </div>
        </div>

        {/* Right Column: Prediction Results */}
        <div className="space-y-6">
          <div className="glass p-6 rounded-xl border border-slate-900 h-full flex flex-col justify-between min-h-[400px]">
            <div>
              <h2 className="text-sm font-semibold mb-6">Formulation Results</h2>
              {predictionResult ? (
                <div className="space-y-6">
                  {/* Score Badges */}
                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-3 bg-slate-900/60 border border-slate-800/80 rounded-lg">
                      <p className="text-[10px] text-slate-500 uppercase font-semibold">Delta E (00)</p>
                      <p className="text-xl font-black text-green-400">{predictionResult.deltaE.toFixed(4)}</p>
                      <span className="text-[9px] text-slate-400">Excellent Match</span>
                    </div>
                    <div className="p-3 bg-slate-900/60 border border-slate-800/80 rounded-lg">
                      <p className="text-[10px] text-slate-500 uppercase font-semibold">Confidence</p>
                      <p className="text-xl font-black text-brand-400">
                        {(predictionResult.confidenceScore * 100).toFixed(1)}%
                      </p>
                      <span className="text-[9px] text-slate-400">Accuracy Score</span>
                    </div>
                  </div>

                  {/* Ratio bar displays */}
                  <div className="space-y-3">
                    <h3 className="text-xs font-semibold text-slate-400">Recommended Recipe Weight</h3>
                    {predictionResult.ratios.map((item) => {
                      const base = baseColors.find((c) => c.id === item.baseId);
                      return (
                        <div key={item.baseId} className="space-y-1">
                          <div className="flex justify-between text-xs font-medium">
                            <span className="truncate">{base?.name || 'Base'}</span>
                            <span>{(item.ratio * 100).toFixed(1)}% ({item.weightGrams}g)</span>
                          </div>
                          <div className="h-2 w-full bg-slate-900 rounded overflow-hidden">
                            <div
                              className="h-full rounded"
                              style={{
                                width: `${item.ratio * 100}%`,
                                backgroundColor: base?.hex || '#ffffff',
                              }}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>

                  {/* Explainable AI summary */}
                  <div className="p-4 bg-brand-500/5 border border-brand-500/10 rounded-lg">
                    <h4 className="text-xs font-bold text-brand-400 mb-1">AI Explanation Summary</h4>
                    <p className="text-xs text-slate-400 leading-relaxed">
                      {predictionResult.explanation.summary}
                    </p>
                  </div>
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center h-64 text-center space-y-3">
                  <div className="w-12 h-12 rounded-full bg-slate-950/40 border border-slate-800/40 flex items-center justify-center text-slate-500">
                    <Wand2 size={20} />
                  </div>
                  <div className="space-y-1">
                    <h3 className="text-sm font-semibold">No active recipe</h3>
                    <p className="text-xs text-slate-500 max-w-[200px] mx-auto">
                      Select bases and click Formulate to generate color recipes.
                    </p>
                  </div>
                </div>
              )}
            </div>

            {predictionResult && (
              <div className="border-t border-slate-800/60 pt-4 flex gap-3 mt-6">
                <button className="flex-1 py-2 bg-slate-900 hover:bg-slate-800 border border-slate-800 text-xs font-semibold rounded-lg transition-all text-center">
                  Export PDF
                </button>
                <button className="flex-1 py-2 bg-slate-900 hover:bg-slate-800 border border-slate-800 text-xs font-semibold rounded-lg transition-all text-center">
                  Save Recipe
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
