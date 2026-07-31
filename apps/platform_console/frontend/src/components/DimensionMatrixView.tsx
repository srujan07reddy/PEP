import { Activity } from 'lucide-react';

export default function DimensionMatrixView({ blueprint }: any) {
  const recommendations = blueprint.recommendation_matrix || [];

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-8">
      <h2 className="text-xl font-bold flex items-center gap-2 text-slate-800 mb-6">
        <Activity className="text-purple-600" /> Dimension Impact Scorecards
      </h2>
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b-2 border-gray-100 text-gray-500 text-sm">
              <th className="py-3 px-4 font-semibold w-1/3">Recommendation</th>
              <th className="py-3 px-4 font-semibold">Priority & ROI</th>
              <th className="py-3 px-4 font-semibold">Dimensions Impacted</th>
            </tr>
          </thead>
          <tbody>
            {recommendations.map((rec: any, idx: number) => (
              <tr key={idx} className="border-b border-gray-50 hover:bg-gray-50 transition-colors">
                <td className="py-4 px-4 align-top">
                  <div className="font-semibold text-slate-800 text-sm mb-1">{rec.title}</div>
                  <div className="text-xs text-gray-500 line-clamp-2">{rec.summary}</div>
                  <div className="mt-2 flex flex-wrap gap-1">
                    {rec.applicable_engineering_principles?.map((p: string, i: number) => (
                      <span key={i} className="text-[10px] bg-purple-50 text-purple-700 px-2 py-0.5 rounded border border-purple-100">{p}</span>
                    ))}
                  </div>
                </td>
                <td className="py-4 px-4 align-top">
                  <div className="flex flex-col gap-2">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium w-fit
                      ${rec.priority?.level === 'Critical' ? 'bg-red-100 text-red-800' : 
                        rec.priority?.level === 'High' ? 'bg-orange-100 text-orange-800' : 'bg-blue-100 text-blue-800'}`}>
                      {rec.priority?.level} Priority
                    </span>
                    <span className="text-xs font-mono text-gray-600 font-semibold mt-1">
                      ROI: {rec.business_impact?.expected_roi || 'N/A'}
                    </span>
                    <span className="text-xs text-gray-500">
                      Effort: {rec.business_impact?.engineering_effort || 'N/A'}
                    </span>
                  </div>
                </td>
                <td className="py-4 px-4 align-top">
                  <div className="flex flex-wrap gap-2">
                    {Object.entries(rec.dimension_scorecard?.dimension_scores || {}).map(([dim, score]: [string, any], i: number) => (
                      <div key={i} className={`flex items-center border rounded-md overflow-hidden text-xs font-medium
                        ${score > 0 ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'}`}>
                        <span className="px-2 py-1 text-slate-700 border-r border-inherit bg-white/50">{dim}</span>
                        <span className={`px-2 py-1 font-mono ${score > 0 ? 'text-green-700' : 'text-red-700'}`}>
                          {score > 0 ? '+' : ''}{score}
                        </span>
                      </div>
                    ))}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
