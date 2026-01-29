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
    <div className="space-y-4">
      {/* Currency Selector */}
      <div>
        <label className="block text-sm font-medium text-surface-300 mb-2">
          Currency
        </label>
        <select
          value={currency}
          onChange={(e) => onCurrencyChange(e.target.value)}
          disabled={isLoading}
          className="w-full px-4 py-2.5 bg-surface-800 border border-surface-600 rounded-lg
                   text-surface-200 focus:outline-none focus:ring-2 focus:ring-primary-500/50
                   focus:border-primary-500 transition-all duration-200"
        >
          {CURRENCIES.map((c) => (
            <option key={c.value} value={c.value}>
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
          transition-all duration-200 overflow-hidden
          ${isDragging
            ? 'border-primary-400 bg-primary-500/10 shadow-lg shadow-primary-500/20'
            : 'border-surface-600 hover:border-primary-500/60 hover:bg-surface-800/50'
          }
          ${isLoading ? 'opacity-60 cursor-not-allowed' : ''}
        `}
      >
        {/* Gradient background on drag */}
        <div
          className={`absolute inset-0 bg-gradient-to-br from-primary-500/10 to-transparent
                    pointer-events-none transition-opacity duration-200
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
              <div className="w-16 h-16 rounded-full bg-primary-500/20 flex items-center justify-center">
                <Loader2 size={32} className="text-primary-400 animate-spin" />
              </div>
              <div>
                <p className="text-lg font-medium text-surface-200">Analyzing your data...</p>
                <p className="text-sm text-surface-400 mt-1">This may take a moment</p>
              </div>
            </>
          ) : (
            <>
              <div
                className={`w-16 h-16 rounded-full flex items-center justify-center transition-all duration-200
                          ${isDragging ? 'bg-primary-500/30 scale-110' : 'bg-surface-700'}`}
              >
                {isDragging ? (
                  <FileUp size={32} className="text-primary-300" />
                ) : (
                  <Upload size={32} className="text-surface-400" />
                )}
              </div>
              <div>
                <p className="text-lg font-medium text-surface-200">
                  Drop your Xero P&L export here
                </p>
                <p className="text-sm text-surface-400 mt-1">
                  or click to browse
                </p>
              </div>
              <div className="flex items-center gap-2 mt-2">
                <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-surface-700/80 text-sm text-surface-400">
                  <FileSpreadsheet size={16} />
                  .xlsx / .xls
                </span>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Help Text */}
      <div className="flex items-start gap-2 text-xs text-surface-500">
        <AlertCircle size={14} className="flex-shrink-0 mt-0.5" />
        <p>
          Export from Xero: Reporting → Profit and Loss → Month by Month → Export to Excel
        </p>
      </div>
    </div>
  );
}
