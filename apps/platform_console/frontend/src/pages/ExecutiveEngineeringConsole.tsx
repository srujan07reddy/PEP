import { useState, useEffect } from 'react';
import InteractiveWorkflowDesigner from '../components/InteractiveWorkflowDesigner';
import EvolutionBlueprintDashboard from '../components/EvolutionBlueprintDashboard';

const tabs = [
  'Workflow Intelligence',
  'Architecture Analysis',
  'Executive Overview',
  'Domain Agents'
];

const roles = [
  { name: 'CIO', label: 'Chief Information Officer' },
  { name: 'CISO', label: 'Chief Info Security Officer' },
  { name: 'Enterprise Architect', label: 'Enterprise Architect' }
];

export default function ExecutiveEngineeringConsole() {
  const [activeTab, setActiveTab] = useState(tabs[0]);
  const [activeRole, setActiveRole] = useState(roles[0].name);
  const [liveWorkflows, setLiveWorkflows] = useState([]);

  useEffect(() => {
    // Fetch live workflows from the real LCS diffing engine
    fetch('http://localhost:8000/workflows/optimize_live', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({})
    })
    .then(res => res.json())
    .then(data => {
      if (data.optimized_workflows) {
        setLiveWorkflows(data.optimized_workflows);
      }
    })
    .catch(console.error);
  }, []);

  return (
    <div className="p-6 bg-white rounded-lg shadow-md h-full flex flex-col">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-slate-800">Executive Engineering Console</h2>
        <div className="flex items-center gap-2">
          <label htmlFor="role-select" className="text-sm font-medium text-gray-700">View As:</label>
          <select
            id="role-select"
            value={activeRole}
            onChange={(e) => setActiveRole(e.target.value)}
            className="border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          >
            {roles.map(role => (
              <option key={role.name} value={role.name}>{role.label}</option>
            ))}
          </select>
        </div>
      </div>
      
      {/* Tabs */}
      <div className="flex border-b border-gray-200 mb-6 overflow-x-auto">
        {tabs.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`whitespace-nowrap py-2 px-4 border-b-2 font-medium text-sm transition-colors ${
              activeTab === tab
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Tab Content Placeholder */}
      <div className="flex-1 overflow-auto bg-gray-50 p-6 rounded border border-gray-200">
        {activeTab === 'Workflow Intelligence' ? (
          <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-8">
            <h2 className="text-2xl font-bold mb-4">Workflow Intelligence & Optimization (Live LCS Diffing)</h2>
            <p className="text-gray-600 mb-6">
              Review live AI-optimized workflows against the compiled Organization Knowledge Model (OKM). 
              The backend Longest Common Subsequence (LCS) algorithm calculates exact missing and extra steps.
            </p>
            <InteractiveWorkflowDesigner workflows={liveWorkflows} />
          </div>
        ) : activeTab === 'Executive Overview' ? (
          <EvolutionBlueprintDashboard />
        ) : (
          <>
            <h3 className="text-xl font-semibold mb-2">{activeTab} View for {activeRole}</h3>
            <p className="text-gray-600">
              This dashboard presents data tailored to the {activeRole} persona.
              It integrates output from the Engineering Decision Board, displaying findings dynamically loaded from the active Domain Pack.
            </p>
          </>
        )}
      </div>
    </div>
  );
}
