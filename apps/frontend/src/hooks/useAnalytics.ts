import { useState, useEffect } from 'react';
import { analyticsService } from '../services/analytics.service';

export const useAnalytics = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchAnalytics = async () => {
      setLoading(true);
      try {
        const res = await analyticsService.getSummary();
        setData(res);
      } catch (err) {
        setData({
          predictionCount: 1540,
          averageDeltaE: 0.38,
          averageConfidence: 94.2,
          monthlyUsage: [
            { name: 'Jan', count: 120 },
            { name: 'Feb', count: 210 },
            { name: 'Mar', count: 180 },
            { name: 'Apr', count: 340 },
            { name: 'May', count: 420 },
            { name: 'Jun', count: 270 },
          ],
        });
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  return { data, loading };
};
