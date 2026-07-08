export const FindingsTable = ({ findings }: { findings: any[] }) => {
  if (!findings || findings.length === 0) {
    return (
      <div className="mt-8 p-8 border border-dashed border-zinc-800 rounded-lg text-center text-zinc-500">
        No security findings detected. The repository appears clean!
      </div>
    );
  }

  return (
    <div className="mt-8">
      <h2 className="text-xl font-bold text-white mb-4">Security Findings</h2>
      <div className="space-y-3">
        {findings.map((f, i) => (
          <div key={i} className="bg-zinc-900 border border-zinc-800 p-4 rounded-lg flex items-start gap-4">
            <div className={`w-2 h-12 rounded ${f.severity === 'CRITICAL' ? 'bg-red-600' : 'bg-yellow-600'}`} />
            <div>
              <h4 className="text-white font-bold">{f.title}</h4>
              <p className="text-zinc-400 text-sm mt-1">{f.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};