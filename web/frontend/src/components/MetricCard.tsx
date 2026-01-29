import { TrendingUp, DollarSign, Flame, Receipt } from 'lucide-react';

interface MetricCardProps {
  label: string;
  value: string;
  status: 'green' | 'yellow' | 'red' | 'neutral';
  subtitle?: string;
  icon?: 'revenue' | 'profit' | 'burn' | 'expense';
}

export function MetricCard({ label, value, status, subtitle, icon }: MetricCardProps) {
  const getStatusStyles = () => {
    switch (status) {
      case 'green':
        return {
          dot: 'bg-emerald-500',
          glow: 'shadow-glow-green',
        };
      case 'yellow':
        return {
          dot: 'bg-amber-500',
          glow: 'shadow-glow-yellow',
        };
      case 'red':
        return {
          dot: 'bg-red-500',
          glow: 'shadow-glow-red',
        };
      default:
        return {
          dot: 'bg-white/30',
          glow: '',
        };
    }
  };

  const getIconConfig = () => {
    switch (icon) {
      case 'revenue':
        return {
          component: <TrendingUp className="w-4 h-4 text-emerald-400" />,
          bg: 'bg-emerald-500/20',
        };
      case 'profit':
        return {
          component: <DollarSign className="w-4 h-4 text-indigo-400" />,
          bg: 'bg-indigo-500/20',
        };
      case 'burn':
        return {
          component: <Flame className="w-4 h-4 text-orange-400" />,
          bg: 'bg-orange-500/20',
        };
      case 'expense':
        return {
          component: <Receipt className="w-4 h-4 text-white/60" />,
          bg: 'bg-white/10',
        };
      default:
        return null;
    }
  };

  const statusStyles = getStatusStyles();
  const iconConfig = getIconConfig();

  return (
    <div className="glass-card p-4 group">
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs font-medium text-white/50 uppercase tracking-wider">
          {label}
        </span>
        <div className="flex items-center gap-2">
          {iconConfig && (
            <div className={`w-6 h-6 rounded-md ${iconConfig.bg} flex items-center justify-center`}>
              {iconConfig.component}
            </div>
          )}
          <span
            className={`w-2.5 h-2.5 rounded-full ${statusStyles.dot} ${statusStyles.glow}`}
          />
        </div>
      </div>
      <div className="text-2xl font-bold text-white">{value}</div>
      {subtitle && (
        <div className="text-sm text-white/40 mt-1">{subtitle}</div>
      )}
    </div>
  );
}
