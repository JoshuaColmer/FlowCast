import { useState } from 'react';
import { MetricCard } from './MetricCard';
import { InsightCard } from './InsightCard';
import { ChartPanel } from './ChartPanel';
import { downloadExport } from '../services/api';
import type { AnalysisData } from '../App';
import {
  TrendingUp,
  PieChart,
  Lightbulb,
  Download,
  FileSpreadsheet,
  Archive,
  Loader2,
  CheckCircle2,
  AlertTriangle,
  AlertCircle,
} from 'lucide-react';

interface DashboardProps {
  data: AnalysisData;
  currency: string;
}

export function Dashboard({ data, currency }: DashboardProps) {
  const [isExporting, setIsExporting] = useState<string | null>(null);

  const handleExport = async (format: 'excel' | 'zip') => {
    setIsExporting(format);
    try {
      const blob = await downloadExport(data.session_id, format);
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = format === 'excel' ? 'FlowCast_Report.xlsx' : 'FlowCast_Complete.zip';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Export failed:', err);
    } finally {
      setIsExporting(null);
    }
  };

  const getHealthIcon = (status: string) => {
    switch (status) {
      case 'green':
        return <CheckCircle2 className="w-5 h-5" />;
      case 'yellow':
        return <AlertTriangle className="w-5 h-5" />;
      case 'red':
        return <AlertCircle className="w-5 h-5" />;
      default:
        return <CheckCircle2 className="w-5 h-5" />;
    }
  };

  const getHealthColor = (status: string) => {
    switch (status) {
      case 'green':
        return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30';
      case 'yellow':
        return 'bg-amber-500/20 text-amber-400 border-amber-500/30';
      case 'red':
        return 'bg-red-500/20 text-red-400 border-red-500/30';
      default:
        return 'bg-surface-700 text-surface-300 border-surface-600';
    }
  };

  const { metrics, health_summary, insights, charts } = data;

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Company & Health Badge */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-white">{data.company}</h2>
          <p className="text-surface-400">Financial Health Analysis</p>
        </div>
        <div
          className={`inline-flex items-center gap-2 px-4 py-2 rounded-full border ${getHealthColor(
            health_summary.overall_status
          )}`}
        >
          {getHealthIcon(health_summary.overall_status)}
          <span className="font-semibold">{health_summary.overall}</span>
        </div>
      </div>

      {/* Key Metrics */}
      <section>
        <div className="flex items-center gap-2 mb-4">
          <TrendingUp className="w-5 h-5 text-primary-400" />
          <h3 className="text-lg font-semibold text-white">Key Metrics</h3>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard
            label="Gross Margin"
            value={metrics.gross_margin?.formatted || 'N/A'}
            status={metrics.gross_margin?.status || 'neutral'}
          />
          <MetricCard
            label="Operating Margin"
            value={metrics.operating_margin?.formatted || 'N/A'}
            status={metrics.operating_margin?.status || 'neutral'}
          />
          <MetricCard
            label="Revenue Trend"
            value={metrics.revenue_trend?.formatted || 'N/A'}
            status={metrics.revenue_trend?.status || 'neutral'}
          />
          <MetricCard
            label="Cost Control"
            value={metrics.cost_control?.formatted || 'N/A'}
            status={metrics.cost_control?.status || 'neutral'}
          />
        </div>

        {/* Secondary Metrics */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-4">
          <MetricCard
            label="Total Revenue"
            value={`${currency}${(metrics.total_revenue?.value || 0).toLocaleString()}`}
            status="neutral"
            icon="revenue"
          />
          <MetricCard
            label="Operating Profit"
            value={`${currency}${(metrics.total_profit?.value || 0).toLocaleString()}`}
            status={metrics.total_profit?.value >= 0 ? 'green' : 'red'}
            icon="profit"
          />
          <MetricCard
            label="Monthly Burn Rate"
            value={`${currency}${(metrics.monthly_burn_rate?.value || 0).toLocaleString()}`}
            status="neutral"
            icon="burn"
          />
          <MetricCard
            label="Largest Expense"
            value={metrics.largest_expense?.category || 'N/A'}
            subtitle={`${metrics.largest_expense?.percentage?.toFixed(0) || 0}% of costs`}
            status="neutral"
            icon="expense"
          />
        </div>
      </section>

      {/* Insights */}
      {insights && insights.length > 0 && (
        <section>
          <div className="flex items-center gap-2 mb-4">
            <Lightbulb className="w-5 h-5 text-amber-400" />
            <h3 className="text-lg font-semibold text-white">Key Insights</h3>
          </div>
          <div className="space-y-3">
            {insights.map((insight, index) => (
              <InsightCard key={index} type={insight.type} text={insight.text} />
            ))}
          </div>
        </section>
      )}

      {/* Charts */}
      <section>
        <div className="flex items-center gap-2 mb-4">
          <PieChart className="w-5 h-5 text-primary-400" />
          <h3 className="text-lg font-semibold text-white">Charts & Forecasts</h3>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <ChartPanel
            title="Revenue & Profit Trend"
            description="Dashed lines show 6-month forecast with confidence bands"
            imageBase64={charts.revenue_profit_trend}
          />
          <ChartPanel
            title="Operating Profit"
            imageBase64={charts.operating_profit}
          />
          <ChartPanel
            title="Cumulative Profit vs Expenses"
            imageBase64={charts.profit_expenses_trend}
          />
          <ChartPanel
            title="Cost Breakdown"
            imageBase64={charts.admin_costs_pie}
          />
        </div>
      </section>

      {/* Export Buttons */}
      <section>
        <div className="flex items-center gap-2 mb-4">
          <Download className="w-5 h-5 text-primary-400" />
          <h3 className="text-lg font-semibold text-white">Download Reports</h3>
        </div>
        <div className="flex flex-wrap gap-3">
          <button
            onClick={() => handleExport('excel')}
            disabled={isExporting !== null}
            className="inline-flex items-center gap-2 px-5 py-2.5 bg-primary-600 hover:bg-primary-500
                     text-white font-medium rounded-lg transition-all duration-200
                     disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isExporting === 'excel' ? (
              <Loader2 size={18} className="animate-spin" />
            ) : (
              <FileSpreadsheet size={18} />
            )}
            Excel Report
          </button>
          <button
            onClick={() => handleExport('zip')}
            disabled={isExporting !== null}
            className="inline-flex items-center gap-2 px-5 py-2.5 bg-surface-700 hover:bg-surface-600
                     text-surface-200 font-medium rounded-lg transition-all duration-200
                     disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isExporting === 'zip' ? (
              <Loader2 size={18} className="animate-spin" />
            ) : (
              <Archive size={18} />
            )}
            Everything (ZIP)
          </button>
        </div>
      </section>
    </div>
  );
}
