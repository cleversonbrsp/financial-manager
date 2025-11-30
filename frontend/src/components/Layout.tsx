import { Link, useLocation, useNavigate } from 'react-router-dom';
import { LayoutDashboard, Receipt, FileText, Upload, LogOut, User, Users } from 'lucide-react';
import { useState } from 'react';
import { uploadAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [uploading, setUploading] = useState(false);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    try {
      await uploadAPI.uploadExcel(file);
      alert('Planilha importada com sucesso!');
      window.location.reload();
    } catch (error) {
      console.error('Erro ao importar:', error);
      alert('Erro ao importar planilha. Verifique o formato.');
    } finally {
      setUploading(false);
      e.target.value = '';
    }
  };

  const navItems = [
    { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/transactions', icon: Receipt, label: 'Transações' },
    { path: '/reports', icon: FileText, label: 'Relatórios' },
    ...(user?.role === 'admin' ? [{ path: '/users', icon: Users, label: 'Usuários' }] : []),
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Sidebar */}
      <aside className="fixed left-0 top-0 h-screen w-64 glass-dark border-r border-white/10 p-6 z-50">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gradient">💰 Financial Manager</h1>
          <p className="text-sm text-gray-400 mt-1">Gestão Inteligente</p>
        </div>

        <nav className="space-y-2 mb-8">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                  isActive
                    ? 'bg-purple-600/30 text-white shadow-lg shadow-purple-500/20'
                    : 'text-gray-300 hover:bg-white/5 hover:text-white'
                }`}
              >
                <Icon size={20} />
                <span className="font-medium">{item.label}</span>
              </Link>
            );
          })}
        </nav>

        {/* Upload Button */}
        <div className="mt-auto space-y-2">
          <label
            className={`flex items-center gap-3 px-4 py-3 rounded-lg cursor-pointer transition-all text-gray-300 hover:bg-white/5 hover:text-white ${
              uploading ? 'opacity-50' : ''
            }`}
          >
            <Upload size={20} />
            <span className="font-medium">
              {uploading ? 'Importando...' : 'Importar Excel'}
            </span>
            <input
              type="file"
              accept=".xlsx,.xls"
              onChange={handleFileUpload}
              disabled={uploading}
              className="hidden"
            />
          </label>

          {/* User Info */}
          <div className="px-4 py-3 rounded-lg bg-white/5 border border-white/10">
            <div className="flex items-center gap-2 mb-2">
              <User size={16} className="text-purple-400" />
              <span className="text-sm text-gray-300 font-medium">
                {user?.full_name || user?.username || 'Usuário'}
              </span>
            </div>
            <p className="text-xs text-gray-400 truncate">{user?.email}</p>
          </div>

          {/* Logout Button */}
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all text-gray-300 hover:bg-red-500/20 hover:text-red-300"
          >
            <LogOut size={20} />
            <span className="font-medium">Sair</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="ml-64 p-8">
        <div className="max-w-7xl mx-auto">{children}</div>
      </main>
    </div>
  );
}

