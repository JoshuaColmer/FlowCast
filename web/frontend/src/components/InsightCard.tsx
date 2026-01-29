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
          iconBg: 'bg-emerald-500/20',
          iconColor: 'text-emerald-400',
          icon: <Sparkles className="w-4 h-4" />,
        };
      case 'negative':
        return {
          iconBg: 'bg-red-500/20',
          iconColor: 'text-red-400',
          icon: <AlertTriangle className="w-4 h-4" />,
        };
      default:
        return {
          iconBg: 'bg-indigo-500/20',
          iconColor: 'text-indigo-400',
          icon: <Lightbulb className="w-4 h-4" />,
        };
    }
  };

  const config = getConfig();

  return (
    <div className="glass-panel glass-panel-hover flex items-start gap-3 p-4">
      <div className={`flex-shrink-0 w-8 h-8 rounded-lg ${config.iconBg} ${config.iconColor} flex items-center justify-center`}>
        {config.icon}
      </div>
      <p className="text-sm text-white/70 leading-relaxed pt-1">{text}</p>
    </div>
  );
}
