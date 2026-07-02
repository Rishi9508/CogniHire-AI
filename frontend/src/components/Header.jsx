import { useLocation } from 'react-router';
import { ChevronRight } from 'lucide-react';

const routeTitles = {
  '/': 'Dashboard',
  '/jobs': 'Job Analysis',
  '/candidates': 'Candidates',
};

export default function Header() {
  const location = useLocation();

  let title = routeTitles[location.pathname];
  let breadcrumbs = [];

  if (location.pathname.startsWith('/rankings/')) {
    title = 'Rankings';
    breadcrumbs = [
      { label: 'Jobs', path: '/jobs' },
      { label: 'Rankings' },
    ];
  } else if (title) {
    breadcrumbs = [{ label: title }];
  } else {
    title = 'Not Found';
    breadcrumbs = [{ label: 'Not Found' }];
  }

  return (
    <header className="flex items-center justify-between px-6 py-4 border-b border-border bg-surface/80 backdrop-blur-lg sticky top-0 z-30">
      <div className="ml-10 md:ml-0">
        <h1 className="text-xl font-bold text-text-primary">{title}</h1>
        <div className="flex items-center gap-1.5 mt-0.5">
          <span className="text-xs text-text-muted">Home</span>
          {breadcrumbs.map((crumb, i) => (
            <span key={i} className="flex items-center gap-1.5">
              <ChevronRight size={10} className="text-text-muted" />
              <span className={`text-xs ${i === breadcrumbs.length - 1 ? 'text-text-secondary' : 'text-text-muted'}`}>
                {crumb.label}
              </span>
            </span>
          ))}
        </div>
      </div>

      {/* Right side actions */}
      <div className="flex items-center gap-3">
        <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-accent-emerald/10 border border-accent-emerald/20">
          <div className="w-1.5 h-1.5 rounded-full bg-accent-emerald animate-pulse" />
          <span className="text-xs text-accent-emerald font-medium">System Online</span>
        </div>
        <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-accent-purple to-accent-blue flex items-center justify-center text-xs font-bold text-white">
          S
        </div>
      </div>
    </header>
  );
}
