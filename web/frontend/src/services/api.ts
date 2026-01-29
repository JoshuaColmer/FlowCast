const API_BASE = import.meta.env.VITE_API_URL || '/api';

export interface AnalysisResponse {
  session_id: string;
  company: string;
  metrics: Record<string, any>;
  health_summary: Record<string, any>;
  insights: Array<{ type: string; text: string }>;
  forecast: Record<string, any>;
  charts: Record<string, string>;
}

export async function uploadAndAnalyze(file: File, currency: string): Promise<AnalysisResponse> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE}/upload?currency=${encodeURIComponent(currency)}`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to analyze file');
  }

  return response.json();
}

export async function downloadExport(sessionId: string, format: 'excel' | 'zip'): Promise<Blob> {
  const response = await fetch(`${API_BASE}/export/${sessionId}/${format}`);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to generate export');
  }

  return response.blob();
}
