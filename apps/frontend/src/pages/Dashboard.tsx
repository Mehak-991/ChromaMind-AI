import React, { useState, useEffect } from 'react';
import { useColors } from '../hooks/useColors';
import { usePrediction } from '../hooks/usePrediction';
import { HexColorPicker } from 'react-colorful';
import { Plus, Trash, Wand2, RefreshCw } from 'lucide-react';
import { useColorStore } from '../store/useColorStore';
import { motion, AnimatePresence } from 'framer-motion';

export const Dashboard: React.FC = () => {
  const { baseColors, targetColor, addBaseColor, removeBaseColor, setTargetColor } = useColors();
  const { runPrediction, isLoading } = usePrediction();
  const { predictionResult, error } = useColorStore();
  const [newColorHex, setNewColorHex] = useState('#ff5555');

  const handleAddBase = () => {
    addBaseColor(newColorHex);
  };

  // Real-time updates whenever Target Color or Base Pigments change
  const baseIdsKey = baseColors.map((c) => c.id + c.hex).join(',');
  useEffect(() => {
    if (baseColors.length >= 3) {
      const timer = setTimeout(() => {
        runPrediction();
      }, 350); // slight debounce to avoid excessive requests during color drag
      return () => clearTimeout(timer);
    }
  }, [targetColor.hex, baseIdsKey]);

  // Delta E status styling helper
  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'Excellent Match':
        return <span className="px-2.5 py-1 text-xs font-semibold rounded bg-green-500/20 text-green-400 border border-green-500/25">Excellent Match</span>;
      case 'Very Good Match':
        return <span className="px-2.5 py-1 text-xs font-semibold rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/25">Very Good Match</span>;
      case 'Good Match':
        return <span className="px-2.5 py-1 text-xs font-semibold rounded bg-blue-500/20 text-blue-400 border border-blue-500/25">Good Match</span>;
      default:
        return <span className="px-2.5 py-1 text-xs font-semibold rounded bg-amber-500/20 text-amber-400 border border-amber-500/25">Needs Optimization</span>;
    }
  };

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Page Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight">Formulation Console</h1>
          <p className="text-slate-400 text-sm">Industrial-grade color synthesis & physical matching engine.</p>
        </div>
        {baseColors.length >= 3 && (
          <button
            onClick={() => runPrediction()}
            disabled={isLoading}
            className="px-4 py-2 bg-slate-900 border border-slate-800 text-xs font-bold rounded-lg hover:bg-slate-800 transition-all flex items-center gap-2"
          >
            <RefreshCw size={14} className={isLoading ? 'animate-spin' : ''} />
            Recalculate
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Input Selection Panels */}
        <div className="space-y-6 lg:col-span-2">
          {/* Target Color Picker & Large Predicted Result */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Color Picker card */}
            <div className="glass p-6 rounded-xl border border-slate-200 dark:border-slate-900 flex flex-col items-center justify-between min-h-[350px]">
              <h2 className="text-sm font-semibold self-start border-b border-slate-200 dark:border-slate-800 pb-2 w-full mb-4">Target Color</h2>
              <HexColorPicker
                color={targetColor.hex}
                onChange={(hex) => setTargetColor(hex, targetColor.lab)}
                className="w-full max-w-[220px]"
              />
              <div className="flex gap-4 items-center justify-between w-full mt-4 bg-slate-100/50 dark:bg-slate-950/40 p-3 rounded-lg border border-slate-200 dark:border-slate-900">
                <div className="flex items-center gap-3">
                  <div
                    className="w-12 h-12 rounded-lg border border-slate-200 dark:border-slate-800 shadow"
                    style={{ backgroundColor: targetColor.hex }}
                  />
                  <div>
                    <p className="text-xs font-bold text-slate-800 dark:text-slate-300">{targetColor.hex.toUpperCase()}</p>
                    <p className="text-[10px] text-slate-600 dark:text-slate-500 uppercase font-mono">
                      LAB: {targetColor.lab[0].toFixed(1)}, {targetColor.lab[1].toFixed(1)}, {targetColor.lab[2].toFixed(1)}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* AI Predicted Mixed Color (Industrial Software Style) */}
            <div className="glass p-6 rounded-xl border border-slate-200 dark:border-slate-900 flex flex-col justify-between min-h-[350px]">
              <h2 className="text-sm font-semibold border-b border-slate-200 dark:border-slate-800 pb-2 w-full">Predicted Mixed Color</h2>
              
              <div className="my-4 flex-1 flex flex-col justify-center">
                <AnimatePresence mode="wait">
                  {predictionResult ? (
                    <motion.div
                      key={predictionResult.predictedHex}
                      initial={{ opacity: 0, scale: 0.95 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.95 }}
                      transition={{ duration: 0.3 }}
                      className="w-full h-32 rounded-lg shadow-inner relative flex items-end p-3"
                      style={{ backgroundColor: predictionResult.predictedHex }}
                    >
                      <div className="absolute inset-0 rounded-lg border border-white/10 pointer-events-none" />
                      <div className="bg-white/90 dark:bg-slate-950/70 backdrop-blur-md px-3 py-1.5 rounded border border-slate-200 dark:border-slate-800 text-[10px] font-mono text-slate-800 dark:text-slate-300 flex justify-between w-full shadow-sm">
                        <span>HEX: {predictionResult.predictedHex.toUpperCase()}</span>
                        <span>RGB: {predictionResult.predictedRgb.join(', ')}</span>
                      </div>
                    </motion.div>
                  ) : (
                    <div className="w-full h-32 rounded-lg bg-slate-100/20 dark:bg-slate-950/20 border border-dashed border-slate-200 dark:border-slate-850 flex items-center justify-center text-slate-400 dark:text-slate-600 text-xs">
                      Awaiting formulation variables...
                    </div>
                  )}
                </AnimatePresence>
              </div>

              {predictionResult && (
                <div className="grid grid-cols-3 gap-2 bg-slate-100/50 dark:bg-slate-950/40 p-3 rounded-lg border border-slate-200 dark:border-slate-900 text-center">
                  <div>
                    <span className="text-[9px] text-slate-600 dark:text-slate-500 uppercase font-semibold block">Predicted L*</span>
                    <span className="text-xs font-mono font-bold text-slate-800 dark:text-slate-300">{predictionResult.predictedLab[0].toFixed(2)}</span>
                  </div>
                  <div>
                    <span className="text-[9px] text-slate-600 dark:text-slate-500 uppercase font-semibold block">Predicted a*</span>
                    <span className="text-xs font-mono font-bold text-slate-800 dark:text-slate-300">{predictionResult.predictedLab[1].toFixed(2)}</span>
                  </div>
                  <div>
                    <span className="text-[9px] text-slate-600 dark:text-slate-500 uppercase font-semibold block">Predicted b*</span>
                    <span className="text-xs font-mono font-bold text-slate-800 dark:text-slate-300">{predictionResult.predictedLab[2].toFixed(2)}</span>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Base Pigments Selection Panel */}
          <div className="glass p-6 rounded-xl border border-slate-200 dark:border-slate-900 space-y-6">
            <div className="flex justify-between items-center border-b border-slate-200 dark:border-slate-800 pb-3">
              <div>
                <h2 className="text-sm font-semibold">Available Base Colors ({baseColors.length}/8)</h2>
                <p className="text-[10px] text-slate-600 dark:text-slate-500">Provide 3 to 8 pigments to use for formulation mixing</p>
              </div>

              {baseColors.length < 8 && (
                <div className="flex gap-2 items-center">
                  <input
                    type="color"
                    value={newColorHex}
                    onChange={(e) => setNewColorHex(e.target.value)}
                    className="w-8 h-8 rounded border border-slate-200 dark:border-slate-800 bg-transparent cursor-pointer"
                  />
                  <button
                    onClick={handleAddBase}
                    className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-xs font-semibold rounded-lg hover:text-slate-900 dark:hover:text-slate-100 transition-all flex items-center gap-1.5 text-slate-700 dark:text-slate-300"
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
                  className="p-3 bg-slate-100/50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800/80 rounded-lg flex flex-col justify-between h-28 hover:border-slate-400 dark:hover:border-slate-700/80 transition-all"
                >
                  <div className="flex justify-between items-start">
                    <div
                      className="w-6 h-6 rounded border border-slate-200 dark:border-slate-800/50 shadow-sm"
                      style={{ backgroundColor: color.hex }}
                    />
                    <button
                      onClick={() => removeBaseColor(color.id)}
                      className="text-slate-500 hover:text-red-500 dark:hover:text-red-400 p-1 rounded-full hover:bg-slate-200 dark:hover:bg-slate-800 transition-colors"
                    >
                      <Trash size={12} />
                    </button>
                  </div>
                  <div>
                    <p className="text-xs font-semibold truncate text-slate-800 dark:text-slate-200">{color.name || 'Pigment'}</p>
                    <p className="text-[10px] text-slate-500 dark:text-slate-400 uppercase font-mono">{color.hex}</p>
                  </div>
                </div>
              ))}
            </div>

            {error && <p className="text-xs text-red-500">{error}</p>}

            <button
              onClick={() => runPrediction()}
              disabled={isLoading || baseColors.length < 3}
              className="w-full py-3 bg-brand-500 hover:bg-brand-600 disabled:bg-slate-200 dark:disabled:bg-slate-900 disabled:text-slate-400 dark:disabled:text-slate-500 disabled:border-slate-300 dark:disabled:border-slate-800/60 disabled:cursor-not-allowed border border-brand-500/20 text-white font-bold rounded-lg text-sm transition-all shadow-lg shadow-brand-500/20 flex items-center justify-center gap-2"
            >
              <Wand2 size={16} />
              {isLoading ? 'Running Global Optimizer...' : 'Formulate Target Color'}
            </button>
          </div>
        </div>

        {/* Right Column: Prediction Results Details */}
        <div className="space-y-6">
          <div className="glass p-6 rounded-xl border border-slate-200 dark:border-slate-900 h-full flex flex-col justify-between min-h-[400px]">
            <div>
              <h2 className="text-sm font-semibold border-b border-slate-200 dark:border-slate-800 pb-3 mb-5">Match Comparison</h2>
              
              {predictionResult ? (
                <div className="space-y-6">
                  {/* Side by Side Comparison Swatches */}
                  <div className="grid grid-cols-2 gap-3 p-1.5 bg-slate-100/50 dark:bg-slate-950/40 rounded-xl border border-slate-200 dark:border-slate-900">
                    <div className="p-3 bg-slate-50 dark:bg-slate-900/40 rounded-lg flex flex-col items-center text-center space-y-2 border border-slate-150 dark:border-slate-850">
                      <span className="text-[10px] text-slate-500 dark:text-slate-400 uppercase font-semibold">Target</span>
                      <div className="w-16 h-16 rounded-md border border-slate-200 dark:border-slate-800 shadow-sm" style={{ backgroundColor: targetColor.hex }} />
                      <span className="text-xs font-mono font-bold text-slate-850 dark:text-slate-200">{targetColor.hex.toUpperCase()}</span>
                    </div>
                    <div className="p-3 bg-slate-50 dark:bg-slate-900/40 rounded-lg flex flex-col items-center text-center space-y-2 border border-slate-150 dark:border-slate-850">
                      <span className="text-[10px] text-slate-500 dark:text-slate-400 uppercase font-semibold">Predicted</span>
                      <div className="w-16 h-16 rounded-md border border-slate-200 dark:border-slate-800 shadow-sm" style={{ backgroundColor: predictionResult.predictedHex }} />
                      <span className="text-xs font-mono font-bold text-slate-850 dark:text-slate-200">{predictionResult.predictedHex.toUpperCase()}</span>
                    </div>
                  </div>

                  {/* Metrics Row */}
                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-3 bg-slate-50 dark:bg-slate-900/40 border border-slate-200 dark:border-slate-850 rounded-lg text-center shadow-sm">
                      <p className="text-[9px] text-slate-500 dark:text-slate-400 uppercase font-semibold">Delta E (CIEDE2000)</p>
                      <p className="text-lg font-black text-green-600 dark:text-green-400">{predictionResult.deltaE.toFixed(2)}</p>
                    </div>
                    <div className="p-3 bg-slate-50 dark:bg-slate-900/40 border border-slate-200 dark:border-slate-850 rounded-lg text-center shadow-sm">
                      <p className="text-[9px] text-slate-500 dark:text-slate-400 uppercase font-semibold">Similarity</p>
                      <p className="text-lg font-black text-brand-600 dark:text-brand-400">
                        {predictionResult.confidenceScore.toFixed(1)}%
                      </p>
                    </div>
                  </div>

                  {/* Match status badge */}
                  <div className="flex justify-between items-center p-3 bg-slate-50 dark:bg-slate-900/40 border border-slate-200 dark:border-slate-850 rounded-lg shadow-sm">
                    <span className="text-xs text-slate-600 dark:text-slate-400 font-semibold">System Quality Rating</span>
                    {getStatusBadge(predictionResult.status)}
                  </div>

                  {/* Recipe Table */}
                  <div className="space-y-3">
                    <h3 className="text-xs font-bold text-slate-700 dark:text-slate-400">Pigment Formula Recipe</h3>
                    
                    <div className="overflow-x-auto rounded-lg border border-slate-200 dark:border-slate-850 bg-slate-100/20 dark:bg-slate-950/20">
                      <table className="min-w-full divide-y divide-slate-200 dark:divide-slate-850 text-left text-xs">
                        <thead className="bg-slate-100 dark:bg-slate-900/60 font-semibold text-slate-600 dark:text-slate-400">
                          <tr>
                            <th className="p-2.5">Pigment</th>
                            <th className="p-2.5 text-right">Ratio %</th>
                            <th className="p-2.5 text-right">Weight (g)</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-200 dark:divide-slate-850">
                          {predictionResult.ratios.map((item) => {
                            const base = baseColors.find((c) => c.name === item.pigment || c.id === item.pigment);
                            return (
                              <tr key={item.pigment} className="hover:bg-slate-100 dark:hover:bg-slate-900/40">
                                <td className="p-2.5 flex items-center gap-2 truncate">
                                  <div className="w-3.5 h-3.5 rounded-full border border-slate-300 dark:border-slate-800 shadow-sm" style={{ backgroundColor: base?.hex || '#ccc' }} />
                                  <span className="truncate text-slate-800 dark:text-slate-300">{item.pigment}</span>
                                </td>
                                <td className="p-2.5 text-right font-mono font-semibold text-slate-700 dark:text-slate-300">{(item.ratio * 100).toFixed(2)}%</td>
                                <td className="p-2.5 text-right font-mono font-semibold text-slate-700 dark:text-slate-300">{item.weightGrams.toFixed(2)}g</td>
                              </tr>
                            );
                          })}
                        </tbody>
                      </table>
                    </div>
                  </div>

                  {/* Explainable AI summary */}
                  <div className="p-4 bg-brand-500/5 border border-brand-500/10 rounded-lg">
                    <h4 className="text-xs font-bold text-brand-500 dark:text-brand-400 mb-1.5">AI Synthesis Explanation</h4>
                    <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                      {predictionResult.explanation.summary}
                    </p>
                  </div>
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center h-80 text-center space-y-3">
                  <div className="w-12 h-12 rounded-full bg-slate-100/40 dark:bg-slate-950/40 border border-slate-200 dark:border-slate-850 flex items-center justify-center text-slate-400 dark:text-slate-500">
                    <Wand2 size={20} />
                  </div>
                  <div className="space-y-1">
                    <h3 className="text-sm font-semibold">No active recipe</h3>
                    <p className="text-xs text-slate-500 dark:text-slate-400 max-w-[200px] mx-auto">
                      Select bases and adjust target color to generate color formulations.
                    </p>
                  </div>
                </div>
              )}
            </div>

            {predictionResult && (
              <div className="border-t border-slate-200 dark:border-slate-800/60 pt-4 flex gap-3 mt-6">
                <button className="flex-1 py-2 bg-slate-100 hover:bg-slate-200 dark:bg-slate-900 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-800 text-xs font-semibold rounded-lg transition-all text-center text-slate-700 dark:text-slate-300">
                  Export PDF
                </button>
                <button className="flex-1 py-2 bg-slate-100 hover:bg-slate-200 dark:bg-slate-900 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-800 text-xs font-semibold rounded-lg transition-all text-center text-slate-700 dark:text-slate-300">
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

