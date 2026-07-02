import { useState } from 'react';
import { useNavigate } from 'react-router';
import { Briefcase, Plus, Trash2, Clock, Award, ChevronRight, Sparkles, AlertCircle } from 'lucide-react';
import useJobs from '../hooks/useJobs';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import Textarea from '../components/ui/Textarea';
import Badge from '../components/ui/Badge';
import Spinner from '../components/ui/Spinner';
import EmptyState from '../components/ui/EmptyState';

export default function JobsPage() {
  const navigate = useNavigate();
  const { jobs, loading, error, createJob, deleteJob } = useJobs();
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [creating, setCreating] = useState(false);
  const [formError, setFormError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim()) {
      setFormError('Job title is required');
      return;
    }
    if (!description.trim()) {
      setFormError('Job description is required');
      return;
    }

    try {
      setCreating(true);
      setFormError('');
      await createJob({ title: title.trim(), description: description.trim() });
      setTitle('');
      setDescription('');
    } catch (err) {
      setFormError(err.message || 'Failed to create job');
    } finally {
      setCreating(false);
    }
  };

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    if (window.confirm('Are you sure you want to delete this job?')) {
      try {
        await deleteJob(id);
      } catch {
        // error is set in hook
      }
    }
  };

  return (
    <section className="max-w-7xl mx-auto">
      <div className="grid grid-cols-1 xl:grid-cols-5 gap-6">
        {/* Left: Create Job Form */}
        <div className="xl:col-span-2 animate-slide-in-left">
          <Card gradient>
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2 rounded-xl bg-gradient-to-br from-accent-purple/20 to-accent-blue/20">
                <Sparkles size={20} className="text-accent-purple" />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-text-primary">Create Job Analysis</h2>
                <p className="text-xs text-text-muted">AI will extract required skills from your description</p>
              </div>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <Input
                label="Job Title"
                placeholder="e.g., Senior React Developer"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                disabled={creating}
              />
              <Textarea
                label="Job Description"
                placeholder="Paste the full job description here. Include responsibilities, requirements, qualifications, and any technical skills needed..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                maxLength={5000}
                disabled={creating}
              />

              {formError && (
                <div className="flex items-center gap-2 text-accent-rose text-sm animate-fade-in">
                  <AlertCircle size={16} />
                  <span>{formError}</span>
                </div>
              )}

              <Button type="submit" className="w-full" disabled={creating}>
                {creating ? (
                  <>
                    <Spinner size={16} />
                    <span>Analyzing...</span>
                  </>
                ) : (
                  <>
                    <Plus size={16} />
                    <span>Analyze Job</span>
                  </>
                )}
              </Button>
            </form>
          </Card>
        </div>

        {/* Right: Job List */}
        <div className="xl:col-span-3 animate-slide-in-right">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-text-primary">
              Existing Jobs
              {jobs.length > 0 && (
                <span className="ml-2 text-sm text-text-muted font-normal">({jobs.length})</span>
              )}
            </h2>
          </div>

          {error && (
            <div className="flex items-center gap-2 text-accent-rose text-sm mb-4 animate-fade-in">
              <AlertCircle size={16} />
              <span>{error}</span>
            </div>
          )}

          {loading ? (
            <div className="flex items-center justify-center py-20">
              <Spinner size={32} />
            </div>
          ) : jobs.length === 0 ? (
            <EmptyState
              icon={Briefcase}
              title="No jobs yet"
              description="Create your first job analysis to get started. AI will automatically extract required skills from the job description."
            />
          ) : (
            <div className="space-y-3">
              {jobs.map((job, i) => (
                <Card
                  key={job.id}
                  hoverable
                  gradient
                  className="opacity-0 animate-fade-in cursor-pointer group"
                  style={{ animationDelay: `${i * 60}ms`, animationFillMode: 'forwards' }}
                  onClick={() => navigate(`/rankings/${job.id}`)}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-2">
                        <h3 className="text-sm font-semibold text-text-primary truncate">{job.title}</h3>
                        {job.experience_level && (
                          <Badge variant="purple">{job.experience_level}</Badge>
                        )}
                      </div>

                      {job.description && (
                        <p className="text-xs text-text-muted line-clamp-2 mb-3">{job.description}</p>
                      )}

                      {/* Skills */}
                      <div className="space-y-2">
                        {job.required_skills?.length > 0 && (
                          <div>
                            <p className="text-[10px] uppercase tracking-wider text-text-muted font-medium mb-1.5">Required Skills</p>
                            <div className="flex flex-wrap gap-1.5">
                              {job.required_skills.slice(0, 6).map((skill, j) => (
                                <Badge key={j} variant="success">{skill}</Badge>
                              ))}
                              {job.required_skills.length > 6 && (
                                <Badge variant="neutral">+{job.required_skills.length - 6}</Badge>
                              )}
                            </div>
                          </div>
                        )}
                        {job.preferred_skills?.length > 0 && (
                          <div>
                            <p className="text-[10px] uppercase tracking-wider text-text-muted font-medium mb-1.5">Preferred Skills</p>
                            <div className="flex flex-wrap gap-1.5">
                              {job.preferred_skills.slice(0, 4).map((skill, j) => (
                                <Badge key={j} variant="info">{skill}</Badge>
                              ))}
                              {job.preferred_skills.length > 4 && (
                                <Badge variant="neutral">+{job.preferred_skills.length - 4}</Badge>
                              )}
                            </div>
                          </div>
                        )}
                      </div>

                      {/* Footer */}
                      <div className="flex items-center gap-3 mt-3 pt-3 border-t border-border">
                        <div className="flex items-center gap-1.5 text-[10px] text-text-muted">
                          <Clock size={10} />
                          <span>{job.created_at ? new Date(job.created_at).toLocaleDateString() : 'Recently'}</span>
                        </div>
                        <div className="flex items-center gap-1 text-xs text-accent-blue font-medium opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                          <span>View Rankings</span>
                          <ChevronRight size={12} />
                        </div>
                      </div>
                    </div>

                    {/* Delete button */}
                    <button
                      onClick={(e) => handleDelete(job.id, e)}
                      className="p-1.5 rounded-lg text-text-muted hover:text-accent-rose hover:bg-accent-rose/10 opacity-0 group-hover:opacity-100 transition-all duration-200 ml-3 mt-1"
                      title="Delete job"
                    >
                      <Trash2 size={14} />
                    </button>
                  </div>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
