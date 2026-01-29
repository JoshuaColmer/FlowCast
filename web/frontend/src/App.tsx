import { useState } from 'react';
import { FileUpload } from './components/FileUpload';
import { Dashboard } from './components/Dashboard';
import { LandingPage } from './components/LandingPage';
import { AnimatedBackground } from './components/AnimatedBackground';
import { BarChart3 } from 'lucide-react';

export interface AnalysisData {
  session_id: string;
  company: string;
  metrics: Record<string, any>;
  health_summary: Record<string, any>;
  insights: Array<{ type: string; text: string }>;
  forecast: Record<string, any>;
  charts: Record<string, string>;
}

function App() {
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null);
  const [currency, setCurrency] = useState('£');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalysisComplete = (data: AnalysisData) => {
    setAnalysisData(data);
    setError(null);
  };

  const handleReset = () => {
    setAnalysisData(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-surface-950 relative">
      {/* Animated Background Orbs */}
      <AnimatedBackground />

      {/* Header */}
      <header className="glass-panel sticky top-0 z-50 border-x-0 border-t-0 rounded-none">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              {/* Logo with gradient glow */}
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-br from-indigo-500 to-violet-500 rounded-xl blur-md opacity-50" />
                <div className="relative w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-500 flex items-center justify-center shadow-glow-primary">
                  <BarChart3 className="w-6 h-6 text-white" />
                </div>
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">FlowCast</h1>
                <p className="text-xs text-white/40">by Books & Balances</p>
              </div>
            </div>

            {analysisData && (
              <button
                onClick={handleReset}
                className="btn-glass px-4 py-2 text-sm font-medium text-white/70 hover:text-white rounded-lg"
              >
                New Analysis
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-6 p-4 glass-panel bg-red-500/10 border-red-500/20">
            <p className="text-red-400 text-sm">{error}</p>
          </div>
        )}

        {!analysisData ? (
          <div className="space-y-8">
            {/* Hero Section */}
            <div className="text-center py-8">
              <span className="inline-block px-4 py-1.5 glass-panel text-indigo-400 text-xs font-semibold uppercase tracking-wider mb-4">
                Financial Health Check
              </span>
              <h2 className="text-4xl sm:text-5xl font-bold text-white mb-3">
                Financial clarity in{' '}
                <span className="gradient-text">60 seconds</span>
              </h2>
              <p className="text-lg text-white/50 max-w-2xl mx-auto">
                Upload your Xero P&L export, get instant insights and forecasts
              </p>
            </div>

            {/* File Upload */}
            <div className="max-w-xl mx-auto">
              <FileUpload
                currency={currency}
                onCurrencyChange={setCurrency}
                onAnalysisComplete={handleAnalysisComplete}
                isLoading={isLoading}
                setIsLoading={setIsLoading}
                setError={setError}
              />
            </div>

            {/* Landing Page Features */}
            <LandingPage />
          </div>
        ) : (
          <Dashboard
            data={analysisData}
            currency={currency}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="relative z-10 border-t border-white/5 py-6 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-sm text-white/40">
            <span className="font-semibold text-white/60">FlowCast</span> by{' '}
            <a
              href="https://www.booksandbalances.co.uk"
              target="_blank"
              rel="noopener noreferrer"
              className="text-indigo-400 hover:text-indigo-300 transition-colors"
            >
              Books & Balances
            </a>
          </p>
          <p className="text-xs text-white/30 mt-1">
            Financial clarity, delivered beautifully.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
