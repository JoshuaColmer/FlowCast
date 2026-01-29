import { useState } from 'react';
import { createPortal } from 'react-dom';
import { X, ZoomIn } from 'lucide-react';

interface ChartPanelProps {
  title: string;
  description?: string;
  imageBase64: string;
}

export function ChartPanel({ title, description, imageBase64 }: ChartPanelProps) {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const imageSrc = `data:image/png;base64,${imageBase64}`;

  return (
    <>
      <div className="bg-surface-800 border border-surface-700 rounded-xl overflow-hidden hover:border-surface-600 transition-all duration-200">
        <div className="p-4 border-b border-surface-700">
          <h4 className="font-semibold text-white">{title}</h4>
          {description && (
            <p className="text-xs text-surface-400 mt-1">{description}</p>
          )}
        </div>
        <div className="p-4">
          <div
            onClick={() => setIsModalOpen(true)}
            className="relative group cursor-pointer"
          >
            <img
              src={imageSrc}
              alt={title}
              className="w-full h-auto rounded-lg transition-all duration-200 group-hover:opacity-90"
            />
            {/* Hover overlay */}
            <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-200 bg-black/20 rounded-lg">
              <div className="bg-surface-900/80 backdrop-blur-sm px-3 py-2 rounded-lg flex items-center gap-2 text-sm text-white">
                <ZoomIn size={16} />
                Click to enlarge
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Lightbox Modal - rendered via Portal to escape parent constraints */}
      {isModalOpen && createPortal(
        <div
          className="fixed inset-0 z-[9999] bg-black/90 backdrop-blur-sm animate-fade-in cursor-pointer"
          onClick={() => setIsModalOpen(false)}
        >
          {/* Close button */}
          <button
            onClick={(e) => { e.stopPropagation(); setIsModalOpen(false); }}
            className="absolute top-4 right-4 p-2 bg-surface-800/80 hover:bg-surface-700 rounded-lg text-white transition-colors z-10"
          >
            <X size={24} />
          </button>

          {/* Title */}
          <div
            className="absolute top-4 left-4 bg-surface-800/80 backdrop-blur-sm px-4 py-2 rounded-lg z-10"
            onClick={(e) => e.stopPropagation()}
          >
            <h4 className="font-semibold text-white">{title}</h4>
            {description && (
              <p className="text-xs text-surface-400 mt-0.5">{description}</p>
            )}
          </div>

          {/* Centered image container - pointer-events-none lets clicks pass through */}
          <div className="absolute inset-0 flex items-center justify-center p-4 pointer-events-none">
            <img
              src={imageSrc}
              alt={title}
              onClick={(e) => e.stopPropagation()}
              className="max-w-[90vw] max-h-[85vh] object-contain rounded-xl shadow-2xl cursor-default pointer-events-auto"
            />
          </div>

          {/* Click anywhere hint */}
          <p className="absolute bottom-4 left-1/2 -translate-x-1/2 text-surface-400 text-sm z-10">
            Click outside image to close
          </p>
        </div>,
        document.body
      )}
    </>
  );
}
