import apiClient from './apiClient';

export const authService = {
  async login(payload: any) {
    const response = await apiClient.post('/auth/login', payload);
    return response.data;
  },
  async register(payload: any) {
    const response = await apiClient.post('/auth/register', payload);
    return response.data;
  },
};
