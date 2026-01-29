import { useState, useRef, useCallback } from 'react';
import { Upload, FileUp, FileSpreadsheet, AlertCircle, Loader2 } from 'lucide-react';
import { uploadAndAnalyze } from '../services/api';
import type { AnalysisData } from '../App';

interface FileUploadProps {
  currency: string;
  onCurrencyChange: (currency: string) => void;
  onAnalysisComplete: (data: AnalysisData) => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

const CURRENCIES = [
  { value: '£', label: '£ GBP' },
  { value: '$', label: '$ USD' },
  { value: '€', label: '€ EUR' },
  { value: 'A$', label: 'A$ AUD' },
  { value: 'C$', label: 'C$ CAD' },
];

export function FileUpload({
  currency,
  onCurrencyChange,
  onAnalysisComplete,
  isLoading,
  setIsLoading,
  setError,
}: FileUploadProps) {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleUpload = async (file: File) => {
    if (!file.name.match(/\.(xlsx|xls)$/i)) {
      setError('Please upload an Excel file (.xlsx or .xls)');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const result = await uploadAndAnalyze(file, currency);
      onAnalysisComplete(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to analyze file');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const file = e.dataTransfer.files[0];
    if (file) {
      handleUpload(file);
    }
  }, [currency]);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleUpload(file);
    }
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="glass-panel p-6 space-y-5">
      {/* Currency Selector */}
      <div>
        <label className="block text-sm font-medium text-white/60 mb-2">
          Currency
        </label>
        <select
          value={currency}
          onChange={(e) => onCurrencyChange(e.target.value)}
          disabled={isLoading}
          className="w-full px-4 py-2.5 bg-white/[0.03] border border-white/10 rounded-lg
                   text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50
                   focus:border-indigo-500/50 transition-all duration-200
                   disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {CURRENCIES.map((c) => (
            <option key={c.value} value={c.value} className="bg-surface-900 text-white">
              {c.label}
            </option>
          ))}
        </select>
      </div>

      {/* Drop Zone */}
      <div
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        onClick={() => !isLoading && fileInputRef.current?.click()}
        className={`
          relative border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer
          transition-all duration-300 overflow-hidden
          ${isDragging
            ? 'border-indigo-400 bg-indigo-500/10'
            : 'border-white/10 hover:border-indigo-500/50 hover:bg-white/[0.02]'
          }
          ${isLoading ? 'opacity-60 cursor-not-allowed' : ''}
        `}
      >
        {/* Gradient background on drag */}
        <div
          className={`absolute inset-0 bg-gradient-to-br from-indigo-500/20 via-violet-500/10 to-transparent
                    pointer-events-none transition-opacity duration-300
                    ${isDragging ? 'opacity-100' : 'opacity-0'}`}
        />

        <input
          ref={fileInputRef}
          type="file"
          accept=".xlsx,.xls"
          onChange={handleFileSelect}
          className="hidden"
          disabled={isLoading}
        />

        <div className="relative flex flex-col items-center gap-4">
          {isLoading ? (
            <>
              <div className="w-16 h-16 rounded-full bg-indigo-500/20 flex items-center justify-center">
                <Loader2 size={32} className="text-indigo-400 animate-spin" />
              </div>
              <div>
                <p className="text-lg font-medium text-white">Analyzing your data...</p>
                <p className="text-sm text-white/40 mt-1">This may take a moment</p>
              </div>
            </>
          ) : (
            <>
              <div
                className={`w-16 h-16 rounded-full flex items-center justify-center transition-all duration-300
                          ${isDragging
                            ? 'bg-indigo-500/30 scale-110'
                            : 'bg-white/[0.05]'
                          }`}
              >
                {isDragging ? (
                  <FileUp size={32} className="text-indigo-300" />
                ) : (
                  <Upload size={32} className="text-white/40" />
                )}
              </div>
              <div>
                <p className="text-lg font-medium text-white">
                  Drop your Xero P&L export here
                </p>
                <p className="text-sm text-white/40 mt-1">
                  or click to browse
                </p>
              </div>
              <div className="flex items-center gap-2 mt-2">
                <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white/[0.05] text-sm text-white/50">
                  <FileSpreadsheet size={16} />
                  .xlsx / .xls
                </span>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Help Text */}
      <div className="flex items-start gap-2 text-xs text-white/40">
        <AlertCircle size={14} className="flex-shrink-0 mt-0.5" />
        <p>
          Export from Xero: Reporting → Profit and Loss → Month by Month → Export to Excel
        </p>
      </div>
    </div>
  );
}
