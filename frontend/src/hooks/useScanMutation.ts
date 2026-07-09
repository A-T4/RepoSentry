import { useMutation } from '@tanstack/react-query';

export const useScanMutation = () => {
  return useMutation({
    mutationFn: async (repoUrl: string) => {
      console.log("Sending request to backend for:", repoUrl);
      
      // Dynamic base URL fallback pattern for production vs local development
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      
      const response = await fetch(`${API_BASE_URL}/api/v1/analyze/`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ repository_url: repoUrl }),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        console.error("Backend error:", data);
        throw new Error(data.detail || 'Scan failed.');
      }
      
      console.log("Scan results received:", data);
      return data;
    },
  });
};