import { useState, useEffect, useCallback } from 'react';
import api from '../services/api';

export function useJobs() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchJobs = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getJobs();
      setJobs(Array.isArray(data) ? data : data.jobs || []);
    } catch (err) {
      setError(err.message || 'Failed to fetch jobs');
    } finally {
      setLoading(false);
    }
  }, []);

  const createJob = useCallback(async (jobData) => {
    try {
      setError(null);
      const newJob = await api.createJob(jobData);
      setJobs((prev) => [newJob, ...prev]);
      return newJob;
    } catch (err) {
      setError(err.message || 'Failed to create job');
      throw err;
    }
  }, []);

  const deleteJob = useCallback(async (id) => {
    try {
      setError(null);
      await api.deleteJob(id);
      setJobs((prev) => prev.filter((job) => job.id !== id));
    } catch (err) {
      setError(err.message || 'Failed to delete job');
      throw err;
    }
  }, []);

  useEffect(() => {
    fetchJobs();
  }, [fetchJobs]);

  return { jobs, loading, error, fetchJobs, createJob, deleteJob };
}

export default useJobs;
