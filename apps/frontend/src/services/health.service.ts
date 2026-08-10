import apiClient from './apiClient';

export const healthService = {
  async check() {
    const response = await apiClient.get('/health');
    return response.data;
  },
};
