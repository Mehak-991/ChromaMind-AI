import apiClient from './apiClient';

export const analyticsService = {
  async getSummary() {
    const response = await apiClient.get('/analytics/summary');
    return response.data;
  },
};
