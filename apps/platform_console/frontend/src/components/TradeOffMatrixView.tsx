import { Scale, CheckCircle2, AlertOctagon } from 'lucide-react';

export default function TradeOffMatrixView({ blueprint }: any) {
  const recommendations = blueprint.recommendation_matrix || [];

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-8">
      <h2 className="text-xl font-bold flex items-center gap-2 text-slate-800 mb-6">
        <Scale className="text-orange-500" /> Engineering Trade-Off Matrix
      </h2>
      <div className="space-y-6">
        {recommendations.map((rec: any, idx: number) => {
          const tradeoffs = rec.trade_offs || [];
          if (tradeoffs.length === 0) return null;

          return (
            <div key={idx} className="border border-gray-200 rounded-lg overflow-hidden">
              <div className="bg-gray-50 px-4 py-3 border-b border-gray-200">
                <h3 className="font-semibold text-slate-800 text-sm">{rec.title}</h3>
              </div>
              <div className="divide-y divide-gray-100">
                {tradeoffs.map((tradeoff: any, tIdx: number) => (
                  <div key={tIdx} className="flex flex-col md:flex-row">
                    {/* Benefits side */}
                    <div className="flex-1 p-4 bg-white hover:bg-green-50/30 transition-colors md:border-r border-gray-100">
                      <div className="flex items-start gap-3">
                        <CheckCircle2 className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                        <div>
                          <div className="text-xs font-bold text-green-700 uppercase tracking-wide mb-1">Benefit Identified</div>
                          <p className="text-sm text-gray-700">{tradeoff.benefit}</p>
                        </div>
                      </div>
                    </div>
                    {/* Drawbacks side */}
                    <div className="flex-1 p-4 bg-white hover:bg-orange-50/30 transition-colors">
                      <div className="flex items-start gap-3">
                        <AlertOctagon className="w-5 h-5 text-orange-500 mt-0.5 flex-shrink-0" />
                        <div>
                          <div className="text-xs font-bold text-orange-700 uppercase tracking-wide mb-1">Risk / Drawback Accepted</div>
                          <p className="text-sm text-gray-700">{tradeoff.drawback}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
