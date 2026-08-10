import apiClient from './apiClient';

export const settingsService = {
  async updateSettings(payload: any) {
    const response = await apiClient.patch('/settings', payload);
    return response.data;
  },
};
