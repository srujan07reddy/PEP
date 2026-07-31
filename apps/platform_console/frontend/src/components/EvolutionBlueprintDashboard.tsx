import { useState, useEffect } from 'react';
import MaturityScorecard from './MaturityScorecard';
import DimensionMatrixView from './DimensionMatrixView';
import TradeOffMatrixView from './TradeOffMatrixView';
import { Download, RefreshCcw, Briefcase } from 'lucide-react';

export default function EvolutionBlueprintDashboard() {
  const [blueprint, setBlueprint] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [filePath, setFilePath] = useState("");

  const fetchBlueprint = () => {
    setLoading(true);
    const url = filePath ? `http://localhost:8000/engineering/blueprint?filepath=${encodeURIComponent(filePath)}` : 'http://localhost:8000/engineering/blueprint';
    fetch(url)
      .then(res => res.json())
      .then(data => {
        setBlueprint(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to fetch blueprint:", err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchBlueprint();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-500">
        <RefreshCcw className="animate-spin w-6 h-6 mr-3" />
        Generating Executive Blueprint...
      </div>
    );
  }

  if (!blueprint) {
    return <div className="p-6 text-red-500">Failed to load Blueprint. Ensure the backend is running.</div>;
  }

  return (
    <div className="animate-fade-in pb-12">
      <div className="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 mb-2">Evolution Blueprint</h1>
          <p className="text-gray-600 max-w-3xl">{blueprint.executive_summary}</p>
        </div>
        <div className="flex flex-col gap-2 items-end">
          <div className="flex items-center gap-2">
            <input 
              type="text" 
              placeholder="Absolute path to OKM .json file" 
              value={filePath}
              onChange={(e) => setFilePath(e.target.value)}
              className="border border-gray-300 rounded-md px-3 py-2 text-sm w-64 focus:ring-blue-500 focus:border-blue-500"
            />
            <button 
              onClick={fetchBlueprint}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md font-medium text-sm transition-colors"
            >
              Run Analysis
            </button>
          </div>
          <button className="flex items-center gap-2 text-slate-600 hover:text-slate-900 px-2 py-1 rounded-lg font-medium transition-colors text-sm">
            <Download className="w-4 h-4" /> Export Report
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-100 rounded-xl p-6">
          <h3 className="text-blue-900 font-semibold mb-2 flex items-center gap-2">
            <Briefcase className="w-4 h-4" /> Business Alignment
          </h3>
          <p className="text-sm text-blue-800 leading-relaxed">{blueprint.business_alignment_summary}</p>
        </div>
        <div className="bg-gradient-to-br from-emerald-50 to-teal-50 border border-emerald-100 rounded-xl p-6">
          <h3 className="text-emerald-900 font-semibold mb-2 flex items-center gap-2">
            <Briefcase className="w-4 h-4" /> Organization Alignment
          </h3>
          <p className="text-sm text-emerald-800 leading-relaxed">{blueprint.organization_alignment_summary}</p>
        </div>
      </div>

      {blueprint.maturity_assessment && (
        <MaturityScorecard maturityAssessment={blueprint.maturity_assessment} />
      )}

      {blueprint.recommendation_matrix && (
        <DimensionMatrixView blueprint={blueprint} />
      )}

      {blueprint.trade_off_matrix && (
        <TradeOffMatrixView blueprint={blueprint} />
      )}
      
      {/* Roadmap section */}
      {blueprint.implementation_roadmap && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h2 className="text-xl font-bold text-slate-800 mb-6">Suggested Phased Roadmap</h2>
          <div className="space-y-4">
            {blueprint.implementation_roadmap.map((phase: any, i: number) => (
              <div key={i} className="flex gap-4">
                <div className="flex flex-col items-center">
                  <div className="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center font-bold text-slate-700">
                    {i+1}
                  </div>
                  {i < blueprint.implementation_roadmap.length - 1 && (
                    <div className="w-0.5 h-full bg-slate-100 mt-2"></div>
                  )}
                </div>
                <div className="pb-6 pt-1">
                  <h3 className="font-bold text-slate-800">{phase.name}</h3>
                  <p className="text-sm text-gray-500 mt-1">{phase.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
