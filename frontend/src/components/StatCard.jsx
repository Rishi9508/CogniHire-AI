import { TrendingUp, TrendingDown } from 'lucide-react';

export default function StatCard({ icon: Icon, label, value, trend, trendLabel, color = 'accent-purple', delay = 0 }) {
  const colorMap = {
    'accent-purple': {
      bg: 'bg-accent-purple/10',
      icon: 'text-accent-purple',
      trend: 'text-accent-purple',
    },
    'accent-blue': {
      bg: 'bg-accent-blue/10',
      icon: 'text-accent-blue',
      trend: 'text-accent-blue',
    },
    'accent-cyan': {
      bg: 'bg-accent-cyan/10',
      icon: 'text-accent-cyan',
      trend: 'text-accent-cyan',
    },
    'accent-emerald': {
      bg: 'bg-accent-emerald/10',
      icon: 'text-accent-emerald',
      trend: 'text-accent-emerald',
    },
    'accent-amber': {
      bg: 'bg-accent-amber/10',
      icon: 'text-accent-amber',
      trend: 'text-accent-amber',
    },
    'accent-rose': {
      bg: 'bg-accent-rose/10',
      icon: 'text-accent-rose',
      trend: 'text-accent-rose',
    },
  };

  const colors = colorMap[color] || colorMap['accent-purple'];

  return (
    <div
      className="glass rounded-2xl p-5 hover:border-border-bright hover:shadow-lg transition-all duration-300 opacity-0 animate-fade-in group"
      style={{ animationDelay: `${delay}ms`, animationFillMode: 'forwards' }}
    >
      <div className="flex items-start justify-between mb-4">
        <div className={`p-2.5 rounded-xl ${colors.bg} transition-transform duration-300 group-hover:scale-110`}>
          <Icon size={20} className={colors.icon} />
        </div>
        {trend !== undefined && (
          <div className={`flex items-center gap-1 text-xs font-medium ${trend >= 0 ? 'text-accent-emerald' : 'text-accent-rose'}`}>
            {trend >= 0 ? <TrendingUp size={14} /> : <TrendingDown size={14} />}
            <span>{Math.abs(trend)}%</span>
          </div>
        )}
      </div>

      <p className="text-2xl font-bold text-text-primary mb-1">{value}</p>
      <p className="text-xs text-text-muted">{label}</p>
      {trendLabel && (
        <p className="text-[10px] text-text-muted mt-1">{trendLabel}</p>
      )}
    </div>
  );
}
