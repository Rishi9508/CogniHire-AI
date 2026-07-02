import { useState, useCallback } from 'react';
import api from '../services/api';

export function useRankings(jobId) {
  const [rankings, setRankings] = useState([]);
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(false);
  const [computing, setComputing] = useState(false);
  const [error, setError] = useState(null);

  const fetchRankings = useCallback(async () => {
    if (!jobId) return;
    try {
      setLoading(true);
      setError(null);
      const [rankingsData, jobData] = await Promise.all([
        api.getRankings(jobId),
        api.getJob(jobId),
      ]);
      setRankings(Array.isArray(rankingsData) ? rankingsData : rankingsData.rankings || []);
      setJob(jobData);
    } catch (err) {
      setError(err.message || 'Failed to fetch rankings');
    } finally {
      setLoading(false);
    }
  }, [jobId]);

  const computeRankings = useCallback(async () => {
    if (!jobId) return;
    try {
      setComputing(true);
      setError(null);
      await api.computeRankings(jobId);
      await fetchRankings();
    } catch (err) {
      setError(err.message || 'Failed to compute rankings');
      throw err;
    } finally {
      setComputing(false);
    }
  }, [jobId, fetchRankings]);

  const exportCSV = useCallback(async () => {
    if (!jobId) return;
    try {
      setError(null);
      const response = await api.exportCSV(jobId);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `rankings-${jobId}.csv`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      setError(err.message || 'Failed to export CSV');
      throw err;
    }
  }, [jobId]);

  return { rankings, job, loading, computing, error, fetchRankings, computeRankings, exportCSV };
}

export default useRankings;
