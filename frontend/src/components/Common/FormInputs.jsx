import React from 'react';

/**
 * Reusable text/number/email/password Input Field
 */
export const InputField = React.forwardRef(({
  label,
  error,
  icon: Icon,
  className = '',
  ...props
}, ref) => {
  return (
    <div className={`space-y-1 ${className}`}>
      {label && (
        <label className="block text-2xs font-extrabold uppercase tracking-wider text-slate-400 dark:text-slate-500">
          {label}
        </label>
      )}
      <div className="relative">
        {Icon && (
          <span className="absolute inset-y-0 left-0 pl-3 flex items-center text-slate-400">
            <Icon className="h-4.5 w-4.5" />
          </span>
        )}
        <input
          ref={ref}
          {...props}
          className={`w-full ${Icon ? 'pl-10' : 'px-3.5'} py-2.5 bg-slate-50 dark:bg-slate-950 border ${
            error ? 'border-rose-500 focus:border-rose-500' : 'border-slate-200 dark:border-slate-800 focus:border-indigo-400'
          } rounded-xl text-sm focus:outline-none transition-colors dark:text-white`}
        />
      </div>
      {error && <span className="text-xs font-bold text-rose-550 block">{error.message || error}</span>}
    </div>
  );
});

InputField.displayName = 'InputField';

/**
 * Reusable Select Field
 */
export const SelectField = React.forwardRef(({
  label,
  error,
  options = [],
  className = '',
  ...props
}, ref) => {
  return (
    <div className={`space-y-1 ${className}`}>
      {label && (
        <label className="block text-2xs font-extrabold uppercase tracking-wider text-slate-400 dark:text-slate-500">
          {label}
        </label>
      )}
      <select
        ref={ref}
        {...props}
        className={`w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-950 border ${
          error ? 'border-rose-500 focus:border-rose-500' : 'border-slate-200 dark:border-slate-800 focus:border-indigo-400'
        } rounded-xl text-sm focus:outline-none transition-colors dark:text-white`}
      >
        {options.map((opt, idx) => (
          <option key={opt.value || idx} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
      {error && <span className="text-xs font-bold text-rose-550 block">{error.message || error}</span>}
    </div>
  );
});

SelectField.displayName = 'SelectField';

/**
 * Reusable Textarea Field
 */
export const TextareaField = React.forwardRef(({
  label,
  error,
  rows = 3,
  className = '',
  ...props
}, ref) => {
  return (
    <div className={`space-y-1 ${className}`}>
      {label && (
        <label className="block text-2xs font-extrabold uppercase tracking-wider text-slate-400 dark:text-slate-500">
          {label}
        </label>
      )}
      <textarea
        ref={ref}
        rows={rows}
        {...props}
        className={`w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-950 border ${
          error ? 'border-rose-500 focus:border-rose-500' : 'border-slate-200 dark:border-slate-800 focus:border-indigo-400'
        } rounded-xl text-sm focus:outline-none transition-colors dark:text-white`}
      />
      {error && <span className="text-xs font-bold text-rose-550 block">{error.message || error}</span>}
    </div>
  );
});

TextareaField.displayName = 'TextareaField';
