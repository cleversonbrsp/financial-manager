import { useEffect, useState } from 'react';
import { usersAPI, User } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { Plus, Edit, Trash2, CheckCircle, XCircle, Search } from 'lucide-react';
import UserModal from '../components/UserModal';

export default function Users() {
  const { user: currentUser } = useAuth();
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (currentUser?.role === 'admin') {
      loadUsers();
    }
  }, [currentUser]);

  const loadUsers = async () => {
    try {
      const response = await usersAPI.getAll();
      setUsers(response.data);
    } catch (error: any) {
      setError('Erro ao carregar usuários');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = () => {
    setSelectedUser(null);
    setShowModal(true);
  };

  const handleEdit = (user: User) => {
    setSelectedUser(user);
    setShowModal(true);
  };

  const handleDelete = async (userId: number) => {
    if (!confirm('Tem certeza que deseja deletar este usuário?')) {
      return;
    }

    try {
      await usersAPI.delete(userId);
      loadUsers();
    } catch (error: any) {
      alert('Erro ao deletar usuário: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleModalClose = () => {
    setShowModal(false);
    setSelectedUser(null);
    loadUsers();
  };

  if (currentUser?.role !== 'admin') {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <Shield className="mx-auto mb-4 text-red-500" size={48} />
          <h2 className="text-2xl font-bold text-white mb-2">Acesso Negado</h2>
          <p className="text-gray-400">Apenas administradores podem acessar esta página.</p>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-gradient mb-2">Gerenciamento de Usuários</h1>
          <p className="text-gray-400">Gerencie usuários e permissões do sistema</p>
        </div>
        <button
          onClick={handleCreate}
          className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg font-medium hover:shadow-lg hover:shadow-purple-500/50 transition-all flex items-center gap-2"
        >
          <Plus size={20} />
          Novo Usuário
        </button>
      </div>

      {error && (
        <div className="p-4 bg-red-500/20 border border-red-500/50 rounded-lg text-red-300">
          {error}
        </div>
      )}

      <div className="glass rounded-2xl p-6 card-hover">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-white/10">
                <th className="text-left py-4 px-4 text-gray-300 font-medium">ID</th>
                <th className="text-left py-4 px-4 text-gray-300 font-medium">Nome</th>
                <th className="text-left py-4 px-4 text-gray-300 font-medium">Email</th>
                <th className="text-left py-4 px-4 text-gray-300 font-medium">Username</th>
                <th className="text-left py-4 px-4 text-gray-300 font-medium">Role</th>
                <th className="text-left py-4 px-4 text-gray-300 font-medium">Status</th>
                <th className="text-left py-4 px-4 text-gray-300 font-medium">Ações</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.id} className="border-b border-white/5 hover:bg-white/5">
                  <td className="py-4 px-4 text-gray-300">{user.id}</td>
                  <td className="py-4 px-4 text-white">{user.full_name || '-'}</td>
                  <td className="py-4 px-4 text-gray-300">{user.email}</td>
                  <td className="py-4 px-4 text-gray-300">{user.username}</td>
                  <td className="py-4 px-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                      user.role === 'admin' 
                        ? 'bg-purple-500/20 text-purple-300' 
                        : 'bg-blue-500/20 text-blue-300'
                    }`}>
                      {user.role === 'admin' ? <Shield size={12} className="inline mr-1" /> : <UserIcon size={12} className="inline mr-1" />}
                      {user.role}
                    </span>
                  </td>
                  <td className="py-4 px-4">
                    {user.is_active ? (
                      <span className="px-3 py-1 rounded-full text-xs font-medium bg-green-500/20 text-green-300 flex items-center gap-1 w-fit">
                        <UserCheck size={12} />
                        Ativo
                      </span>
                    ) : (
                      <span className="px-3 py-1 rounded-full text-xs font-medium bg-red-500/20 text-red-300 flex items-center gap-1 w-fit">
                        <UserX size={12} />
                        Inativo
                      </span>
                    )}
                  </td>
                  <td className="py-4 px-4">
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handleEdit(user)}
                        className="p-2 hover:bg-white/10 rounded-lg transition-colors text-blue-400"
                        title="Editar"
                      >
                        <Edit size={18} />
                      </button>
                      {user.id !== currentUser?.id && (
                        <button
                          onClick={() => handleDelete(user.id)}
                          className="p-2 hover:bg-white/10 rounded-lg transition-colors text-red-400"
                          title="Deletar"
                        >
                          <Trash2 size={18} />
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {showModal && (
        <UserModal
          user={selectedUser}
          onClose={handleModalClose}
        />
      )}
    </div>
  );
}

