import { useState, useEffect } from 'react';
import { historyService } from '../services/history.service';

export const useHistory = () => {
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const data = await historyService.getHistory();
      setHistory(data.items || []);
    } catch (err) {
      console.warn("Backend offline, returning mock formulation history.");
      setHistory([
        { id: '1', target_hex: '#3a86c8', delta_e: 0.42, created_at: '2026-08-07T02:15:00Z' },
        { id: '2', target_hex: '#e25c5c', delta_e: 0.81, created_at: '2026-08-06T14:30:00Z' },
        { id: '3', target_hex: '#4caf50', delta_e: 0.12, created_at: '2026-08-05T09:12:00Z' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  return { history, loading, refresh: fetchHistory };
};
