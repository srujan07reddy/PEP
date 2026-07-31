import { Target, TrendingUp, AlertTriangle } from 'lucide-react';

export default function MaturityScorecard({ maturityAssessment }: any) {
  const current = maturityAssessment.current_maturity;
  const projected = maturityAssessment.projected_maturity;
  
  const dimensions = [
    { key: 'organization_alignment', label: 'Org Alignment' },
    { key: 'workflow_alignment', label: 'Workflow' },
    { key: 'architecture_quality', label: 'Architecture' },
    { key: 'governance_quality', label: 'Governance' },
    { key: 'data_quality', label: 'Data Quality' },
    { key: 'ai_readiness', label: 'AI Readiness' },
    { key: 'integration_quality', label: 'Integration' },
    { key: 'reliability', label: 'Reliability' },
    { key: 'maintainability', label: 'Maintainability' },
  ];

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-8">
      <div className="flex justify-between items-center mb-6 border-b border-gray-100 pb-4">
        <div>
          <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-800">
            <Target className="text-blue-600" /> Engineering Maturity Assessment (EMA)
          </h2>
          <p className="text-sm text-gray-500 mt-1">Current software capabilities vs OKM projected potential.</p>
        </div>
        <div className="flex gap-4">
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <div className="w-3 h-3 bg-gray-300 rounded-full"></div> Current
          </div>
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <div className="w-3 h-3 bg-green-500 rounded-full"></div> Projected
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {dimensions.map(dim => {
          const curScore = current[dim.key] || 0;
          const projScore = projected[dim.key] || 0;
          const improvement = projScore - curScore;
          
          return (
            <div key={dim.key} className="p-4 rounded-lg bg-gray-50 border border-gray-100 transition-all hover:shadow-md">
              <div className="flex justify-between items-center mb-2">
                <span className="font-semibold text-gray-700">{dim.label}</span>
                {improvement > 0 ? (
                  <span className="text-xs font-bold text-green-600 flex items-center gap-1 bg-green-100 px-2 py-1 rounded-full">
                    <TrendingUp className="w-3 h-3" /> +{improvement.toFixed(1)}
                  </span>
                ) : (
                  <span className="text-xs text-gray-400 bg-white border border-gray-200 px-2 py-1 rounded-full">Optimal</span>
                )}
              </div>
              
              <div className="relative pt-1">
                <div className="overflow-hidden h-2 mb-2 text-xs flex rounded bg-gray-200">
                  <div style={{ width: `${curScore}%` }} className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-gray-400 z-10 rounded-l"></div>
                  {improvement > 0 && (
                    <div style={{ width: `${improvement}%` }} className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-green-500 z-0"></div>
                  )}
                </div>
                <div className="flex justify-between text-xs text-gray-500 mt-1 font-mono">
                  <span>{curScore.toFixed(1)}</span>
                  {improvement > 0 && <span className="font-bold text-slate-800">{projScore.toFixed(1)}</span>}
                </div>
              </div>
            </div>
          );
        })}
      </div>
      
      {/* Evidence section */}
      {maturityAssessment.evidence && maturityAssessment.evidence.length > 0 && (
        <div className="mt-8 pt-6 border-t border-gray-100">
          <h3 className="text-lg font-semibold mb-4 text-slate-700">OKM Evidence Mapping</h3>
          <div className="space-y-3">
            {maturityAssessment.evidence.map((ev: any, idx: number) => (
              <div key={idx} className="flex gap-3 text-sm p-3 bg-blue-50/50 rounded-md border border-blue-100 text-blue-900">
                <AlertTriangle className="w-4 h-4 mt-0.5 text-blue-500 flex-shrink-0" />
                <div>
                  <span className="font-bold">{ev.dimension}:</span> {ev.explanation}
                  <div className="mt-1 text-xs text-blue-500 font-mono">
                    References: {ev.okm_references.join(", ")}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
