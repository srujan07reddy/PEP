import { useState } from 'react';
import { ShieldAlert, AlertTriangle, AlertCircle, Play } from 'lucide-react';

export default function ValidationReport({ orgName = "mock_org" }: any) {
  const [loading, setLoading] = useState(false);
  const [issues, setIssues] = useState<any[] | null>(null);

  const runValidation = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/organization/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ org_name: orgName, industry: "Enterprise" })
      });
      const data = await response.json();
      setIssues(data.issues);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex justify-between items-start mb-6">
        <div>
          <h2 className="text-xl font-bold flex items-center gap-2">
            <ShieldAlert className="text-red-500" /> Graph Validation Engine
          </h2>
          <p className="text-sm text-gray-500 mt-1">
            Executes advanced graph theory algorithms (like Depth-First Search) over the OKG to detect 
            orphaned nodes, broken hierarchies, and circular dependencies before they hit the ERP layer.
          </p>
        </div>
        <button 
          onClick={runValidation}
          disabled={loading}
          className="bg-gray-800 hover:bg-black text-white px-4 py-2 rounded shadow flex items-center gap-2 disabled:opacity-50"
        >
          {loading ? <Play className="animate-pulse w-4 h-4" /> : <Play className="w-4 h-4" />}
          Run DFS Validation
        </button>
      </div>

      {issues && issues.length > 0 ? (
        <div className="space-y-4">
          <h3 className="font-semibold text-gray-700">Detected Issues ({issues.length})</h3>
          {issues.map((issue, idx) => (
            <div key={idx} className={`p-4 rounded border-l-4 flex gap-3 ${issue.severity === 'high' ? 'bg-red-50 border-red-500 text-red-900' : 'bg-yellow-50 border-yellow-500 text-yellow-900'}`}>
              <div className="pt-0.5">
                {issue.severity === 'high' ? <AlertCircle className="w-5 h-5 text-red-500" /> : <AlertTriangle className="w-5 h-5 text-yellow-600" />}
              </div>
              <div>
                <div className="font-bold text-sm uppercase tracking-wide opacity-80">{issue.type}</div>
                <div className="mt-1">{issue.message}</div>
              </div>
            </div>
          ))}
        </div>
      ) : issues && issues.length === 0 ? (
        <div className="p-8 text-center text-gray-500 border border-dashed rounded">
          No validation issues found in the graph.
        </div>
      ) : (
        <div className="p-8 text-center text-gray-400 border border-dashed rounded bg-gray-50">
          Validation has not been run yet.
        </div>
      )}
    </div>
  );
}
