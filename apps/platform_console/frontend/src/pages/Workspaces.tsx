import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getWorkspaces, createDomain, deleteDomain, runGeneration, runDeployment } from '../lib/api';
import { Trash2, FolderCode } from 'lucide-react';

export default function Workspaces() {
  const queryClient = useQueryClient();
  const { data: workspaces, isLoading } = useQuery({ queryKey: ['workspaces'], queryFn: getWorkspaces });

  const [isCreatingProject, setIsCreatingProject] = useState(false);
  const [newProjectName, setNewProjectName] = useState('');
  const [newExternalPath, setNewExternalPath] = useState('');

  const createProjectMutation = useMutation({
    mutationFn: ({ name, absolutePath }: { name: string, absolutePath?: string }) => createDomain(name, absolutePath),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['workspaces'] });
      setIsCreatingProject(false);
      setNewProjectName('');
      setNewExternalPath('');
    }
  });

  const deleteProjectMutation = useMutation({
    mutationFn: (workspaceId: string) => deleteDomain(workspaceId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['workspaces'] });
    }
  });

  const runGenerationMutation = useMutation({
    mutationFn: (targetDomain: string) => runGeneration({ targetDomain })
  });

  const runDeploymentMutation = useMutation({
    mutationFn: (targetDomain: string) => runDeployment({ targetDomain })
  });

  if (isLoading) return <div className="text-gray-500">Loading workspaces...</div>;

  return (
    <div>
      <div className="flex justify-between items-start mb-6">
        <div>
          <h1 className="text-3xl font-bold mb-2 text-gray-800">Code Workspaces</h1>
          <p className="text-gray-600 max-w-3xl">
            This view displays the active physical codebases managed by the <code className="bg-gray-100 px-1 py-0.5 rounded text-sm">WorkspaceRegistry</code>.
          </p>
        </div>
        
        <button 
          onClick={() => setIsCreatingProject(true)}
          className="text-sm bg-slate-900 hover:bg-slate-800 text-white px-4 py-2 rounded-md shadow-sm transition-colors shrink-0 flex items-center gap-2"
        >
          <FolderCode className="w-4 h-4" />
          Add New Workspace
        </button>
      </div>
      
      <div className="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-gray-50 border-b border-gray-200">
              <th className="p-4 font-semibold text-gray-600">Workspace ID</th>
              <th className="p-4 font-semibold text-gray-600">Name</th>
              <th className="p-4 font-semibold text-gray-600">Mapped Domain</th>
              <th className="p-4 font-semibold text-gray-600">External Path</th>
              <th className="p-4 font-semibold text-gray-600">Status</th>
              <th className="p-4 font-semibold text-gray-600 text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            {workspaces?.map((w: any) => (
              <tr key={w.id} className="border-b border-gray-100 last:border-0 hover:bg-gray-50 transition-colors">
                <td className="p-4 font-mono text-gray-700 text-sm">{w.id}</td>
                <td className="p-4 font-medium">{w.name}</td>
                <td className="p-4 text-gray-600 font-mono text-sm">
                  {w.mapped_domain !== 'None' ? (
                     <span className="bg-blue-50 text-blue-700 px-2 py-1 rounded">{w.mapped_domain}</span>
                  ) : (
                     <span className="text-gray-400 italic">None</span>
                  )}
                </td>
                <td className="p-4">
                  {w.absolute_path ? (
                    <span className="font-mono text-xs bg-indigo-50 text-indigo-700 px-2 py-1 rounded border border-indigo-100">
                      {w.absolute_path}
                    </span>
                  ) : (
                    <span className="text-gray-400 text-sm italic">Managed</span>
                  )}
                </td>
                <td className="p-4">
                  <span className={`px-2 py-1 rounded text-xs font-semibold ${w.status === 'ACTIVE' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                    {w.status}
                  </span>
                </td>
                <td className="p-4 text-right flex items-center justify-end gap-2">
                  <button
                    onClick={async () => {
                      if(window.confirm(`Deploy scaffolding for ${w.name}?`)) {
                        try {
                          await runDeploymentMutation.mutateAsync(w.mapped_domain);
                          alert('Deployment pipeline kicked off!');
                        } catch (e) {
                          alert('Deployment failed.');
                        }
                      }
                    }}
                    disabled={w.mapped_domain === 'None' || runDeploymentMutation.isPending}
                    className="text-xs bg-orange-100 hover:bg-orange-200 text-orange-700 px-3 py-1 rounded transition-colors disabled:opacity-50"
                  >
                    🚀 Deploy
                  </button>
                  <button
                    onClick={async () => {
                      if(window.confirm(`Generate scaffolding for ${w.name}?`)) {
                        try {
                          await runGenerationMutation.mutateAsync(w.mapped_domain);
                          alert('Generation pipeline kicked off!');
                        } catch (e) {
                          alert('Generation failed.');
                        }
                      }
                    }}
                    disabled={w.mapped_domain === 'None' || runGenerationMutation.isPending}
                    className="text-xs bg-purple-100 hover:bg-purple-200 text-purple-700 px-3 py-1 rounded transition-colors disabled:opacity-50"
                  >
                    ⚡ Generate
                  </button>
                  <button 
                    onClick={() => {
                      if(window.confirm(`Are you sure you want to remove ${w.name}?`)) {
                        deleteProjectMutation.mutate(w.id);
                      }
                    }}
                    className="text-red-500 hover:text-red-700 transition-colors p-1 rounded hover:bg-red-50"
                    title="Remove Workspace"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </td>
              </tr>
            ))}
            {workspaces?.length === 0 && (
              <tr>
                <td colSpan={6} className="p-8 text-center text-gray-500">
                  No workspaces found. Click "Add New Workspace" to attach a domain to a codebase.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Create Project Modal */}
      {isCreatingProject && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-md flex flex-col">
            <div className="p-5 border-b border-gray-200">
              <h2 className="text-xl font-bold text-gray-800">Create New Workspace</h2>
            </div>
            
            <div className="p-5">
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Target Domain ID</label>
                <input 
                  type="text" 
                  value={newProjectName}
                  onChange={(e) => setNewProjectName(e.target.value)}
                  placeholder="e.g. University ERP"
                  className="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-slate-900"
                  autoFocus
                />
                <p className="text-xs text-gray-500 mt-2">
                  This must match the name of a registered domain package to map properly.
                </p>
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
                  If provided, this registers a local folder as a project.
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
                Create Workspace
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
