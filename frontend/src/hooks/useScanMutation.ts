import { useMutation } from '@tanstack/react-query';

export const useScanMutation = () => {
  return useMutation({
    mutationFn: async (repoUrl: string) => {
      // Prioritize the env var, but fallback to localhost:8000 for local dev
      const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      
      console.log("Connecting to API at:", baseUrl); // Add this log to verify
      
      const response = await fetch(`${baseUrl}/api/v1/analyze/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ repository_url: repoUrl }),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.detail || 'Scan failed.');
      }
      
      return data;
    },
  });
};