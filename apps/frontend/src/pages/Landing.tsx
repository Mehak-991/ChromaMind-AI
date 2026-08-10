import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, Sliders, Activity, Brain, Sparkles } from 'lucide-react';

export const Landing: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 selection:bg-brand-500 selection:text-white">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 glass border-b border-slate-900 px-8 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded bg-brand-500 flex items-center justify-center font-bold text-white shadow-lg shadow-brand-500/30">
            C
          </div>
          <span className="font-bold text-lg">ChromaMind AI</span>
        </div>
        <div className="flex gap-4">
          <Link to="/login" className="text-slate-400 hover:text-slate-100 text-sm font-semibold transition-colors py-2 px-4">
            Sign In
          </Link>
          <Link to="/signup" className="bg-brand-500 hover:bg-brand-600 shadow-lg shadow-brand-500/20 text-white text-sm font-semibold py-2 px-5 rounded-lg transition-all flex items-center gap-2">
            Register
            <ArrowRight size={16} />
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-8 max-w-7xl mx-auto flex flex-col items-center text-center relative overflow-hidden">
        {/* Glow Effects */}
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-brand-500/10 rounded-full blur-[120px] pointer-events-none" />
        <div className="absolute top-1/3 left-1/3 w-[300px] h-[300px] bg-purple-500/5 rounded-full blur-[100px] pointer-events-none" />

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="space-y-6 max-w-4xl"
        >
          <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-500/10 border border-brand-500/20 text-brand-400 text-xs font-semibold">
            <Sparkles size={12} />
            State-of-the-Art Color Science
          </span>
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight leading-none bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-200 to-brand-500">
            Explainable AI-Powered Color Formulation
          </h1>
          <p className="text-lg md:text-xl text-slate-400 max-w-2xl mx-auto leading-relaxed">
            Instantly predict and optimize color mixtures with physical constraints, minimal Delta E similarity, and explainable neural network coordinates.
          </p>
          <div className="flex gap-4 justify-center pt-4">
            <Link to="/dashboard" className="bg-brand-500 hover:bg-brand-600 shadow-xl shadow-brand-500/30 text-white font-semibold py-3 px-8 rounded-lg transition-all flex items-center gap-2 text-base">
              Launch Console
              <ArrowRight size={18} />
            </Link>
            <a href="#features" className="glass hover:bg-slate-900 border border-slate-800 text-slate-300 hover:text-white font-semibold py-3 px-8 rounded-lg transition-all text-base">
              Explore Features
            </a>
          </div>
        </motion.div>
      </section>

      {/* Features Grid */}
      <section id="features" className="py-20 px-8 max-w-7xl mx-auto border-t border-slate-900">
        <h2 className="text-3xl md:text-4xl font-bold text-center mb-16">
          Architected for Industrial Color Scientists
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="glass p-8 rounded-xl border border-slate-900">
            <div className="w-12 h-12 rounded-lg bg-brand-500/10 border border-brand-500/20 text-brand-400 flex items-center justify-center mb-6">
              <Brain size={24} />
            </div>
            <h3 className="text-xl font-bold mb-3">Predictive Neural Network</h3>
            <p className="text-slate-400 text-sm leading-relaxed">
              Fast deep learning regressor ensemble estimates formulation metrics in under 50ms.
            </p>
          </div>
          <div className="glass p-8 rounded-xl border border-slate-900">
            <div className="w-12 h-12 rounded-lg bg-brand-500/10 border border-brand-500/20 text-brand-400 flex items-center justify-center mb-6">
              <Sliders size={24} />
            </div>
            <h3 className="text-xl font-bold mb-3">DE Optimizer</h3>
            <p className="text-slate-400 text-sm leading-relaxed">
              SciPy Differential Evolution algorithms fine-tune weight ratios to achieve a Delta E under 1.0.
            </p>
          </div>
          <div className="glass p-8 rounded-xl border border-slate-900">
            <div className="w-12 h-12 rounded-lg bg-brand-500/10 border border-brand-500/20 text-brand-400 flex items-center justify-center mb-6">
              <Activity size={24} />
            </div>
            <h3 className="text-xl font-bold mb-3">Explainable AI (SHAP)</h3>
            <p className="text-slate-400 text-sm leading-relaxed">
              Instantly view contribution vectors explaining how each base color coordinate impacts the final recipe.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-slate-900 px-8 text-center text-xs text-slate-500">
        <p>&copy; {new Date().getFullYear()} ChromaMind AI Corp. All rights reserved. Industrial Grade Formulation.</p>
      </footer>
    </div>
  );
};
