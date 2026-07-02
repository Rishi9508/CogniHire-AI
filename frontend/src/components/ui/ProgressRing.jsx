import { useEffect, useRef, useState } from 'react';

export default function ProgressRing({
  value = 0,
  size = 80,
  strokeWidth = 6,
  color = 'var(--color-accent-purple)',
  bgColor = 'rgba(148, 163, 184, 0.1)',
  showValue = true,
  fontSize,
  className = '',
}) {
  const [mounted, setMounted] = useState(false);
  const circleRef = useRef(null);

  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const clampedValue = Math.max(0, Math.min(100, value));
  const offset = circumference - (clampedValue / 100) * circumference;

  useEffect(() => {
    requestAnimationFrame(() => setMounted(true));
  }, []);

  const computedFontSize = fontSize || Math.max(12, size * 0.22);

  return (
    <div className={`relative inline-flex items-center justify-center ${className}`}>
      <svg
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
        className="-rotate-90"
      >
        {/* Background circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={bgColor}
          strokeWidth={strokeWidth}
        />
        {/* Progress circle */}
        <circle
          ref={circleRef}
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={mounted ? offset : circumference}
          style={{
            transition: 'stroke-dashoffset 1.2s ease-out',
            filter: `drop-shadow(0 0 6px ${color}40)`,
          }}
        />
      </svg>
      {showValue && (
        <span
          className="absolute font-bold text-text-primary"
          style={{ fontSize: computedFontSize }}
        >
          {Math.round(clampedValue)}
        </span>
      )}
    </div>
  );
}
