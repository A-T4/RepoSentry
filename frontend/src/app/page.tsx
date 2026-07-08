'use client';

import { useState } from 'react';
// The alias @/ maps to the /src directory automatically in Next.js
import { useScanMutation } from '@/hooks/useScanMutation';
import { ScoreCard } from './components/dashboard/ScoreCard';
import { FindingsTable } from './components/dashboard/FindingsTable';

export default function Dashboard() {
  const [url, setUrl] = useState('');
  const scanMutation = useScanMutation();

  return (
    <main className="min-h-screen bg-black text-white p-8">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">RepoSentry Dashboard</h1>
        
        <div className="flex gap-4 mb-8">
          <input 
            className="flex-1 bg-zinc-900 border border-zinc-800 p-2 rounded text-white"
            placeholder="https://github.com/user/repo"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
          <button 
            className="bg-blue-600 px-6 py-2 rounded font-bold"
            onClick={() => scanMutation.mutate(url)}
            disabled={scanMutation.isPending}
          >
            {scanMutation.isPending ? 'Analyzing...' : 'Analyze'}
          </button>
        </div>

        {scanMutation.data && (
          <>
            <div className="grid grid-cols-5 gap-4 mb-8">
              {scanMutation.data.category_scores.map((cs: any) => (
                <ScoreCard key={cs.category} title={cs.category} score={cs.score} reasoning={cs.reasoning} />
              ))}
            </div>
            <FindingsTable findings={scanMutation.data.findings} />
          </>
        )}
      </div>
    </main>
  );
}