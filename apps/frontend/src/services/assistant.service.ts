import apiClient from './apiClient';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export const assistantService = {
  async chat(message: string, contextId?: string) {
    const response = await apiClient.post('/rag/chat', { message, prediction_context_id: contextId });
    return response.data;
  },
};
