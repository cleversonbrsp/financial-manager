import { ArrowUpRight, ArrowDownRight } from 'lucide-react';
import { formatCurrency, formatDate } from '../utils/formatters';

interface Transaction {
  id: number;
  type: string;
  description: string;
  amount: number;
  date: string;
  category: string;
}

interface RecentTransactionsProps {
  transactions: Transaction[];
}

export default function RecentTransactions({ transactions }: RecentTransactionsProps) {
  if (transactions.length === 0) {
    return <p className="text-gray-400 text-center py-8">Nenhuma transação recente</p>;
  }

  return (
    <div className="space-y-3">
      {transactions.map((transaction) => (
        <div
          key={transaction.id}
          className="glass rounded-lg p-4 flex items-center justify-between hover:bg-white/5 transition-all"
        >
          <div className="flex items-center gap-4">
            <div
              className={`p-2 rounded-lg ${
                transaction.type === 'income'
                  ? 'bg-green-500/20 text-green-400'
                  : 'bg-red-500/20 text-red-400'
              }`}
            >
              {transaction.type === 'income' ? (
                <ArrowUpRight size={20} />
              ) : (
                <ArrowDownRight size={20} />
              )}
            </div>
            <div>
              <p className="font-medium text-white">{transaction.description}</p>
              <p className="text-sm text-gray-400">
                {transaction.category} • {formatDate(transaction.date)}
              </p>
            </div>
          </div>
          <div className="text-right">
            <p
              className={`font-bold ${
                transaction.type === 'income' ? 'text-green-400' : 'text-red-400'
              }`}
            >
              {transaction.type === 'income' ? '+' : '-'}
              {formatCurrency(transaction.amount)}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}

