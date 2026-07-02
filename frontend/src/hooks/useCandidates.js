import { useState, useEffect, useCallback } from 'react';
import api from '../services/api';

export function useCandidates() {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const fetchCandidates = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getCandidates();
      setCandidates(Array.isArray(data) ? data : data.candidates || []);
    } catch (err) {
      setError(err.message || 'Failed to fetch candidates');
    } finally {
      setLoading(false);
    }
  }, []);

  const uploadCandidates = useCallback(async (files) => {
    try {
      setUploading(true);
      setError(null);
      const result = await api.uploadCandidates(files);
      await fetchCandidates();
      return result;
    } catch (err) {
      setError(err.message || 'Failed to upload candidates');
      throw err;
    } finally {
      setUploading(false);
    }
  }, [fetchCandidates]);

  const deleteCandidate = useCallback(async (id) => {
    try {
      setError(null);
      await api.deleteCandidate(id);
      setCandidates((prev) => prev.filter((c) => c.id !== id));
    } catch (err) {
      setError(err.message || 'Failed to delete candidate');
      throw err;
    }
  }, []);

  useEffect(() => {
    fetchCandidates();
  }, [fetchCandidates]);

  return { candidates, loading, uploading, error, fetchCandidates, uploadCandidates, deleteCandidate };
}

export default useCandidates;
