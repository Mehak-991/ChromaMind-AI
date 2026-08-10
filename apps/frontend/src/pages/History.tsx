import React from 'react';
import { useHistory } from '../hooks/useHistory';
import { Search, Calendar, Heart, SlidersHorizontal } from 'lucide-react';

export const History: React.FC = () => {
  const { history, loading } = useHistory();

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight">Formulation History</h1>
          <p className="text-slate-400 text-sm">Browse, filter, and review previous recipe generation requests.</p>
        </div>
      </div>

      {/* Filter toolbar */}
      <div className="flex gap-4">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={16} />
          <input
            type="text"
            className="w-full bg-slate-900 border border-slate-800 focus:border-brand-500 rounded-lg pl-10 pr-4 py-2 text-sm text-slate-100 placeholder-slate-600 focus:outline-none transition-colors"
            placeholder="Search by target HEX code or formulation ID..."
          />
        </div>
        <button className="px-4 py-2 bg-slate-900 border border-slate-800 text-sm font-semibold rounded-lg hover:bg-slate-800 transition-all flex items-center gap-2">
          <SlidersHorizontal size={14} />
          Filter
        </button>
      </div>

      {/* Grid of history cards */}
      {loading ? (
        <div className="text-sm text-slate-500">Loading history records...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {history.map((item) => (
            <div
              key={item.id}
              className="glass p-5 rounded-xl border border-slate-900 hover:border-slate-800 transition-all flex flex-col justify-between h-44"
            >
              <div>
                <div className="flex justify-between items-start">
                  <div className="flex items-center gap-2">
                    <div
                      className="w-8 h-8 rounded border border-slate-800"
                      style={{ backgroundColor: item.target_hex }}
                    />
                    <div>
                      <h3 className="text-xs font-bold uppercase">{item.target_hex}</h3>
                      <p className="text-[9px] text-slate-500">ID: {item.id}</p>
                    </div>
                  </div>
                  <button className="text-slate-600 hover:text-red-400 transition-colors">
                    <Heart size={14} />
                  </button>
                </div>

                <div className="mt-4 grid grid-cols-2 gap-2 text-xs">
                  <div className="bg-slate-950/40 p-2 rounded border border-slate-900">
                    <span className="text-[9px] text-slate-500 uppercase block">Delta E (00)</span>
                    <span className="font-semibold text-green-400">{item.delta_e.toFixed(3)}</span>
                  </div>
                  <div className="bg-slate-950/40 p-2 rounded border border-slate-900">
                    <span className="text-[9px] text-slate-500 uppercase block">Status</span>
                    <span className="font-semibold text-brand-400">Match Saved</span>
                  </div>
                </div>
              </div>

              <div className="flex justify-between items-center text-[10px] text-slate-500 border-t border-slate-900 pt-3">
                <span className="flex items-center gap-1">
                  <Calendar size={10} />
                  {new Date(item.created_at).toLocaleDateString()}
                </span>
                <button className="text-brand-400 hover:text-brand-300 font-semibold">
                  Load Workspace
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
