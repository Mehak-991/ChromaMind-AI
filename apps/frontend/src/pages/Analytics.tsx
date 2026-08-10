import React from 'react';
import { useAnalytics } from '../hooks/useAnalytics';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';

export const Analytics: React.FC = () => {
  const { data, loading } = useAnalytics();

  if (loading) {
    return <div className="text-sm text-slate-500">Loading analytics dashboards...</div>;
  }

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      <div>
        <h1 className="text-3xl font-extrabold tracking-tight">Performance Analytics</h1>
        <p className="text-slate-400 text-sm">Analyze formulate throughput, similarity improvement rates, and system loads.</p>
      </div>

      {/* Stats summary row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass p-6 rounded-xl border border-slate-900">
          <p className="text-xs text-slate-500 font-semibold uppercase">Total Formulations Run</p>
          <p className="text-3xl font-black mt-2 text-white">{data?.predictionCount || 0}</p>
        </div>
        <div className="glass p-6 rounded-xl border border-slate-900">
          <p className="text-xs text-slate-500 font-semibold uppercase">Average Delta E (00)</p>
          <p className="text-3xl font-black mt-2 text-green-400">{data?.averageDeltaE || 0.0}</p>
        </div>
        <div className="glass p-6 rounded-xl border border-slate-900">
          <p className="text-xs text-slate-500 font-semibold uppercase">Avg Confidence Score</p>
          <p className="text-3xl font-black mt-2 text-brand-400">{data?.averageConfidence || 0.0}%</p>
        </div>
      </div>

      {/* Chart grids */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="glass p-6 rounded-xl border border-slate-900 space-y-4">
          <h2 className="text-sm font-semibold">Monthly Usage Rates</h2>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data?.monthlyUsage || []}>
                <defs>
                  <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#0e91eb" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#0e91eb" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="name" stroke="#64748b" fontSize={10} />
                <YAxis stroke="#64748b" fontSize={10} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b' }} />
                <Area type="monotone" dataKey="count" stroke="#0e91eb" fillOpacity={1} fill="url(#colorCount)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="glass p-6 rounded-xl border border-slate-900 space-y-4">
          <h2 className="text-sm font-semibold">Optimizer Success Metrics</h2>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data?.monthlyUsage || []}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="name" stroke="#64748b" fontSize={10} />
                <YAxis stroke="#64748b" fontSize={10} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b' }} />
                <Bar dataKey="count" fill="#38acf8" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
