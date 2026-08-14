import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { LayoutDashboard, History, BarChart3, Settings, MessageSquareShare, LogOut, Moon, Sun, ShieldAlert } from 'lucide-react';
import { useAuthStore } from '../../store/useAuthStore';
import { useTheme } from '../../hooks/useTheme';

export const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, logout } = useAuthStore();
  const { toggleTheme, isDark } = useTheme();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Analytics', path: '/analytics', icon: BarChart3 },
    { name: 'History', path: '/history', icon: History },
    { name: 'AI Copilot', path: '/assistant', icon: MessageSquareShare },
    { name: 'Settings', path: '/settings', icon: Settings },
  ];

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100">
      {/* Left Sidebar */}
      <aside className="w-64 glass flex flex-col justify-between border-r border-slate-200 dark:border-slate-800">
        <div>
          <div className="p-6 flex items-center gap-3 border-b border-slate-200 dark:border-slate-800">
            <div className="w-8 h-8 rounded bg-brand-500 flex items-center justify-center font-bold text-white shadow-lg shadow-brand-500/30">
              C
            </div>
            <div>
              <h1 className="font-bold text-lg leading-none">ChromaMind</h1>
              <span className="text-xs text-slate-400 dark:text-slate-500">Explainable AI</span>
            </div>
          </div>

          <nav className="p-4 space-y-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-brand-500 text-white shadow-lg shadow-brand-500/20'
                      : 'text-slate-500 hover:bg-slate-150 hover:text-slate-900 dark:text-slate-400 dark:hover:bg-slate-900 dark:hover:text-slate-100'
                  }`}
                >
                  <Icon size={18} />
                  {item.name}
                </Link>
              );
            })}
          </nav>
        </div>

        {/* User Info & Footer */}
        <div className="p-4 border-t border-slate-200 dark:border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-slate-200 dark:bg-slate-800 flex items-center justify-center font-semibold text-slate-800 dark:text-slate-200">
                SC
              </div>
              <div>
                <p className="text-xs font-semibold">{user?.fullName || 'Dr. Carter'}</p>
                <p className="text-[10px] text-slate-500 capitalize">{user?.role || 'Scientist'}</p>
              </div>
            </div>
            <button
              onClick={toggleTheme}
              className="p-2 hover:bg-slate-150 dark:hover:bg-slate-900 rounded-full text-slate-400 hover:text-slate-900 dark:hover:text-slate-100"
            >
              {isDark ? <Sun size={18} /> : <Moon size={18} />}
            </button>
          </div>
          <button
            onClick={handleLogout}
            className="w-full flex items-center justify-center gap-2 py-2 text-xs font-medium text-red-500 dark:text-red-400 hover:text-red-600 dark:hover:text-red-300 bg-red-500/10 hover:bg-red-500/20 dark:bg-red-950/20 dark:hover:bg-red-950/40 rounded-lg transition-colors border border-red-200/50 dark:border-red-900/30"
          >
            <LogOut size={14} />
            Sign Out
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Header */}
        <header className="h-16 glass flex items-center justify-between px-8 border-b border-slate-200 dark:border-slate-800">
          <div className="flex items-center gap-3">
            <span className="text-xs px-2 py-1 rounded bg-yellow-500/10 text-yellow-600 dark:text-yellow-500 border border-yellow-500/20 flex items-center gap-1">
              <ShieldAlert size={12} />
              API Connected
            </span>
          </div>
          <div className="text-xs text-slate-500 dark:text-slate-400">
            System status: <span className="text-green-500 dark:text-green-400 font-semibold">Active</span>
          </div>
        </header>

        {/* Dynamic page container */}
        <main className="flex-1 overflow-y-auto p-8 bg-slate-100/50 dark:bg-slate-950/50">
          {children}
        </main>
      </div>
    </div>
  );
};
