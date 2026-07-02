const variants = {
  success: 'bg-accent-emerald/15 text-accent-emerald border-accent-emerald/25',
  danger: 'bg-accent-rose/15 text-accent-rose border-accent-rose/25',
  info: 'bg-accent-blue/15 text-accent-blue border-accent-blue/25',
  warning: 'bg-accent-amber/15 text-accent-amber border-accent-amber/25',
  neutral: 'bg-white/5 text-text-secondary border-white/10',
  purple: 'bg-accent-purple/15 text-accent-purple border-accent-purple/25',
  cyan: 'bg-accent-cyan/15 text-accent-cyan border-accent-cyan/25',
};

export default function Badge({ variant = 'neutral', children, className = '', ...props }) {
  return (
    <span
      className={`
        inline-flex items-center px-2.5 py-0.5 text-xs font-medium rounded-full
        border transition-colors duration-200
        ${variants[variant]}
        ${className}
      `}
      {...props}
    >
      {children}
    </span>
  );
}
