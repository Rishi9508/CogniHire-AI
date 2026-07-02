import { useNavigate } from 'react-router';
import { HelpCircle, ArrowLeft } from 'lucide-react';
import Button from '../components/ui/Button';

export default function NotFound() {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center min-h-[70vh] text-center p-6 animate-fade-in">
      <div className="p-4 rounded-full bg-white/5 border border-white/10 mb-6">
        <HelpCircle size={48} className="text-accent-purple animate-pulse" />
      </div>
      <h1 className="text-4xl font-extrabold text-text-primary tracking-tight mb-2">404</h1>
      <h2 className="text-lg font-semibold text-text-secondary mb-4">Page Not Found</h2>
      <p className="text-sm text-text-muted max-w-md mb-8">
        The page you are looking for does not exist or has been moved. Let's get you back to the recruiter dashboard.
      </p>
      <Button onClick={() => navigate('/')} className="flex items-center gap-2">
        <ArrowLeft size={16} />
        <span>Back to Dashboard</span>
      </Button>
    </div>
  );
}
