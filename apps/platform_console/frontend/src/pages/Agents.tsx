import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getAgents, runAgent, getAgentDetails, getDomains, createDomain, createAgent, updateAgent, toggleAgent, deleteAgent } from '../lib/api';

export default function Agents() {
  const queryClient = useQueryClient();
  const { data: agents, isLoading: isLoadingAgents } = useQuery({ queryKey: ['agents'], queryFn: getAgents });
  const { data: domains, isLoading: isLoadingDomains } = useQuery({ queryKey: ['domains'], queryFn: getDomains });
  
  const [executionResult, setExecutionResult] = useState<any>(null);
  const [viewingAgentId, setViewingAgentId] = useState<string | null>(null);
  const [selectedDomain, setSelectedDomain] = useState<string>('');
  const [externalPath, setExternalPath] = useState<string>('');
  
  const [isCreatingProject, setIsCreatingProject] = useState(false);
  const [newProjectName, setNewProjectName] = useState('');
  
  const [newExternalPath, setNewExternalPath] = useState('');
  
  const [isCreatingAgent, setIsCreatingAgent] = useState(false);
  const [newAgentId, setNewAgentId] = useState('');
  
  const [isEditingAgent, setIsEditingAgent] = useState(false);
  const [editAgentCode, setEditAgentCode] = useState('');

  const { data: agentDetails, isLoading: isLoadingDetails } = useQuery({
    queryKey: ['agentDetails', viewingAgentId],
    queryFn: () => getAgentDetails(viewingAgentId!),
    enabled: !!viewingAgentId
  });

  // Populate edit box when entering edit mode
  useEffect(() => {
    if (isEditingAgent && agentDetails) {
      setEditAgentCode(agentDetails.code);
    }
  }, [isEditingAgent, agentDetails]);

  // Auto-select first domain if none is selected
  useEffect(() => {
    if (domains && domains.length > 0 && !selectedDomain) {
      setSelectedDomain(domains[0].id);
    }
  }, [domains, selectedDomain]);

  // Auto-populate external path if the selected domain has one registered
  useEffect(() => {
    if (domains && selectedDomain) {
      const domainObj = domains.find((d: any) => d.id === selectedDomain);
      if (domainObj && domainObj.absolute_path) {
        setExternalPath(domainObj.absolute_path);
      } else {
        setExternalPath('');
      }
    }
  }, [selectedDomain, domains]);

  const createProjectMutation = useMutation({
    mutationFn: ({ name, absolutePath }: { name: string, absolutePath?: string }) => createDomain(name, absolutePath),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['domains'] });
      setSelectedDomain(data.id);
      setIsCreatingProject(false);
      setNewProjectName('');
      setNewExternalPath('');
    }
  });

  const createAgentMutation = useMutation({
    mutationFn: createAgent,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['agents'] });
      setIsCreatingAgent(false);
      setNewAgentId('');
      setViewingAgentId(data.id);
      setIsEditingAgent(true);
    }
  });

  const updateAgentMutation = useMutation({
    mutationFn: ({ id, code }: { id: string, code: string }) => updateAgent(id, code),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['agentDetails', viewingAgentId] });
      setIsEditingAgent(false);
    }
  });

  const runMutation = useMutation({
    mutationFn: runAgent,
    onSuccess: (data) => {
      setExecutionResult(data);
    }
  });

  const handleSaveResult = () => {
    if (!executionResult) return;
    const blob = new Blob([JSON.stringify(executionResult, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `execution_result_${executionResult.agent_id}_${executionResult.pipeline_id}.json`;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => {
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }, 100);
  };

  const toggleAgentMutation = useMutation({
    mutationFn: ({ id, status }: { id: string, status: 'active' | 'disabled' }) => toggleAgent(id, status),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['agents'] });
    }
  });

  const deleteAgentMutation = useMutation({
    mutationFn: (id: string) => deleteAgent(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['agents'] });
    }
  });

  if (isLoadingAgents || isLoadingDomains) return <div className="text-gray-500">Loading...</div>;

  return (
    <div>
      <div className="flex justify-between items-start mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Governance Agents</h1>
        
        <div className="flex flex-col space-y-2 items-end">
          <div className="flex items-center space-x-3 bg-white px-4 py-2 rounded-lg shadow-sm border border-gray-200">
            <label className="text-sm font-semibold text-gray-600">Target Project:</label>
            <div className="flex items-center space-x-2">
              <select 
                value={selectedDomain}
                onChange={(e) => {
                  setSelectedDomain(e.target.value);
                }}
                className="text-sm bg-gray-50 border border-gray-300 rounded-md px-3 py-1.5 outline-none focus:ring-2 focus:ring-slate-900"
              >
                {domains?.map((d: any) => (
                  <option key={d.id} value={d.id}>{d.name}</option>
                ))}
              </select>
              <button 
                onClick={() => setIsCreatingProject(true)}
                className="bg-indigo-600 hover:bg-indigo-700 text-white p-1.5 rounded-md flex items-center justify-center transition-colors"
                title="Add New Project"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
              </button>
            </div>
          </div>
          
          <div className="flex items-center space-x-3 bg-white px-4 py-2 rounded-lg shadow-sm border border-gray-200 w-full max-w-sm">
            <label className="text-sm font-semibold text-gray-600 whitespace-nowrap">External Path:</label>
            <input 
              type="text"
              value={externalPath}
              onChange={(e) => setExternalPath(e.target.value)}
              placeholder="e.g. D:\University_ERP"
              className="w-full text-sm bg-gray-50 border border-gray-300 rounded-md px-3 py-1.5 outline-none focus:ring-2 focus:ring-slate-900"
            />
          </div>
          
          <div className="flex space-x-2 mt-2">
            <button 
              onClick={() => setIsCreatingAgent(true)}
              className="text-sm bg-gray-800 hover:bg-gray-900 text-white px-4 py-1.5 rounded-md shadow-sm transition-colors w-full text-center"
            >
              + Custom Agent
            </button>
            <button 
              onClick={() => runMutation.mutate({ 
                agentId: 'all', 
                targetDomain: selectedDomain,
                absolutePath: externalPath.trim() || undefined
              })}
              disabled={runMutation.isPending}
              className="text-sm bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-1.5 rounded-md shadow-sm transition-colors w-full text-center disabled:opacity-50"
            >
              {runMutation.isPending && runMutation.variables?.agentId === 'all' ? 'Running...' : 'Execute All'}
            </button>
          </div>
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden mb-8">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-gray-50 border-b border-gray-200">
              <th className="p-4 font-semibold text-gray-600">Agent ID</th>
              <th className="p-4 font-semibold text-gray-600">Status</th>
              <th className="p-4 font-semibold text-gray-600 text-right">Action</th>
            </tr>
          </thead>
          <tbody>
            {agents?.map((a: any) => (
              <tr key={a.id} className="border-b border-gray-100 last:border-0 hover:bg-gray-50 transition-colors">
                <td className="p-4 font-mono text-gray-700">{a.id}</td>
                <td className="p-4">
                  <span className={`px-2 py-1 rounded text-xs font-semibold ${a.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                    {a.status.toUpperCase()}
                  </span>
                </td>
                <td className="p-4 text-right space-x-2">
                  <button 
                    onClick={() => {
                      const newStatus = a.status === 'active' ? 'disabled' : 'active';
                      toggleAgentMutation.mutate({ id: a.id, status: newStatus });
                    }}
                    className={`${a.status === 'active' ? 'bg-orange-50 text-orange-600 hover:bg-orange-100 border-orange-200' : 'bg-green-50 text-green-600 hover:bg-green-100 border-green-200'} border px-3 py-1.5 rounded-md text-sm font-medium transition-colors`}
                    disabled={toggleAgentMutation.isPending && toggleAgentMutation.variables?.id === a.id}
                  >
                    {a.status === 'active' ? 'Disable' : 'Enable'}
                  </button>
                  <button 
                    onClick={() => {
                      setViewingAgentId(a.id);
                      setIsEditingAgent(false);
                    }}
                    className="bg-white border border-gray-300 hover:bg-gray-50 text-gray-700 px-4 py-1.5 rounded-md text-sm font-medium transition-colors"
                  >
                    View Code
                  </button>
                  <button 
                    onClick={() => {
                      if (window.confirm(`Are you sure you want to delete agent ${a.id}?`)) {
                        deleteAgentMutation.mutate(a.id);
                      }
                    }}
                    className="bg-red-50 border border-red-200 hover:bg-red-100 text-red-700 px-4 py-1.5 rounded-md text-sm font-medium transition-colors"
                    disabled={deleteAgentMutation.isPending && deleteAgentMutation.variables === a.id}
                  >
                    {deleteAgentMutation.isPending && deleteAgentMutation.variables === a.id ? 'Deleting...' : 'Delete'}
                  </button>
                  <button 
                    onClick={() => runMutation.mutate({ 
                      agentId: a.id, 
                      targetDomain: selectedDomain,
                      absolutePath: externalPath.trim() || undefined
                    })}
                    disabled={a.status !== 'active' || runMutation.isPending}
                    className="bg-slate-900 hover:bg-slate-800 disabled:bg-slate-300 disabled:cursor-not-allowed text-white px-4 py-1.5 rounded-md text-sm font-medium transition-colors"
                  >
                    {runMutation.isPending && runMutation.variables?.agentId === a.id ? 'Running...' : 'Execute'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {executionResult && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden mb-8">
          <div className="p-4 border-b border-gray-100 flex justify-between items-center bg-gray-50">
            <h3 className="font-semibold text-gray-800 flex items-center">
              Execution Result: {executionResult.agent_id}
              <span className="ml-3 px-2.5 py-1 text-xs font-medium bg-indigo-100 text-indigo-800 rounded-full font-mono">
                {executionResult.target_ref}
              </span>
            </h3>
            <div className="flex items-center space-x-3">
              <button 
                onClick={handleSaveResult}
                className="text-xs bg-gray-200 hover:bg-gray-300 text-gray-700 px-3 py-1 rounded transition-colors font-semibold"
              >
                Save JSON
              </button>
              <button 
                onClick={() => setExecutionResult(null)}
                className="text-xs bg-gray-200 hover:bg-gray-300 text-gray-700 px-3 py-1 rounded transition-colors font-semibold"
              >
                Clear
              </button>
              <span className={`px-3 py-1 rounded-full text-sm font-bold ${executionResult.status === 'PASS' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                {executionResult.status}
              </span>
            </div>
          </div>

          <div className="p-6">
            {executionResult.logs && executionResult.logs.length > 0 && (
              <div className="mb-6">
                <h3 className="font-semibold text-gray-700 mb-2">Execution Terminal:</h3>
                <div className="bg-slate-900 rounded-md p-4 font-mono text-sm overflow-x-auto">
                  {executionResult.logs.map((log: string, idx: number) => {
                    let color = "text-gray-300";
                    if (log.includes("[ERROR]") || log.includes("[!]")) color = "text-red-400 font-bold";
                    if (log.includes("[OK]")) color = "text-green-400 font-bold";
                    if (log.startsWith && log.startsWith("---")) color = "text-blue-400 font-bold";
                    return (
                      <div key={idx} className={`${color} mb-1 whitespace-pre-wrap`}>
                        {log}
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          
            {executionResult.findings?.length > 0 ? (
              <div className="space-y-4">
                <h3 className="font-semibold text-gray-700">Findings:</h3>
                {executionResult.findings.map((f: any, idx: number) => (
                  <div key={idx} className="border-l-4 border-red-500 bg-red-50 p-4 rounded-r-md">
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-bold text-red-900">{f.title}</h4>
                      <span className="text-xs bg-red-200 text-red-900 px-2 py-0.5 rounded font-mono">{f.severity}</span>
                    </div>
                    <p className="text-sm text-red-800 mb-2">{f.description}</p>
                    <div className="text-xs text-red-700 font-mono mb-2">Location: {f.location?.file_path}</div>
                    <p className="text-sm font-medium text-red-900">Recommendation: {f.recommendation}</p>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-green-700 bg-green-50 p-4 rounded-md border border-green-200">
                No architectural violations found. Codebase is clean!
              </div>
            )}
          </div>
        </div>
      )}

      {/* Agent Details / Edit Modal */}
      {viewingAgentId && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-5xl max-h-[90vh] flex flex-col">
            <div className="p-6 border-b border-gray-200 flex justify-between items-center bg-gray-50 rounded-t-lg">
              <h2 className="text-2xl font-bold text-gray-800">Agent Source: {viewingAgentId}</h2>
              <div className="space-x-2">
                {!isEditingAgent && (
                  <button 
                    onClick={() => setIsEditingAgent(true)}
                    className="bg-indigo-50 hover:bg-indigo-100 text-indigo-700 px-4 py-1.5 rounded-md text-sm font-semibold transition-colors"
                  >
                    Edit Code
                  </button>
                )}
                <button 
                  onClick={() => {
                    setViewingAgentId(null);
                    setIsEditingAgent(false);
                  }}
                  className="text-gray-500 hover:text-gray-800 font-bold text-xl"
                >
                  &times;
                </button>
              </div>
            </div>
            
            <div className="p-6 overflow-y-auto flex-1 flex flex-col">
              {isLoadingDetails ? (
                <div className="text-gray-500">Loading agent source code...</div>
              ) : agentDetails ? (
                <div className="flex-1 flex flex-col">
                  <div className="mb-6 shrink-0">
                    <h3 className="text-lg font-semibold text-gray-800 mb-3">Core Functionalities</h3>
                    <div className="flex flex-wrap gap-2">
                      {agentDetails.functionalities?.map((func: string, idx: number) => (
                        <span key={idx} className="bg-indigo-100 text-indigo-800 px-3 py-1 rounded-full text-sm font-medium">
                          {func}
                        </span>
                      ))}
                    </div>
                  </div>
                  
                  <div className="flex-1 flex flex-col min-h-0">
                    <h3 className="text-lg font-semibold text-gray-800 mb-3 shrink-0">Python Implementation</h3>
                    {isEditingAgent ? (
                      <textarea
                        value={editAgentCode}
                        onChange={(e) => setEditAgentCode(e.target.value)}
                        className="flex-1 bg-slate-900 text-gray-300 font-mono text-sm p-4 rounded-lg outline-none focus:ring-2 focus:ring-indigo-500 w-full resize-none min-h-[400px]"
                        spellCheck={false}
                      />
                    ) : (
                      <div className="bg-slate-900 rounded-lg p-4 overflow-y-auto flex-1 min-h-[400px]">
                        <pre className="text-gray-300 text-sm font-mono leading-relaxed">
                          <code>{agentDetails.code || "Code not available."}</code>
                        </pre>
                      </div>
                    )}
                  </div>
                </div>
              ) : (
                <div className="text-red-500">Failed to load agent details.</div>
              )}
            </div>
            
            <div className="p-4 border-t border-gray-200 bg-gray-50 rounded-b-lg flex justify-end space-x-3 shrink-0">
              <button 
                onClick={() => {
                  setViewingAgentId(null);
                  setIsEditingAgent(false);
                }}
                className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded-md text-sm font-medium transition-colors"
              >
                Close
              </button>
              {isEditingAgent && (
                <button 
                  onClick={() => updateAgentMutation.mutate({ id: viewingAgentId, code: editAgentCode })}
                  disabled={updateAgentMutation.isPending}
                  className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors disabled:opacity-50"
                >
                  {updateAgentMutation.isPending ? 'Saving...' : 'Save Changes'}
                </button>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Create Project Modal */}
      {isCreatingProject && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-md flex flex-col">
            <div className="p-5 border-b border-gray-200">
              <h2 className="text-xl font-bold text-gray-800">Create New Project</h2>
            </div>
            
            <div className="p-5">
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Project Name</label>
                <input 
                  type="text" 
                  value={newProjectName}
                  onChange={(e) => setNewProjectName(e.target.value)}
                  placeholder="e.g. Hospital ERP"
                  className="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-slate-900"
                  autoFocus
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">External Path (Optional)</label>
                <input 
                  type="text" 
                  value={newExternalPath}
                  onChange={(e) => setNewExternalPath(e.target.value)}
                  placeholder="e.g. D:\University_ERP"
                  className="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-slate-900"
                />
                <p className="text-xs text-gray-500 mt-2">
                  If provided, this registers a local folder as a project. The agent will run against your external code instead of a platform workspace.
                </p>
              </div>
            </div>
            
            <div className="p-4 border-t border-gray-200 bg-gray-50 rounded-b-lg flex justify-end space-x-2">
              <button 
                onClick={() => {
                  setIsCreatingProject(false);
                  setNewProjectName('');
                  setNewExternalPath('');
                }}
                className="bg-white border border-gray-300 hover:bg-gray-50 text-gray-700 px-4 py-2 rounded-md text-sm font-medium transition-colors"
              >
                Cancel
              </button>
              <button 
                onClick={() => {
                  if (newProjectName.trim()) {
                    createProjectMutation.mutate({ 
                      name: newProjectName, 
                      absolutePath: newExternalPath.trim() || undefined 
                    });
                  }
                }}
                disabled={!newProjectName.trim() || createProjectMutation.isPending}
                className="bg-slate-900 hover:bg-slate-800 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors disabled:opacity-50"
              >
                Create Project
              </button>
            </div>
          </div>
        </div>
      )}
      
      {/* Create Agent Modal */}
      {isCreatingAgent && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-md flex flex-col">
            <div className="p-5 border-b border-gray-200">
              <h2 className="text-xl font-bold text-gray-800">Create Custom Agent</h2>
            </div>
            
            <div className="p-5">
              <label className="block text-sm font-medium text-gray-700 mb-1">Agent ID</label>
              <input 
                type="text" 
                value={newAgentId}
                onChange={(e) => setNewAgentId(e.target.value)}
                placeholder="e.g. custom-linter-agent"
                className="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-slate-900"
                autoFocus
              />
              <p className="text-xs text-gray-500 mt-2">
                This will automatically generate a boilerplate python script and dynamically load it into the orchestrator pipeline.
              </p>
              {createAgentMutation.isError && (
                <p className="text-sm text-red-600 mt-2">Error creating agent. Ensure ID is unique.</p>
              )}
            </div>
            
            <div className="p-4 border-t border-gray-200 bg-gray-50 rounded-b-lg flex justify-end space-x-2">
              <button 
                onClick={() => {
                  setIsCreatingAgent(false);
                  setNewAgentId('');
                }}
                className="bg-white border border-gray-300 hover:bg-gray-50 text-gray-700 px-4 py-2 rounded-md text-sm font-medium transition-colors"
              >
                Cancel
              </button>
              <button 
                onClick={() => {
                  if (newAgentId.trim()) {
                    createAgentMutation.mutate(newAgentId);
                  }
                }}
                disabled={!newAgentId.trim() || createAgentMutation.isPending}
                className="bg-slate-900 hover:bg-slate-800 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors disabled:opacity-50"
              >
                {createAgentMutation.isPending ? 'Creating...' : 'Create & Edit'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
