import { Sparkles, AlertTriangle, Lightbulb } from 'lucide-react';

interface InsightCardProps {
  type: string;
  text: string;
}

export function InsightCard({ type, text }: InsightCardProps) {
  const getConfig = () => {
    switch (type) {
      case 'positive':
        return {
          bg: 'bg-emerald-500/10',
          border: 'border-emerald-500/20',
          accent: 'border-l-emerald-500',
          icon: <Sparkles className="w-5 h-5 text-emerald-400" />,
        };
      case 'negative':
        return {
          bg: 'bg-red-500/10',
          border: 'border-red-500/20',
          accent: 'border-l-red-500',
          icon: <AlertTriangle className="w-5 h-5 text-red-400" />,
        };
      default:
        return {
          bg: 'bg-primary-500/10',
          border: 'border-primary-500/20',
          accent: 'border-l-primary-500',
          icon: <Lightbulb className="w-5 h-5 text-primary-400" />,
        };
    }
  };

  const config = getConfig();

  return (
    <div
      className={`flex items-start gap-3 p-4 rounded-xl border-l-4 ${config.bg} ${config.border} ${config.accent}`}
    >
      <div className="flex-shrink-0 mt-0.5">{config.icon}</div>
      <p className="text-sm text-surface-200 leading-relaxed">{text}</p>
    </div>
  );
}
