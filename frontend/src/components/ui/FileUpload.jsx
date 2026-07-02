import { useState, useRef, useCallback } from 'react';
import { Upload, FileText, X, AlertCircle } from 'lucide-react';
import Button from './Button';

const ACCEPTED_TYPES = {
  'application/pdf': '.pdf',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
};

const ACCEPTED_EXTENSIONS = ['.pdf', '.docx'];

function isValidFile(file) {
  const ext = '.' + file.name.split('.').pop().toLowerCase();
  return ACCEPTED_EXTENSIONS.includes(ext) || Object.keys(ACCEPTED_TYPES).includes(file.type);
}

export default function FileUpload({ onFilesSelected, multiple = true, disabled = false }) {
  const [isDragOver, setIsDragOver] = useState(false);
  const [files, setFiles] = useState([]);
  const [error, setError] = useState('');
  const inputRef = useRef(null);

  const handleFiles = useCallback((fileList) => {
    setError('');
    const newFiles = Array.from(fileList);
    const validFiles = newFiles.filter(isValidFile);
    const invalidCount = newFiles.length - validFiles.length;

    if (invalidCount > 0) {
      setError(`${invalidCount} file(s) rejected. Only .pdf and .docx files are accepted.`);
    }

    if (validFiles.length > 0) {
      const updatedFiles = multiple ? [...files, ...validFiles] : validFiles;
      setFiles(updatedFiles);
      onFilesSelected?.(updatedFiles);
    }
  }, [files, multiple, onFilesSelected]);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setIsDragOver(false);
    handleFiles(e.dataTransfer.files);
  }, [handleFiles]);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const removeFile = useCallback((index) => {
    const updatedFiles = files.filter((_, i) => i !== index);
    setFiles(updatedFiles);
    onFilesSelected?.(updatedFiles);
  }, [files, onFilesSelected]);

  const formatSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  return (
    <div className="space-y-3">
      {/* Drop zone */}
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={() => !disabled && inputRef.current?.click()}
        className={`
          relative flex flex-col items-center justify-center
          p-8 rounded-2xl border-2 border-dashed cursor-pointer
          transition-all duration-300 ease-out
          ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
          ${isDragOver
            ? 'border-accent-purple bg-accent-purple/10 shadow-lg shadow-accent-purple/10'
            : 'border-border-bright bg-surface-elevated/50 hover:border-accent-blue/40 hover:bg-surface-elevated/80'
          }
        `}
      >
        <div className={`
          p-4 rounded-2xl mb-4 transition-all duration-300
          ${isDragOver
            ? 'bg-accent-purple/20 scale-110'
            : 'bg-gradient-to-br from-accent-purple/10 to-accent-blue/10'
          }
        `}>
          <Upload
            size={32}
            className={`transition-colors duration-300 ${isDragOver ? 'text-accent-purple' : 'text-text-muted'}`}
          />
        </div>

        <p className="text-sm font-medium text-text-primary mb-1">
          {isDragOver ? 'Drop files here' : 'Drag & drop resumes here'}
        </p>
        <p className="text-xs text-text-muted mb-4">or click to browse</p>
        <Button variant="secondary" size="sm" disabled={disabled} onClick={(e) => e.stopPropagation()}>
          Browse Files
        </Button>
        <p className="text-xs text-text-muted mt-3">Supports .pdf and .docx files</p>

        <input
          ref={inputRef}
          type="file"
          multiple={multiple}
          accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
          className="hidden"
          onChange={(e) => handleFiles(e.target.files)}
          disabled={disabled}
        />
      </div>

      {/* Error */}
      {error && (
        <div className="flex items-center gap-2 text-accent-rose text-sm animate-fade-in">
          <AlertCircle size={16} />
          <span>{error}</span>
        </div>
      )}

      {/* File list */}
      {files.length > 0 && (
        <div className="space-y-2 animate-fade-in">
          {files.map((file, index) => (
            <div
              key={`${file.name}-${index}`}
              className="flex items-center justify-between px-4 py-2.5 rounded-xl bg-surface-elevated border border-border group hover:border-border-bright transition-all duration-200"
            >
              <div className="flex items-center gap-3 min-w-0">
                <div className="p-1.5 rounded-lg bg-accent-blue/10">
                  <FileText size={16} className="text-accent-blue" />
                </div>
                <div className="min-w-0">
                  <p className="text-sm text-text-primary truncate">{file.name}</p>
                  <p className="text-xs text-text-muted">{formatSize(file.size)}</p>
                </div>
              </div>
              <button
                onClick={() => removeFile(index)}
                className="p-1 rounded-lg text-text-muted hover:text-accent-rose hover:bg-accent-rose/10 opacity-0 group-hover:opacity-100 transition-all duration-200"
              >
                <X size={14} />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
