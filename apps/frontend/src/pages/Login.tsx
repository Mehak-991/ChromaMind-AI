import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useAuthStore } from '../store/useAuthStore';
import { Shield } from 'lucide-react';
import apiClient from '../services/apiClient';

const loginSchema = z.object({
  email: z.string().email({ message: 'Enter a valid email address' }),
  password: z.string().min(6, { message: 'Password must be at least 6 characters' }),
});

type LoginFormValues = z.infer<typeof loginSchema>;

export const Login: React.FC = () => {
  const { login } = useAuthStore();
  const navigate = useNavigate();

  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema)
  });

  const onSubmit = async (data: LoginFormValues) => {
    try {
      const response = await apiClient.post('/auth/login', {
        email: data.email,
        password: data.password,
      });
      const { access_token, user } = response.data;
      
      login({
        id: user.id,
        email: user.email,
        fullName: user.full_name,
        role: user.role,
      }, access_token);
      
      navigate('/dashboard');
    } catch (error: any) {
      console.error('Login failed', error);
      // In a real app we'd display this error to the user
      alert(error.response?.data?.detail || 'Login failed');
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center px-4 relative overflow-hidden">
      <div className="absolute w-[400px] h-[400px] bg-brand-500/5 rounded-full blur-[100px] pointer-events-none" />

      <div className="w-full max-w-md glass border border-slate-900 rounded-xl p-8 space-y-6">
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-lg bg-brand-500/10 border border-brand-500/20 text-brand-400 flex items-center justify-center mx-auto">
            <Shield size={24} />
          </div>
          <h2 className="text-2xl font-bold">Sign In</h2>
          <p className="text-xs text-slate-500">Access your ChromaMind AI console</p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="space-y-1">
            <label className="text-xs font-semibold text-slate-400">Email Address</label>
            <input
              type="email"
              {...register('email')}
              className="w-full bg-slate-900 border border-slate-800 focus:border-brand-500 rounded-lg px-3 py-2 text-sm text-slate-100 placeholder-slate-600 focus:outline-none transition-colors"
              placeholder="name@company.com"
            />
            {errors.email && <p className="text-[10px] text-red-400">{errors.email.message}</p>}
          </div>

          <div className="space-y-1">
            <label className="text-xs font-semibold text-slate-400">Password</label>
            <input
              type="password"
              {...register('password')}
              className="w-full bg-slate-900 border border-slate-800 focus:border-brand-500 rounded-lg px-3 py-2 text-sm text-slate-100 placeholder-slate-600 focus:outline-none transition-colors"
              placeholder="••••••••"
            />
            {errors.password && <p className="text-[10px] text-red-400">{errors.password.message}</p>}
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full py-2.5 bg-brand-500 hover:bg-brand-600 disabled:bg-brand-500/50 text-white font-semibold rounded-lg text-sm transition-all shadow-lg shadow-brand-500/20"
          >
            {isSubmitting ? 'Verifying...' : 'Sign In'}
          </button>
        </form>

        <div className="text-center text-xs text-slate-500">
          Don't have an account?{' '}
          <Link to="/signup" className="text-brand-400 hover:text-brand-300 font-semibold">
            Create Account
          </Link>
        </div>
      </div>
    </div>
  );
};
