import { create } from 'zustand';

interface User {
  id: string;
  email: string;
  fullName: string;
  role: 'user' | 'admin' | 'scientist';
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (user: User, token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: {
    id: 'u_dev_123',
    email: 'scientist@chromamind.ai',
    fullName: 'Dr. Sarah Carter',
    role: 'scientist'
  }, // Prepopulate with a default development session user
  token: 'mock_jwt_token',
  isAuthenticated: true,
  login: (user, token) => set({ user, token, isAuthenticated: true }),
  logout: () => set({ user: null, token: null, isAuthenticated: false }),
}));
