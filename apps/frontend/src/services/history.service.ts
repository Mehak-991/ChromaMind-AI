import apiClient from './apiClient';

export const historyService = {
  async getHistory(page = 1, limit = 10) {
    const response = await apiClient.get('/history', { params: { page, limit } });
    return response.data;
  },
  async getPredictionById(id: string) {
    const response = await apiClient.get(`/history/${id}`);
    return response.data;
  },
  async saveRecipe(recipe: any) {
    const response = await apiClient.post('/history/save', recipe);
    return response.data;
  },
};
