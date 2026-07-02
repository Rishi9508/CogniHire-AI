import { forwardRef } from 'react';

const Input = forwardRef(function Input(
  { label, error, id, className = '', ...props },
  ref
) {
  const inputId = id || label?.toLowerCase().replace(/\s+/g, '-');

  return (
    <div className="space-y-1.5">
      {label && (
        <label
          htmlFor={inputId}
          className="block text-sm font-medium text-text-secondary"
        >
          {label}
        </label>
      )}
      <input
        ref={ref}
        id={inputId}
        className={`
          w-full px-4 py-2.5 rounded-xl
          bg-surface-elevated border border-border-bright
          text-text-primary placeholder:text-text-muted
          focus:outline-none focus:ring-2 focus:ring-accent-purple/50 focus:border-accent-purple/50
          transition-all duration-200
          ${error ? 'border-accent-rose/50 focus:ring-accent-rose/50 focus:border-accent-rose/50' : ''}
          ${className}
        `}
        {...props}
      />
      {error && (
        <p className="text-xs text-accent-rose mt-1">{error}</p>
      )}
    </div>
  );
});

export default Input;
