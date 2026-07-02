import { useState } from 'react';
import { NavLink, useLocation } from 'react-router';
import { LayoutDashboard, Briefcase, Users, BarChart3, Menu, X, Sparkles } from 'lucide-react';

const navItems = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/jobs', icon: Briefcase, label: 'Jobs' },
  { to: '/candidates', icon: Users, label: 'Candidates' },
];

export default function Sidebar() {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  const isRankingsActive = location.pathname.startsWith('/rankings');

  return (
    <>
      {/* Mobile hamburger */}
      <button
        onClick={() => setIsOpen(true)}
        className="fixed top-4 left-4 z-50 p-2 rounded-xl glass md:hidden hover:bg-white/5 transition-colors"
      >
        <Menu size={20} className="text-text-primary" />
      </button>

      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/50 backdrop-blur-sm md:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Sidebar */}
      <nav
        className={`
          fixed top-0 left-0 z-50 h-full w-64
          bg-surface/95 backdrop-blur-xl border-r border-border
          flex flex-col
          transition-transform duration-300 ease-out
          md:translate-x-0 md:static md:z-auto
          ${isOpen ? 'translate-x-0' : '-translate-x-full'}
        `}
      >
        {/* Logo */}
        <div className="flex items-center justify-between px-5 py-6 border-b border-border">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-accent-purple to-accent-cyan flex items-center justify-center shadow-lg shadow-accent-purple/30">
              <Sparkles size={18} className="text-white" />
            </div>
            <div>
              <h1 className="text-sm font-bold text-text-primary tracking-tight">SemantiHire</h1>
              <p className="text-[10px] text-text-muted font-medium tracking-wider uppercase">AI Platform</p>
            </div>
          </div>
          <button
            onClick={() => setIsOpen(false)}
            className="p-1 rounded-lg hover:bg-white/5 md:hidden transition-colors"
          >
            <X size={18} className="text-text-muted" />
          </button>
        </div>

        {/* Nav links */}
        <div className="flex-1 px-3 py-4 space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
              onClick={() => setIsOpen(false)}
              className={({ isActive }) => `
                flex items-center gap-3 px-3 py-2.5 rounded-xl
                text-sm font-medium transition-all duration-200
                group relative
                ${isActive
                  ? 'text-text-primary bg-gradient-to-r from-accent-purple/15 to-accent-blue/10 shadow-sm'
                  : 'text-text-muted hover:text-text-secondary hover:bg-white/3'
                }
              `}
            >
              {({ isActive }) => (
                <>
                  {isActive && (
                    <div className="absolute left-0 top-1/2 -translate-y-1/2 w-0.5 h-5 bg-gradient-to-b from-accent-purple to-accent-blue rounded-full" />
                  )}
                  <item.icon
                    size={18}
                    className={`transition-colors duration-200 ${isActive ? 'text-accent-purple' : 'text-text-muted group-hover:text-text-secondary'}`}
                  />
                  <span>{item.label}</span>
                </>
              )}
            </NavLink>
          ))}

          {/* Rankings link (shows as active for /rankings/* routes) */}
          <NavLink
            to="/jobs"
            onClick={() => setIsOpen(false)}
            className={`
              flex items-center gap-3 px-3 py-2.5 rounded-xl
              text-sm font-medium transition-all duration-200
              group relative
              ${isRankingsActive
                ? 'text-text-primary bg-gradient-to-r from-accent-purple/15 to-accent-blue/10 shadow-sm'
                : 'text-text-muted hover:text-text-secondary hover:bg-white/3'
              }
            `}
          >
            {isRankingsActive && (
              <div className="absolute left-0 top-1/2 -translate-y-1/2 w-0.5 h-5 bg-gradient-to-b from-accent-purple to-accent-blue rounded-full" />
            )}
            <BarChart3
              size={18}
              className={`transition-colors duration-200 ${isRankingsActive ? 'text-accent-purple' : 'text-text-muted group-hover:text-text-secondary'}`}
            />
            <span>Rankings</span>
          </NavLink>
        </div>

        {/* Bottom section */}
        <div className="px-4 py-4 border-t border-border">
          <div className="px-3 py-3 rounded-xl bg-gradient-to-r from-accent-purple/10 to-accent-blue/10 border border-accent-purple/20">
            <p className="text-xs font-medium text-text-primary mb-0.5">Semantic Matching</p>
            <p className="text-[10px] text-text-muted">Powered by AI embeddings</p>
          </div>
        </div>
      </nav>
    </>
  );
}
