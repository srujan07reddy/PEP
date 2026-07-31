import { useState } from 'react';
import { GitCompare, CheckCircle, XCircle, Download } from 'lucide-react';

export default function InteractiveWorkflowDesigner({ workflows = [] }: { workflows?: any[] }) {
  const [selectedWorkflow, setSelectedWorkflow] = useState<any>(null);

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden flex h-[600px]">
      {/* Sidebar */}
      <div className="w-1/3 border-r border-gray-200 bg-gray-50 flex flex-col">
        <div className="p-4 border-b border-gray-200 bg-white">
          <h3 className="font-bold text-gray-800">Optimized Workflows</h3>
          <p className="text-xs text-gray-500">Human-in-the-Loop Review Required</p>
        </div>
        <div className="flex-1 overflow-auto p-2 space-y-2">
          {workflows.map((wf, idx) => (
            <button 
              key={idx}
              onClick={() => setSelectedWorkflow(wf)}
              className={`w-full text-left p-3 rounded border transition-colors ${selectedWorkflow?.id === wf.id ? 'bg-blue-50 border-blue-200' : 'bg-white border-gray-200 hover:border-blue-300'}`}
            >
              <div className="font-semibold text-gray-800 text-sm">{wf.name || "Unknown Workflow"}</div>
              <div className="flex justify-between items-center mt-2">
                <span className="text-xs px-2 py-0.5 bg-yellow-100 text-yellow-800 rounded">Pending Review</span>
                <span className="text-xs font-mono text-gray-500">-{wf.expected_time_reduction || '0%'} time</span>
              </div>
            </button>
          ))}
          {workflows.length === 0 && (
            <div className="p-4 text-sm text-gray-500 text-center">No workflows pending review.</div>
          )}
        </div>
      </div>

      {/* Main Area */}
      <div className="w-2/3 flex flex-col bg-white">
        {selectedWorkflow ? (
          <>
            <div className="p-4 border-b border-gray-200 flex justify-between items-center bg-gray-50">
              <h3 className="font-bold text-gray-800 flex items-center gap-2">
                <GitCompare className="w-5 h-5 text-blue-600" />
                Workflow Comparison
              </h3>
              <div className="flex gap-2">
                <button className="px-3 py-1.5 text-sm bg-green-600 hover:bg-green-700 text-white rounded flex items-center gap-1 font-medium transition-colors">
                  <CheckCircle className="w-4 h-4" /> Approve
                </button>
                <button className="px-3 py-1.5 text-sm bg-red-50 hover:bg-red-100 text-red-600 rounded flex items-center gap-1 font-medium transition-colors">
                  <XCircle className="w-4 h-4" /> Reject
                </button>
                <button className="px-3 py-1.5 text-sm border border-gray-300 hover:bg-gray-100 text-gray-700 rounded flex items-center gap-1 font-medium transition-colors">
                  <Download className="w-4 h-4" /> BPMN
                </button>
              </div>
            </div>
            
            <div className="flex-1 overflow-auto p-6 flex flex-col gap-6">
              <div className="grid grid-cols-2 gap-6">
                <div className="border border-gray-200 rounded-lg p-4 bg-gray-50">
                  <h4 className="font-semibold text-gray-700 mb-3 flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-red-500"></span> Current Implementation
                  </h4>
                  <ul className="text-sm space-y-2 text-gray-600 list-disc pl-4">
                    {selectedWorkflow.problems_detected?.map((p: string, i: number) => <li key={i}>{p}</li>)}
                  </ul>
                  <div className="mt-4 p-4 border border-dashed border-gray-300 rounded text-center text-gray-400 font-mono text-xs">
                    (Mermaid Graph Render)
                  </div>
                </div>
                
                <div className="border border-green-200 rounded-lg p-4 bg-green-50">
                  <h4 className="font-semibold text-green-800 mb-3 flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-green-500"></span> AI Optimized Target
                  </h4>
                  <ul className="text-sm space-y-2 text-green-700 list-disc pl-4">
                    {selectedWorkflow.optimized_steps?.map((s: string, i: number) => <li key={i}>{s}</li>)}
                  </ul>
                  <div className="mt-4 p-4 border border-dashed border-green-300 rounded text-center text-green-600 font-mono text-xs">
                    {selectedWorkflow.mermaid_graph || "(Mermaid Graph Render)"}
                  </div>
                </div>
              </div>
              
              <div className="border border-gray-200 rounded-lg p-4">
                <h4 className="font-semibold text-gray-800 mb-3">AI & Automation Opportunities</h4>
                <div className="flex flex-wrap gap-2">
                  {selectedWorkflow.automation_opportunities?.map((opp: string, i: number) => (
                    <span key={i} className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-xs font-medium border border-purple-200">
                      ⚡ {opp}
                    </span>
                  ))}
                  {selectedWorkflow.ai_opportunities?.map((opp: string, i: number) => (
                    <span key={i} className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-medium border border-blue-200">
                      🧠 {opp}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center text-gray-400">
            <div className="text-center">
              <GitCompare className="w-12 h-12 mx-auto mb-3 opacity-20" />
              <p>Select a workflow to review changes</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
