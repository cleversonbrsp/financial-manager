import { LucideIcon } from 'lucide-react';
import { TrendingUp, TrendingDown } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: string;
  icon: LucideIcon;
  trend?: 'up' | 'down';
  color?: 'green' | 'red' | 'blue' | 'purple';
}

export default function StatCard({ title, value, icon: Icon, trend, color = 'purple' }: StatCardProps) {
  const colorClasses: Record<string, { gradient: string; bg: string; icon: string }> = {
    green: {
      gradient: 'from-green-500/20 to-emerald-500/20 border-green-500/30',
      bg: 'bg-green-500/20',
      icon: 'text-green-400',
    },
    red: {
      gradient: 'from-red-500/20 to-pink-500/20 border-red-500/30',
      bg: 'bg-red-500/20',
      icon: 'text-red-400',
    },
    blue: {
      gradient: 'from-blue-500/20 to-cyan-500/20 border-blue-500/30',
      bg: 'bg-blue-500/20',
      icon: 'text-blue-400',
    },
    purple: {
      gradient: 'from-purple-500/20 to-pink-500/20 border-purple-500/30',
      bg: 'bg-purple-500/20',
      icon: 'text-purple-400',
    },
  };

  const colors = colorClasses[color] || colorClasses.purple;

  return (
    <div className={`glass rounded-2xl p-6 bg-gradient-to-br ${colors.gradient} border card-hover glow-effect`}>
      <div className="flex items-center justify-between mb-4">
        <div className={`p-3 rounded-xl ${colors.bg}`}>
          <Icon className={colors.icon} size={24} />
        </div>
        {trend && (
          <div className={`flex items-center gap-1 ${trend === 'up' ? 'text-green-400' : 'text-red-400'}`}>
            {trend === 'up' ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
          </div>
        )}
      </div>
      <h3 className="text-gray-400 text-sm font-medium mb-1">{title}</h3>
      <p className="text-2xl font-bold text-white">{value}</p>
    </div>
  );
}
