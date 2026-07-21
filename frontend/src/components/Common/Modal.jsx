import React, { useEffect } from 'react';
import { X } from 'lucide-react';

/**
 * Reusable Modal component with animation and backdrop blur
 */
const Modal = ({
  isOpen = false,
  onClose,
  title = '',
  children,
  maxWidth = 'max-w-lg'
}) => {
  // Prevent body scroll when modal is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-xs transition-opacity duration-300">
      {/* Backdrop click closer */}
      <div className="absolute inset-0" onClick={onClose} />

      {/* Modal Dialog Body */}
      <div className={`relative w-full ${maxWidth} bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-2xl p-6 overflow-y-auto max-h-[90vh] transition-all transform scale-100 duration-300 space-y-6 z-10`}>
        {/* Header */}
        <div className="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
          <h3 className="font-extrabold text-slate-800 dark:text-white text-base tracking-tight">{title}</h3>
          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-850 rounded-xl transition-all cursor-pointer"
          >
            <X className="h-4.5 w-4.5" />
          </button>
        </div>

        {/* Content */}
        <div className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  );
};

export default Modal;
