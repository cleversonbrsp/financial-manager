import { useState } from 'react';
import { reportsAPI } from '../services/api';
import { FileText, Download, Calendar } from 'lucide-react';

export default function Reports() {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [generating, setGenerating] = useState(false);

  const handleGenerateReport = async (format: 'pdf' | 'excel') => {
    if (!startDate || !endDate) {
      alert('Por favor, selecione as datas inicial e final');
      return;
    }

    setGenerating(true);
    try {
      const params = {
        start_date: startDate,
        end_date: endDate,
      };

      const response = await reportsAPI[format === 'pdf' ? 'generatePDF' : 'generateExcel'](params);
      
      // Criar URL do blob e fazer download
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `relatorio_financeiro.${format === 'pdf' ? 'pdf' : 'xlsx'}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Erro ao gerar relatório:', error);
      alert('Erro ao gerar relatório');
    } finally {
      setGenerating(false);
    }
  };

  // Definir data padrão (último mês)
  const today = new Date();
  const lastMonth = new Date(today.getFullYear(), today.getMonth() - 1, 1);
  const defaultStartDate = lastMonth.toISOString().split('T')[0];
  const defaultEndDate = today.toISOString().split('T')[0];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gradient mb-2">Relatórios</h1>
        <p className="text-gray-400">Gere relatórios detalhados em PDF ou Excel</p>
      </div>

      {/* Report Generator Card */}
      <div className="glass rounded-2xl p-8 max-w-2xl">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-3 bg-purple-500/20 rounded-lg">
            <FileText className="text-purple-400" size={24} />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white">Gerar Relatório</h2>
            <p className="text-sm text-gray-400">Selecione o período e formato</p>
          </div>
        </div>

        {/* Date Range */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              <Calendar size={16} className="inline mr-2" />
              Data Inicial
            </label>
            <input
              type="date"
              value={startDate || defaultStartDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:border-purple-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              <Calendar size={16} className="inline mr-2" />
              Data Final
            </label>
            <input
              type="date"
              value={endDate || defaultEndDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:border-purple-500"
            />
          </div>
        </div>

        {/* Format Selection */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-300 mb-4">Formato do Relatório</label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* PDF Card */}
            <button
              onClick={() => handleGenerateReport('pdf')}
              disabled={generating}
              className="glass-dark rounded-xl p-6 hover:bg-white/5 transition-all text-left group"
            >
              <div className="flex items-center gap-4 mb-3">
                <div className="p-3 bg-red-500/20 rounded-lg group-hover:scale-110 transition-transform">
                  <FileText className="text-red-400" size={24} />
                </div>
                <div>
                  <h3 className="font-bold text-white">PDF</h3>
                  <p className="text-xs text-gray-400">Formato de impressão</p>
                </div>
              </div>
              <p className="text-sm text-gray-400">
                Relatório formatado e profissional, ideal para impressão e compartilhamento.
              </p>
            </button>

            {/* Excel Card */}
            <button
              onClick={() => handleGenerateReport('excel')}
              disabled={generating}
              className="glass-dark rounded-xl p-6 hover:bg-white/5 transition-all text-left group"
            >
              <div className="flex items-center gap-4 mb-3">
                <div className="p-3 bg-green-500/20 rounded-lg group-hover:scale-110 transition-transform">
                  <Download className="text-green-400" size={24} />
                </div>
                <div>
                  <h3 className="font-bold text-white">Excel</h3>
                  <p className="text-xs text-gray-400">Planilha editável</p>
                </div>
              </div>
              <p className="text-sm text-gray-400">
                Dados estruturados em planilha, perfeito para análise e manipulação adicional.
              </p>
            </button>
          </div>
        </div>

        {generating && (
          <div className="text-center py-4">
            <div className="inline-flex items-center gap-2 text-purple-400">
              <div className="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-purple-500"></div>
              Gerando relatório...
            </div>
          </div>
        )}
      </div>

      {/* Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass rounded-xl p-6">
          <h3 className="font-bold text-white mb-2">📊 Dados Completos</h3>
          <p className="text-sm text-gray-400">
            Todos os dados financeiros do período selecionado incluídos no relatório.
          </p>
        </div>
        <div className="glass rounded-xl p-6">
          <h3 className="font-bold text-white mb-2">💼 Profissional</h3>
          <p className="text-sm text-gray-400">
            Formatação profissional adequada para apresentações e documentos.
          </p>
        </div>
        <div className="glass rounded-xl p-6">
          <h3 className="font-bold text-white mb-2">⚡ Rápido</h3>
          <p className="text-sm text-gray-400">
            Geração instantânea de relatórios com todos os dados consolidados.
          </p>
        </div>
      </div>
    </div>
  );
}

