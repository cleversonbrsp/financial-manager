import { useState } from 'react';
import { dashboardAPI, HourlyCalculationResponse } from '../services/api';
import { Calculator, DollarSign, Clock, Calendar, TrendingUp } from 'lucide-react';
import { formatCurrency } from '../utils/formatters';

export default function HourlyCalculation() {
  const [month, setMonth] = useState(new Date().getMonth() + 1);
  const [year, setYear] = useState(new Date().getFullYear());
  const [daysWorked, setDaysWorked] = useState(22);
  const [hoursPerDay, setHoursPerDay] = useState(8);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<HourlyCalculationResponse | null>(null);

  const handleCalculate = async () => {
    setLoading(true);
    try {
      const response = await dashboardAPI.calculateHourly({
        month,
        year,
        days_worked: daysWorked,
        hours_per_day: hoursPerDay,
      });
      setResult(response.data);
    } catch (error) {
      console.error('Erro ao calcular:', error);
      alert('Erro ao calcular valores. Verifique se há receitas cadastradas no mês selecionado.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass rounded-2xl p-6 card-hover border-2 border-purple-500/30">
      <div className="flex items-center gap-3 mb-6">
        <Calculator className="text-purple-400" size={28} />
        <h2 className="text-2xl font-bold text-white bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
          💰 Cálculo de Valores por Hora/Dia/Semana
        </h2>
      </div>
      
      <p className="text-gray-400 mb-6 text-sm">
        Preencha os campos abaixo e clique em "Calcular Valores" para ver:
        <br />💵 Valor por Hora • 💸 Valor por Dia • 💼 Valor por Semana
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Mês</label>
          <select
            value={month}
            onChange={(e) => setMonth(Number(e.target.value))}
            className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:border-purple-500"
          >
            {Array.from({ length: 12 }, (_, i) => i + 1).map((m) => (
              <option key={m} value={m}>
                {new Date(2000, m - 1).toLocaleString('pt-BR', { month: 'long' })}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Ano</label>
          <input
            type="number"
            value={year}
            onChange={(e) => setYear(Number(e.target.value))}
            className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:border-purple-500"
            min="2020"
            max="2100"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Dias Trabalhados</label>
          <input
            type="number"
            value={daysWorked}
            onChange={(e) => setDaysWorked(Number(e.target.value))}
            className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:border-purple-500"
            min="1"
            max="31"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Horas por Dia</label>
          <input
            type="number"
            value={hoursPerDay}
            onChange={(e) => setHoursPerDay(Number(e.target.value))}
            className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:border-purple-500"
            min="1"
            max="24"
            step="0.5"
          />
        </div>
      </div>

      <button
        onClick={handleCalculate}
        disabled={loading}
        className="w-full px-4 py-3 bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg font-medium hover:shadow-lg hover:shadow-purple-500/50 transition-all disabled:opacity-50 mb-6"
      >
        {loading ? 'Calculando...' : 'Calcular Valores'}
      </button>

      {result && (
        <div className="space-y-4">
          <div className="p-4 bg-white/5 rounded-lg border border-white/10">
            <div className="flex items-center gap-2 mb-2">
              <Calendar className="text-green-400" size={20} />
              <span className="text-sm text-gray-400">Mês de Referência</span>
            </div>
            <p className="text-2xl font-bold text-white">{result.month}</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 bg-white/5 rounded-lg border border-white/10">
              <div className="flex items-center gap-2 mb-2">
                <DollarSign className="text-green-400" size={20} />
                <span className="text-sm text-gray-400">Valor Total Recebido</span>
              </div>
              <p className="text-2xl font-bold text-white">{formatCurrency(result.total_received)}</p>
            </div>

            <div className="p-4 bg-white/5 rounded-lg border border-white/10">
              <div className="flex items-center gap-2 mb-2">
                <Calendar className="text-blue-400" size={20} />
                <span className="text-sm text-gray-400">Dias Trabalhados</span>
              </div>
              <p className="text-2xl font-bold text-white">{result.days_worked} dias</p>
            </div>

            <div className="p-4 bg-white/5 rounded-lg border border-white/10">
              <div className="flex items-center gap-2 mb-2">
                <Clock className="text-purple-400" size={20} />
                <span className="text-sm text-gray-400">Horas por Dia</span>
              </div>
              <p className="text-2xl font-bold text-white">{result.hours_per_day}h</p>
            </div>

            <div className="p-4 bg-white/5 rounded-lg border border-white/10">
              <div className="flex items-center gap-2 mb-2">
                <Clock className="text-orange-400" size={20} />
                <span className="text-sm text-gray-400">Total de Horas</span>
              </div>
              <p className="text-2xl font-bold text-white">{result.total_hours.toFixed(1)}h</p>
            </div>

            <div className="p-4 bg-gradient-to-br from-purple-600/20 to-pink-600/20 rounded-lg border border-purple-500/30">
              <div className="flex items-center gap-2 mb-2">
                <TrendingUp className="text-purple-300" size={20} />
                <span className="text-sm text-gray-300">Valor por Hora</span>
              </div>
              <p className="text-3xl font-bold text-white">{formatCurrency(result.value_per_hour)}</p>
            </div>

            <div className="p-4 bg-gradient-to-br from-blue-600/20 to-cyan-600/20 rounded-lg border border-blue-500/30">
              <div className="flex items-center gap-2 mb-2">
                <DollarSign className="text-blue-300" size={20} />
                <span className="text-sm text-gray-300">Valor por Dia</span>
              </div>
              <p className="text-3xl font-bold text-white">{formatCurrency(result.value_per_day)}</p>
            </div>

            <div className="p-4 bg-gradient-to-br from-green-600/20 to-emerald-600/20 rounded-lg border border-green-500/30">
              <div className="flex items-center gap-2 mb-2">
                <Calendar className="text-green-300" size={20} />
                <span className="text-sm text-gray-300">Valor por Semana</span>
              </div>
              <p className="text-3xl font-bold text-white">{formatCurrency(result.value_per_week)}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

