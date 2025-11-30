import { useEffect, useState } from 'react';
import { dashboardAPI, DashboardStats } from '../services/api';
import StatCard from '../components/StatCard';
import { TrendingUp, TrendingDown, DollarSign, Activity } from 'lucide-react';
import MonthlyTrendChart from '../components/charts/MonthlyTrendChart';
import CategoryPieChart from '../components/charts/CategoryPieChart';
import RecentTransactions from '../components/RecentTransactions';
import HourlyCalculation from '../components/HourlyCalculation';
import { formatCurrency } from '../utils/formatters';

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const response = await dashboardAPI.getStats();
      setStats(response.data);
    } catch (error) {
      console.error('Erro ao carregar estatísticas:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  if (!stats) {
    return <div className="text-center text-gray-400">Erro ao carregar dados</div>;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gradient mb-2">Dashboard Financeiro</h1>
        <p className="text-gray-400">Visão geral das suas finanças</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Receitas"
          value={formatCurrency(stats.total_income)}
          icon={TrendingUp}
          trend="up"
          color="green"
        />
        <StatCard
          title="Despesas"
          value={formatCurrency(stats.total_expense)}
          icon={TrendingDown}
          trend="down"
          color="red"
        />
        <StatCard
          title="Saldo Total"
          value={formatCurrency(stats.balance)}
          icon={DollarSign}
          trend={stats.balance >= 0 ? 'up' : 'down'}
          color={stats.balance >= 0 ? 'green' : 'red'}
        />
        <StatCard
          title="Saldo Mensal"
          value={formatCurrency(stats.monthly_balance)}
          icon={DollarSign}
          trend={stats.monthly_balance >= 0 ? 'up' : 'down'}
          color={stats.monthly_balance >= 0 ? 'green' : 'red'}
        />
      </div>

      {/* New Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard
          title="Gastos Fixos"
          value={formatCurrency(stats.fixed_expenses)}
          icon={Activity}
          color="red"
        />
        <StatCard
          title="Gastos Esporádicos"
          value={formatCurrency(stats.sporadic_expenses)}
          icon={Activity}
          color="blue"
        />
        <StatCard
          title="Investimentos"
          value={formatCurrency(stats.investments)}
          icon={TrendingUp}
          color="purple"
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass rounded-2xl p-6 card-hover">
          <h2 className="text-xl font-bold mb-4 text-white">Tendência Mensal</h2>
          <MonthlyTrendChart data={stats.monthly_trend} />
        </div>

        <div className="glass rounded-2xl p-6 card-hover">
          <h2 className="text-xl font-bold mb-4 text-white">Despesas por Categoria</h2>
          <CategoryPieChart data={stats.expense_by_category} />
        </div>
      </div>

      {/* Hourly Calculation - Cálculo de Valores por Hora/Dia/Semana */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-white mb-4">💰 Cálculo de Valores por Hora</h2>
        <HourlyCalculation />
      </div>

      {/* Recent Transactions */}
      <div className="glass rounded-2xl p-6 card-hover">
        <h2 className="text-xl font-bold mb-4 text-white">Transações Recentes</h2>
        <RecentTransactions transactions={stats.recent_transactions} />
      </div>
    </div>
  );
}

