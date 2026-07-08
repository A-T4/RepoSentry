// ADD 'export' BEFORE 'const'
export const ScoreCard = ({ title, score, reasoning }: { title: string, score: number, reasoning: string }) => (
  <div className="bg-zinc-900 border border-zinc-800 p-4 rounded-lg">
    <div className="flex justify-between items-center mb-2">
      <h3 className="text-zinc-400 text-sm font-medium">{title}</h3>
      <span className="text-xl font-bold text-white">{score}</span>
    </div>
    <p className="text-zinc-500 text-xs">{reasoning}</p>
  </div>
);