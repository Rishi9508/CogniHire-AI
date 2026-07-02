import { forwardRef } from 'react';

const variants = {
  primary:
    'bg-gradient-to-r from-accent-purple to-accent-blue text-white shadow-lg shadow-accent-purple/20 hover:shadow-accent-purple/40 hover:brightness-110',
  secondary:
    'bg-surface-elevated text-text-primary border border-border-bright hover:bg-white/5 hover:border-white/20',
  danger:
    'bg-accent-rose/10 text-accent-rose border border-accent-rose/20 hover:bg-accent-rose/20 hover:border-accent-rose/40',
  ghost:
    'text-text-secondary hover:text-text-primary hover:bg-white/5',
};

const sizes = {
  sm: 'px-3 py-1.5 text-xs rounded-lg gap-1.5',
  md: 'px-4 py-2 text-sm rounded-xl gap-2',
  lg: 'px-6 py-3 text-base rounded-xl gap-2.5',
};

const Button = forwardRef(function Button(
  { variant = 'primary', size = 'md', children, className = '', disabled, ...props },
  ref
) {
  return (
    <button
      ref={ref}
      className={`
        inline-flex items-center justify-center font-medium
        transition-all duration-200 ease-out
        active:scale-[0.97] disabled:opacity-50 disabled:cursor-not-allowed disabled:active:scale-100
        cursor-pointer select-none
        ${variants[variant]}
        ${sizes[size]}
        ${className}
      `}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
});

export default Button;
