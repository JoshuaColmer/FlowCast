import {
  Upload,
  BarChart3,
  Sparkles,
  Target,
  TrendingUp,
  Lightbulb,
  Download,
  Zap,
} from 'lucide-react';

interface FeatureCardProps {
  icon: React.ReactNode;
  iconBg: string;
  title: string;
  description: string;
}

function FeatureCard({ icon, iconBg, title, description }: FeatureCardProps) {
  return (
    <div className="glass-card p-6 group">
      <div className={`w-12 h-12 rounded-xl ${iconBg} flex items-center justify-center mb-4 transition-transform duration-300 group-hover:scale-110`}>
        {icon}
      </div>
      <h3 className="text-lg font-semibold text-white mb-2">{title}</h3>
      <p className="text-sm text-white/50 leading-relaxed">{description}</p>
    </div>
  );
}

export function LandingPage() {
  return (
    <div className="space-y-12 mt-8">
      {/* How It Works */}
      <section>
        <h3 className="text-xl font-bold text-white mb-6 text-center">How It Works</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <FeatureCard
            icon={<Upload className="w-6 h-6 text-indigo-400" />}
            iconBg="bg-indigo-500/20"
            title="1. Export from Xero"
            description="Go to Reporting → Profit and Loss → Month by Month → Export to Excel"
          />
          <FeatureCard
            icon={<Zap className="w-6 h-6 text-violet-400" />}
            iconBg="bg-violet-500/20"
            title="2. Upload Here"
            description="Drag and drop your Excel file above. We'll analyse it instantly."
          />
          <FeatureCard
            icon={<BarChart3 className="w-6 h-6 text-cyan-400" />}
            iconBg="bg-cyan-500/20"
            title="3. Get Insights"
            description="See your financial health, forecasts, and download beautiful reports."
          />
        </div>
      </section>

      {/* What You Get */}
      <section>
        <h3 className="text-xl font-bold text-white mb-6 text-center">What You Get</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <FeatureCard
            icon={<Target className="w-6 h-6 text-emerald-400" />}
            iconBg="bg-emerald-500/20"
            title="Health Metrics"
            description="Gross margin, operating margin, revenue trends, and cost control indicators with traffic light status."
          />
          <FeatureCard
            icon={<TrendingUp className="w-6 h-6 text-blue-400" />}
            iconBg="bg-blue-500/20"
            title="6-Month Forecast"
            description="AI-powered projections with confidence bands. See where your business is heading."
          />
          <FeatureCard
            icon={<Lightbulb className="w-6 h-6 text-amber-400" />}
            iconBg="bg-amber-500/20"
            title="Smart Insights"
            description="Automated analysis that surfaces what matters. No more guessing, just clarity."
          />
          <FeatureCard
            icon={<Download className="w-6 h-6 text-purple-400" />}
            iconBg="bg-purple-500/20"
            title="Export Anywhere"
            description="Download as PNG charts, Excel workbook, PDF report, or PowerPoint deck."
          />
        </div>
      </section>

      {/* Pro Tip */}
      <section className="glass-panel p-6 text-center">
        <div className="w-12 h-12 rounded-xl bg-indigo-500/20 flex items-center justify-center mx-auto mb-4">
          <Sparkles className="w-6 h-6 text-indigo-400" />
        </div>
        <h4 className="text-lg font-semibold text-white mb-2">Pro Tip</h4>
        <p className="text-white/50 max-w-xl mx-auto">
          The more months of data you provide, the more accurate your forecast will be.
          We recommend at least 6 months of historical data for best results.
        </p>
      </section>
    </div>
  );
}
