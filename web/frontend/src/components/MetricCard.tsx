import { TrendingUp, TrendingDown, DollarSign, Flame, Receipt, Minus } from 'lucide-react';

interface MetricCardProps {
  label: string;
  value: string;
  status: 'green' | 'yellow' | 'red' | 'neutral';
  subtitle?: string;
  icon?: 'revenue' | 'profit' | 'burn' | 'expense';
}

export function MetricCard({ label, value, status, subtitle, icon }: MetricCardProps) {
  const getStatusColor = () => {
    switch (status) {
      case 'green':
        return 'bg-emerald-500';
      case 'yellow':
        return 'bg-amber-500';
      case 'red':
        return 'bg-red-500';
      default:
        return 'bg-surface-500';
    }
  };

  const getIcon = () => {
    switch (icon) {
      case 'revenue':
        return <TrendingUp className="w-4 h-4 text-emerald-400" />;
      case 'profit':
        return <DollarSign className="w-4 h-4 text-primary-400" />;
      case 'burn':
        return <Flame className="w-4 h-4 text-orange-400" />;
      case 'expense':
        return <Receipt className="w-4 h-4 text-surface-400" />;
      default:
        return null;
    }
  };

  return (
    <div className="bg-surface-800 border border-surface-700 rounded-xl p-4 hover:border-surface-600 transition-all duration-200">
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs font-medium text-surface-400 uppercase tracking-wider">
          {label}
        </span>
        <div className="flex items-center gap-2">
          {getIcon()}
          <span className={`w-2.5 h-2.5 rounded-full ${getStatusColor()}`} />
        </div>
      </div>
      <div className="text-2xl font-bold text-white">{value}</div>
      {subtitle && (
        <div className="text-sm text-surface-400 mt-1">{subtitle}</div>
      )}
    </div>
  );
}
