import axios from 'axios';

const api = axios.create({
  baseURL: (import.meta.env?.VITE_API_URL as string) || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para refresh token
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    // Se não houver resposta (backend offline), não tentar refresh
    if (!error.response) {
      console.log('Backend não disponível:', error.message);
      return Promise.reject(error);
    }
    
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const apiUrl = (import.meta.env?.VITE_API_URL as string) || '/api';
          const response = await axios.post(`${apiUrl}/auth/refresh`, {
            refresh_token: refreshToken,
          });
          
          const { access_token, refresh_token: newRefreshToken } = response.data;
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', newRefreshToken);
          
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return api(originalRequest);
        } catch (refreshError) {
          // Refresh falhou, redirecionar para login apenas se não for erro de conexão
          if (refreshError && (refreshError as any).response) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.href = '/login';
          }
          return Promise.reject(refreshError);
        }
      }
    }
    
    return Promise.reject(error);
  }
);

export interface Transaction {
  id: number;
  type: 'expense' | 'income';
  subtype?: 'fixed' | 'sporadic' | 'investment' | 'received' | null;
  description: string;
  amount: number;
  date: string;
  category: string;
  notes?: string;
  created_at: string;
  updated_at?: string;
}

export interface DashboardStats {
  total_income: number;
  total_expense: number;
  balance: number;
  expense_by_category: Record<string, number>;
  income_by_category: Record<string, number>;
  monthly_trend: Array<{
    month: string;
    income: number;
    expense: number;
  }>;
  recent_transactions: Array<{
    id: number;
    type: string;
    description: string;
    amount: number;
    date: string;
    category: string;
  }>;
  fixed_expenses: number;
  sporadic_expenses: number;
  investments: number;
  monthly_balance: number;
}

export interface HourlyCalculationRequest {
  month: number;
  year: number;
  days_worked: number;
  hours_per_day: number;
}

export interface HourlyCalculationResponse {
  total_received: number;
  days_worked: number;
  hours_per_day: number;
  total_hours: number;
  value_per_hour: number;
  value_per_day: number;
  value_per_week: number;
  month: string;
}

export const transactionsAPI = {
  getAll: (params?: any) => api.get<Transaction[]>('/transactions/', { params }),
  getById: (id: number) => api.get<Transaction>(`/transactions/${id}`),
  create: (data: Partial<Transaction>) => api.post<Transaction>('/transactions/', data),
  update: (id: number, data: Partial<Transaction>) => api.put<Transaction>(`/transactions/${id}`, data),
  delete: (id: number) => api.delete(`/transactions/${id}`),
};

export const dashboardAPI = {
  getStats: (startDate?: string, endDate?: string) => 
    api.get<DashboardStats>('/dashboard/stats', { params: { start_date: startDate, end_date: endDate } }),
  calculateHourly: (data: HourlyCalculationRequest) =>
    api.post<HourlyCalculationResponse>('/dashboard/hourly-calculation', data),
};

export const uploadAPI = {
  uploadExcel: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/upload/excel', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
};

export const reportsAPI = {
  generatePDF: (params?: any) => 
    api.get('/reports/pdf', { params, responseType: 'blob' }),
  generateExcel: (params?: any) => 
    api.get('/reports/excel', { params, responseType: 'blob' }),
};

export const authAPI = {
  login: (username: string, password: string) => {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);
    return api.post('/auth/login', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
  },
  refreshToken: (refreshToken: string) =>
    api.post('/auth/refresh', { refresh_token: refreshToken }),
  logout: (refreshToken: string) =>
    api.post('/auth/logout', { refresh_token: refreshToken }),
  getMe: (token?: string) => {
    // Se token for fornecido, usar diretamente
    if (token) {
      return api.get('/auth/me', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
    }
    return api.get('/auth/me');
  },
};

export interface User {
  id: number;
  email: string;
  username: string;
  full_name?: string;
  role: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
}

export const usersAPI = {
  getAll: () => api.get<User[]>('/users/'),
  getById: (id: number) => api.get<User>(`/users/${id}`),
  create: (data: Partial<User> & { password: string }) => api.post<User>('/users/', data),
  update: (id: number, data: Partial<User> & { password?: string }) => api.put<User>(`/users/${id}`, data),
  delete: (id: number) => api.delete(`/users/${id}`),
};

export default api;
