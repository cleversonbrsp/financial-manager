import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authAPI } from '../services/api';

interface User {
  id: number;
  email: string;
  username: string;
  full_name?: string;
  is_active: boolean;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  refreshToken: string | null;
  login: (username: string, password: string) => Promise<void>;
  register: (email: string, username: string, password: string, fullName?: string) => Promise<void>;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('access_token'));
  const [refreshToken, setRefreshToken] = useState<string | null>(localStorage.getItem('refresh_token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Verificar se há token salvo e validar
    const savedToken = localStorage.getItem('access_token');
    const savedRefreshToken = localStorage.getItem('refresh_token');
    
    // Timeout de segurança para garantir que loading sempre termine
    const timeoutId = setTimeout(() => {
      setLoading(false);
    }, 5000); // 5 segundos máximo
    
    if (savedToken) {
      setToken(savedToken);
      setRefreshToken(savedRefreshToken);
      validateToken().finally(() => {
        clearTimeout(timeoutId);
      });
    } else {
      clearTimeout(timeoutId);
      setLoading(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const validateToken = async () => {
    const currentToken = token || localStorage.getItem('access_token');
    const currentRefreshToken = refreshToken || localStorage.getItem('refresh_token');
    
    if (!currentToken) {
      setLoading(false);
      return;
    }
    
    try {
      const response = await authAPI.getMe();
      setUser(response.data);
      setLoading(false);
    } catch (error: any) {
      console.log('Token inválido ou backend não disponível:', error?.message || error);
      // Token inválido, tentar refresh
      if (currentRefreshToken) {
        try {
          await refreshAccessToken();
          setLoading(false);
        } catch (refreshError: any) {
          console.log('Refresh falhou, limpando autenticação:', refreshError?.message || refreshError);
          // Refresh falhou, limpar tudo
          clearAuth();
          setLoading(false);
        }
      } else {
        console.log('Sem refresh token, limpando autenticação');
        clearAuth();
        setLoading(false);
      }
    }
  };

  const refreshAccessToken = async () => {
    if (!refreshToken) throw new Error('No refresh token');
    
    try {
      const response = await authAPI.refreshToken(refreshToken);
      setToken(response.data.access_token);
      setRefreshToken(response.data.refresh_token);
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('refresh_token', response.data.refresh_token);
      
      // Obter dados do usuário
      const userResponse = await authAPI.getMe();
      setUser(userResponse.data);
    } catch (error) {
      // Refresh falhou, limpar tudo
      clearAuth();
      throw error;
    }
  };

  const login = async (username: string, password: string) => {
    console.log('🔐 Iniciando login...');
    const response = await authAPI.login(username, password);
    console.log('✅ Login bem-sucedido, tokens recebidos');
    
    const accessToken = response.data.access_token;
    const refreshTokenValue = response.data.refresh_token;
    
    console.log('💾 Salvando tokens...', {
      accessToken: accessToken ? accessToken.substring(0, 20) + '...' : 'null',
      refreshToken: refreshTokenValue ? refreshTokenValue.substring(0, 20) + '...' : 'null'
    });
    
    // Salvar tokens primeiro
    setToken(accessToken);
    setRefreshToken(refreshTokenValue);
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshTokenValue);
    
    // Verificar se foi salvo
    const savedToken = localStorage.getItem('access_token');
    console.log('✅ Token salvo no localStorage:', savedToken ? savedToken.substring(0, 20) + '...' : 'null');
    
    // Obter dados do usuário passando o token diretamente
    try {
      console.log('👤 Obtendo dados do usuário...');
      const userResponse = await authAPI.getMe(accessToken);
      console.log('✅ Dados do usuário obtidos:', userResponse.data);
      setUser(userResponse.data);
    } catch (error: any) {
      console.error('❌ Erro ao obter dados do usuário após login:', error);
      console.error('Resposta completa:', error?.response?.data);
      console.error('Status:', error?.response?.status);
      // Se falhar, limpar tokens e relançar erro
      clearAuth();
      throw error;
    }
  };

  const register = async (email: string, username: string, password: string, fullName?: string) => {
    await authAPI.register(email, username, password, fullName);
    // Após registro, fazer login automaticamente
    await login(username, password);
  };

  const logout = async () => {
    if (refreshToken) {
      try {
        await authAPI.logout(refreshToken);
      } catch (error) {
        console.error('Erro ao fazer logout:', error);
      }
    }
    clearAuth();
  };

  const clearAuth = () => {
    setUser(null);
    setToken(null);
    setRefreshToken(null);
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        refreshToken,
        login,
        register,
        logout,
        isAuthenticated: !!user && !!token,
        loading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

