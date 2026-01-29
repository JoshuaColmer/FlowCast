import { useState } from 'react';
import { FileUpload } from './components/FileUpload';
import { Dashboard } from './components/Dashboard';
import { LandingPage } from './components/LandingPage';
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
    <div className="min-h-screen bg-surface-900">
      {/* Header */}
      <header className="border-b border-surface-700 bg-surface-800/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-primary-600 flex items-center justify-center">
                <BarChart3 className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">FlowCast</h1>
                <p className="text-xs text-surface-400">by Books & Balances</p>
              </div>
            </div>

            {analysisData && (
              <button
                onClick={handleReset}
                className="px-4 py-2 text-sm font-medium text-surface-300 hover:text-white
                         bg-surface-700/50 hover:bg-surface-700 rounded-lg transition-all duration-200"
              >
                New Analysis
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-6 p-4 bg-red-500/10 border border-red-500/20 rounded-xl">
            <p className="text-red-400 text-sm">{error}</p>
          </div>
        )}

        {!analysisData ? (
          <div className="space-y-8">
            {/* Hero Section */}
            <div className="text-center py-8">
              <span className="inline-block px-4 py-1.5 bg-primary-500/20 text-primary-400 text-xs font-semibold rounded-full uppercase tracking-wider mb-4">
                Financial Health Check
              </span>
              <h2 className="text-4xl font-bold text-white mb-3">
                Financial clarity in 60 seconds
              </h2>
              <p className="text-lg text-surface-400 max-w-2xl mx-auto">
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
      <footer className="border-t border-surface-700 py-6 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-sm text-surface-500">
            <span className="font-semibold text-surface-400">FlowCast</span> by{' '}
            <a
              href="https://www.booksandbalances.co.uk"
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary-400 hover:text-primary-300 transition-colors"
            >
              Books & Balances
            </a>
          </p>
          <p className="text-xs text-surface-600 mt-1">
            Financial clarity, delivered beautifully.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
