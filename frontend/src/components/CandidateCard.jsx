import { X, Mail, ExternalLink } from 'lucide-react';
import Badge from './ui/Badge';

export default function CandidateCard({ candidate, onDelete, onView, delay = 0 }) {
  const { name, email, skills = [] } = candidate;
  const displaySkills = skills.slice(0, 5);
  const extraCount = skills.length - 5;

  const initials = name
    ? name
        .split(' ')
        .map((w) => w[0])
        .join('')
        .toUpperCase()
        .slice(0, 2)
    : '??';

  const gradients = [
    'from-accent-purple to-accent-blue',
    'from-accent-blue to-accent-cyan',
    'from-accent-cyan to-accent-emerald',
    'from-accent-emerald to-accent-amber',
    'from-accent-amber to-accent-rose',
    'from-accent-rose to-accent-purple',
  ];

  const gradientIndex = name ? name.charCodeAt(0) % gradients.length : 0;

  return (
    <article
      className="glass rounded-2xl overflow-hidden group hover:border-border-bright hover:shadow-xl hover:shadow-accent-purple/5 hover:-translate-y-1 transition-all duration-300 opacity-0 animate-fade-in"
      style={{ animationDelay: `${delay}ms`, animationFillMode: 'forwards' }}
    >
      {/* Gradient top bar */}
      <div className={`h-1 bg-gradient-to-r ${gradients[gradientIndex]}`} />

      <div className="p-5">
        {/* Header row */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${gradients[gradientIndex]} flex items-center justify-center text-sm font-bold text-white shadow-lg`}>
              {initials}
            </div>
            <div>
              <h3 className="text-sm font-semibold text-text-primary">{name || 'Unknown'}</h3>
              {email && (
                <div className="flex items-center gap-1 mt-0.5">
                  <Mail size={10} className="text-text-muted" />
                  <span className="text-xs text-text-muted truncate max-w-[180px]">{email}</span>
                </div>
              )}
            </div>
          </div>

          {onDelete && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                onDelete(candidate.id);
              }}
              className="p-1.5 rounded-lg text-text-muted hover:text-accent-rose hover:bg-accent-rose/10 opacity-0 group-hover:opacity-100 transition-all duration-200"
              title="Delete candidate"
            >
              <X size={14} />
            </button>
          )}
        </div>

        {/* Skills */}
        {displaySkills.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mb-4">
            {displaySkills.map((skill, i) => (
              <Badge key={i} variant="info">
                {skill}
              </Badge>
            ))}
            {extraCount > 0 && (
              <Badge variant="neutral">+{extraCount} more</Badge>
            )}
          </div>
        )}

        {/* Footer */}
        {onView && (
          <button
            onClick={() => onView(candidate.id)}
            className="flex items-center gap-1.5 text-xs text-accent-blue hover:text-accent-cyan font-medium transition-colors duration-200 group/link"
          >
            <span>View Details</span>
            <ExternalLink size={12} className="transition-transform duration-200 group-hover/link:translate-x-0.5" />
          </button>
        )}
      </div>
    </article>
  );
}
