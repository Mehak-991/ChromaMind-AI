import { useEffect } from 'react';
import { useUIStore } from '../store/useUIStore';

export const useTheme = () => {
  const { theme, toggleTheme } = useUIStore();

  useEffect(() => {
    const root = window.document.documentElement;
    if (theme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
  }, [theme]);

  return { theme, toggleTheme, isDark: theme === 'dark' };
};
