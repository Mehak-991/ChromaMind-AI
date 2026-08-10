import React from 'react';
import { useUIStore } from '../store/useUIStore';
import { Sliders, Save } from 'lucide-react';

export const Settings: React.FC = () => {
  const { deltaEThreshold, optimizerIterations, modelSelection, setSettings } = useUIStore();

  const handleSave = () => {
    alert('Configurations updated successfully.');
  };

  return (
    <div className="max-w-3xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-extrabold tracking-tight">System Settings</h1>
        <p className="text-slate-400 text-sm">Configure formulation parameters, optimizer models, and thresholds.</p>
      </div>

      <div className="glass border border-slate-900 rounded-xl p-6 space-y-6">
        <h2 className="text-sm font-semibold flex items-center gap-2 border-b border-slate-800 pb-3">
          <Sliders size={16} className="text-brand-400" />
          Formulator Parameters
        </h2>

        <div className="space-y-4">
          <div className="space-y-1">
            <label className="text-xs font-semibold text-slate-400 flex items-center gap-1">
              Delta E Threshold
              <span className="text-[10px] text-slate-500 font-normal">(Delta E 00)</span>
            </label>
            <input
              type="number"
              step="0.1"
              value={deltaEThreshold}
              onChange={(e) => setSettings({ deltaEThreshold: parseFloat(e.target.value) })}
              className="w-full bg-slate-900 border border-slate-800 focus:border-brand-500 rounded-lg px-3 py-2 text-sm text-slate-100 placeholder-slate-650 focus:outline-none transition-colors"
            />
            <p className="text-[10px] text-slate-500">
              Formulation search stops immediately when similarity is below this metric.
            </p>
          </div>

          <div className="space-y-1">
            <label className="text-xs font-semibold text-slate-400">Optimizer Max Iterations</label>
            <input
              type="number"
              value={optimizerIterations}
              onChange={(e) => setSettings({ optimizerIterations: parseInt(e.target.value) })}
              className="w-full bg-slate-900 border border-slate-800 focus:border-brand-500 rounded-lg px-3 py-2 text-sm text-slate-100 placeholder-slate-650 focus:outline-none transition-colors"
            />
          </div>

          <div className="space-y-1">
            <label className="text-xs font-semibold text-slate-400">Prediction Engine Model</label>
            <select
              value={modelSelection}
              onChange={(e) => setSettings({ modelSelection: e.target.value })}
              className="w-full bg-slate-900 border border-slate-800 focus:border-brand-500 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none transition-colors"
            >
              <option value="NeuralNet-Ensemble-v1">NeuralNet-Ensemble-v1 (Recommended)</option>
              <option value="XGBoost-Ensemble-v2">XGBoost-Ensemble-v2</option>
              <option value="Physical-Simulation-Only">Physical-Simulation-Only</option>
            </select>
          </div>
        </div>

        <button
          onClick={handleSave}
          className="w-full py-2.5 bg-brand-500 hover:bg-brand-600 text-white font-semibold rounded-lg text-sm transition-colors flex items-center justify-center gap-2 shadow-lg shadow-brand-500/20"
        >
          <Save size={16} />
          Save Configurations
        </button>
      </div>
    </div>
  );
};
