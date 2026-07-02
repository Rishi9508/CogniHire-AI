import { useState } from 'react';
import { Users, Upload, Sparkles, AlertCircle } from 'lucide-react';
import useCandidates from '../hooks/useCandidates';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import FileUpload from '../components/ui/FileUpload';
import CandidateCard from '../components/CandidateCard';
import Spinner from '../components/ui/Spinner';
import EmptyState from '../components/ui/EmptyState';

export default function CandidatesPage() {
  const { candidates, loading, uploading, error, uploadCandidates, deleteCandidate } = useCandidates();
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [localError, setLocalError] = useState('');

  const handleFilesSelected = (files) => {
    setSelectedFiles(files);
    setLocalError('');
  };

  const handleUpload = async () => {
    if (selectedFiles.length === 0) return;
    try {
      setLocalError('');
      await uploadCandidates(selectedFiles);
      setSelectedFiles([]); // Reset after successful upload
    } catch (err) {
      setLocalError(err.message || 'Failed to upload one or more resumes');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this candidate?')) {
      try {
        await deleteCandidate(id);
      } catch {
        // error is set in hook
      }
    }
  };

  return (
    <section className="max-w-7xl mx-auto">
      <div className="grid grid-cols-1 xl:grid-cols-5 gap-6">
        {/* Left: Upload card */}
        <div className="xl:col-span-2 animate-slide-in-left">
          <Card gradient>
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2 rounded-xl bg-gradient-to-br from-accent-cyan/20 to-accent-blue/20">
                <Sparkles size={20} className="text-accent-cyan" />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-text-primary">Upload Resumes</h2>
                <p className="text-xs text-text-muted">AI will extract name, email, phone, and skills</p>
              </div>
            </div>

            <div className="space-y-4">
              <FileUpload
                onFilesSelected={handleFilesSelected}
                disabled={uploading}
              />

              {localError && (
                <div className="flex items-center gap-2 text-accent-rose text-sm animate-fade-in">
                  <AlertCircle size={16} />
                  <span>{localError}</span>
                </div>
              )}

              {selectedFiles.length > 0 && (
                <Button
                  onClick={handleUpload}
                  className="w-full mt-4"
                  disabled={uploading}
                >
                  {uploading ? (
                    <>
                      <Spinner size={16} />
                      <span>Parsing Resumes...</span>
                    </>
                  ) : (
                    <>
                      <Upload size={16} />
                      <span>Upload & Parse {selectedFiles.length} Resume(s)</span>
                    </>
                  )}
                </Button>
              )}
            </div>
          </Card>
        </div>

        {/* Right: Candidate Grid */}
        <div className="xl:col-span-3 animate-slide-in-right">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-text-primary">
              All Candidates
              {candidates.length > 0 && (
                <span className="ml-2 text-sm text-text-muted font-normal">({candidates.length})</span>
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
          ) : candidates.length === 0 ? (
            <EmptyState
              icon={Users}
              title="No candidates yet"
              description="Upload candidate resumes in PDF or DOCX format. The AI pipeline will automatically parse and display them here."
            />
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {candidates.map((candidate, i) => (
                <CandidateCard
                  key={candidate.id}
                  candidate={candidate}
                  onDelete={handleDelete}
                  delay={i * 50}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
