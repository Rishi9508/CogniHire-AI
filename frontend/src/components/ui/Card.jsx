export default function Card({ children, className = '', gradient = false, hoverable = false, ...props }) {
  return (
    <div
      className={`
        glass rounded-2xl p-5
        ${gradient ? 'gradient-border' : ''}
        ${hoverable ? 'hover:border-border-bright hover:shadow-lg hover:shadow-accent-purple/5 hover:-translate-y-0.5 cursor-pointer' : ''}
        transition-all duration-300 ease-out
        ${className}
      `}
      {...props}
    >
      {children}
    </div>
  );
}
