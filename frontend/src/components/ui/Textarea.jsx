import { forwardRef } from 'react';

const Textarea = forwardRef(function Textarea(
  { label, error, id, maxLength, value = '', className = '', ...props },
  ref
) {
  const inputId = id || label?.toLowerCase().replace(/\s+/g, '-');
  const charCount = typeof value === 'string' ? value.length : 0;

  return (
    <div className="space-y-1.5">
      {label && (
        <div className="flex items-center justify-between">
          <label
            htmlFor={inputId}
            className="block text-sm font-medium text-text-secondary"
          >
            {label}
          </label>
          {maxLength && (
            <span className={`text-xs ${charCount > maxLength * 0.9 ? 'text-accent-rose' : 'text-text-muted'}`}>
              {charCount}/{maxLength}
            </span>
          )}
        </div>
      )}
      <textarea
        ref={ref}
        id={inputId}
        value={value}
        maxLength={maxLength}
        className={`
          w-full px-4 py-3 rounded-xl
          bg-surface-elevated border border-border-bright
          text-text-primary placeholder:text-text-muted
          focus:outline-none focus:ring-2 focus:ring-accent-purple/50 focus:border-accent-purple/50
          transition-all duration-200 resize-y min-h-[120px]
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

export default Textarea;
