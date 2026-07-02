import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router';
import { BarChart3, Download, RefreshCw, AlertCircle, ArrowLeft, CheckCircle, XCircle, ChevronDown, ChevronUp } from 'lucide-react';
import useRankings from '../hooks/useRankings';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';
import ProgressRing from '../components/ui/ProgressRing';
import Spinner from '../components/ui/Spinner';
import EmptyState from '../components/ui/EmptyState';

export default function RankingsPage() {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const {
    rankings,
    job,
    loading,
    computing,
    error: apiError,
    fetchRankings,
    computeRankings,
    exportCSV,
  } = useRankings(jobId);

  const [expandedExplanation, setExpandedExplanation] = useState({});
  const [localError, setLocalError] = useState('');

  useEffect(() => {
    fetchRankings();
  }, [fetchRankings]);

  const handleCompute = async () => {
    try {
      setLocalError('');
      await computeRankings();
    } catch (err) {
      setLocalError(err.message || 'Failed to compute rankings. Make sure you have uploaded candidate resumes.');
    }
  };

  const handleExport = async () => {
    try {
      setLocalError('');
      await exportCSV();
    } catch (err) {
      setLocalError(err.message || 'Failed to export rankings.');
    }
  };

  const toggleExplanation = (id) => {
    setExpandedExplanation((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  const getRankBadge = (rank) => {
    if (rank === 1) return <span className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-r from-yellow-400 to-amber-500 text-white font-extrabold shadow-lg shadow-yellow-500/20 text-sm">#1</span>;
    if (rank === 2) return <span className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-r from-slate-300 to-slate-400 text-white font-extrabold shadow-lg shadow-slate-400/20 text-sm">#2</span>;
    if (rank === 3) return <span className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-r from-amber-600 to-amber-700 text-white font-extrabold shadow-lg shadow-amber-700/20 text-sm">#3</span>;
    return <span className="flex items-center justify-center w-8 h-8 rounded-full bg-white/5 border border-white/10 text-text-secondary font-bold text-xs">#{rank}</span>;
  };

  if (loading && !computing) {
    return (
      <div className="flex items-center justify-center h-full py-20">
        <div className="flex flex-col items-center gap-4">
          <Spinner size={42} />
          <p className="text-sm text-text-muted">Fetching job rankings...</p>
        </div>
      </div>
    );
  }

  const error = localError || apiError;

  return (
    <section className="max-w-7xl mx-auto space-y-6">
      {/* Top navigation header */}
      <div className="flex items-center justify-between">
        <Button variant="ghost" size="sm" onClick={() => navigate('/jobs')} className="flex items-center gap-2">
          <ArrowLeft size={16} />
          <span>Back to Jobs</span>
        </Button>

        <div className="flex items-center gap-2">
          <Button
            variant="secondary"
            size="sm"
            onClick={handleCompute}
            disabled={computing}
            className="flex items-center gap-1.5"
          >
            <RefreshCw size={14} className={computing ? 'animate-spin' : ''} />
            <span>{computing ? 'Ranking Candidates...' : 'Rank Candidates'}</span>
          </Button>

          {rankings.length > 0 && (
            <Button
              variant="primary"
              size="sm"
              onClick={handleExport}
              className="flex items-center gap-1.5"
            >
              <Download size={14} />
              <span>Export CSV</span>
            </Button>
          )}
        </div>
      </div>

      {error && (
        <div className="flex items-center gap-2 p-4 rounded-xl bg-accent-rose/15 text-accent-rose text-sm border border-accent-rose/25 animate-fade-in">
          <AlertCircle size={18} className="shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Job Details Card */}
      {job && (
        <Card className="animate-slide-in-top">
          <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
            <div className="space-y-2">
              <div className="flex items-center gap-3">
                <h1 className="text-xl font-bold text-text-primary">{job.title}</h1>
                {job.experience_level && (
                  <Badge variant="purple">{job.experience_level}</Badge>
                )}
              </div>
              <p className="text-sm text-text-secondary leading-relaxed line-clamp-3 hover:line-clamp-none transition-all duration-300">
                {job.description}
              </p>
            </div>
          </div>

          {job.required_skills?.length > 0 && (
            <div className="mt-4 pt-4 border-t border-border">
              <p className="text-[10px] uppercase tracking-wider text-text-muted font-semibold mb-2">Target Skills Profile</p>
              <div className="flex flex-wrap gap-1.5">
                {job.required_skills.map((skill, index) => (
                  <Badge key={index} variant="success">{skill}</Badge>
                ))}
              </div>
            </div>
          )}
        </Card>
      )}

      {/* Rankings List */}
      <div className="space-y-4">
        <h2 className="text-lg font-semibold text-text-primary">
          Ranked Candidates
          {rankings.length > 0 && (
            <span className="ml-2 text-sm text-text-muted font-normal">({rankings.length})</span>
          )}
        </h2>

        {computing ? (
          <div className="flex flex-col items-center justify-center py-20 bg-surface-elevated/20 rounded-2xl border border-border border-dashed gap-4">
            <Spinner size={36} />
            <p className="text-sm text-text-secondary">AI pipeline is parsing context and matching embeddings...</p>
          </div>
        ) : rankings.length === 0 ? (
          <EmptyState
            icon={BarChart3}
            title="No rankings calculated"
            description="Trigger the AI matching pipeline to rank uploaded candidates against this job description. The algorithm will run semantic similarity and skill gap analysis."
            actionLabel="Rank Candidates Now"
            onAction={handleCompute}
          />
        ) : (
          <div className="space-y-4">
            {rankings.map((ranking, index) => {
              const isExpanded = expandedExplanation[ranking.id] ?? true; // Default expanded for readability
              const overallPct = ranking.overall_score * 100;
              const semanticPct = ranking.semantic_score * 100;
              const skillPct = ranking.skill_score * 100;
              
              return (
                <div
                  key={ranking.id}
                  className="glass rounded-2xl overflow-hidden border border-border hover:border-border-bright hover:shadow-xl hover:shadow-accent-purple/5 transition-all duration-300 opacity-0 animate-fade-in"
                  style={{ animationDelay: `${index * 80}ms`, animationFillMode: 'forwards' }}
                >
                  <div className="p-5 flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
                    {/* Left: Rank & Candidate Info */}
                    <div className="flex items-center gap-4 min-w-0">
                      <div className="shrink-0">
                        {getRankBadge(ranking.rank)}
                      </div>
                      <div className="min-w-0">
                        <h3 className="text-base font-semibold text-text-primary truncate">
                          {ranking.candidate_name || 'Candidate Name'}
                        </h3>
                        <p className="text-xs text-text-muted truncate">
                          {ranking.candidate_email || 'No email provided'}
                        </p>
                      </div>
                    </div>

                    {/* Middle: Score ring & breakdowns */}
                    <div className="flex items-center gap-6 shrink-0 w-full lg:w-auto">
                      <div className="flex items-center gap-2">
                        <ProgressRing value={overallPct} size={64} strokeWidth={5} />
                        <div className="flex flex-col">
                          <span className="text-xs font-semibold text-text-primary">Overall Score</span>
                          <span className="text-[10px] text-text-muted">Weighted hybrid</span>
                        </div>
                      </div>

                      <div className="flex-1 flex flex-col gap-2 min-w-[160px] max-w-[220px]">
                        <div>
                          <div className="flex justify-between text-[10px] font-medium text-text-secondary mb-0.5">
                            <span>Semantic Fit</span>
                            <span>{Math.round(semanticPct)}%</span>
                          </div>
                          <div className="h-1 bg-white/5 rounded-full overflow-hidden">
                            <div className="h-full bg-accent-purple rounded-full" style={{ width: `${semanticPct}%` }} />
                          </div>
                        </div>
                        <div>
                          <div className="flex justify-between text-[10px] font-medium text-text-secondary mb-0.5">
                            <span>Skill Profile</span>
                            <span>{Math.round(skillPct)}%</span>
                          </div>
                          <div className="h-1 bg-white/5 rounded-full overflow-hidden">
                            <div className="h-full bg-accent-blue rounded-full" style={{ width: `${skillPct}%` }} />
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Right: Expand details */}
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => toggleExplanation(ranking.id)}
                      className="flex items-center gap-1.5 shrink-0 self-end lg:self-auto text-text-secondary"
                    >
                      <span>{isExpanded ? 'Hide Details' : 'View Details'}</span>
                      {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </Button>
                  </div>

                  {/* Expanded Section (Detailed explanation and skill breakdown) */}
                  {isExpanded && (
                    <div className="px-5 pb-5 pt-1 border-t border-border/50 bg-white/1 space-y-4 animate-fade-in">
                      {/* Skills match/missing grid */}
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {ranking.matched_skills?.length > 0 && (
                          <div className="space-y-2">
                            <div className="flex items-center gap-1.5 text-[10px] font-bold tracking-wider text-accent-emerald uppercase">
                              <CheckCircle size={12} />
                              <span>Matched Skills ({ranking.matched_skills.length})</span>
                            </div>
                            <div className="flex flex-wrap gap-1.5">
                              {ranking.matched_skills.map((skill, sIdx) => (
                                <Badge key={sIdx} variant="success">{skill}</Badge>
                              ))}
                            </div>
                          </div>
                        )}

                        {ranking.missing_skills?.length > 0 && (
                          <div className="space-y-2">
                            <div className="flex items-center gap-1.5 text-[10px] font-bold tracking-wider text-accent-rose uppercase">
                              <XCircle size={12} />
                              <span>Missing Skills ({ranking.missing_skills.length})</span>
                            </div>
                            <div className="flex flex-wrap gap-1.5">
                              {ranking.missing_skills.map((skill, sIdx) => (
                                <Badge key={sIdx} variant="danger">{skill}</Badge>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>

                      {/* Explanation box */}
                      {ranking.explanation && (
                        <div className="p-4 rounded-xl bg-surface-elevated/50 border border-border/30">
                          <p className="text-[10px] font-bold uppercase tracking-wider text-text-muted mb-1.5">AI Explanation</p>
                          <p className="text-xs text-text-secondary leading-relaxed whitespace-pre-line">
                            {ranking.explanation}
                          </p>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </section>
  );
}
