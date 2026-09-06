import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getMcpTools } from '../lib/api';
import { Terminal, Settings, Zap, Database, Key, Server } from 'lucide-react';

export default function Mcp() {
  const { data: tools, isLoading } = useQuery({ queryKey: ['mcp_tools'], queryFn: getMcpTools });
  const [activeTab, setActiveTab] = useState<'status' | 'settings'>('status');
  const [modelConfig, setModelConfig] = useState({
    defaultModel: 'gpt-4o',
    anthropicKey: '',
    openaiKey: '',
    customEngineUrl: ''
  });
  const [isSaving, setIsSaving] = useState(false);

  const handleSaveSettings = () => {
    setIsSaving(true);
    setTimeout(() => {
      setIsSaving(false);
      alert('MCP Settings saved successfully!');
    }, 1000);
  };

  if (isLoading) return <div className="text-gray-500">Loading MCP status...</div>;

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="mb-6 flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold mb-2 text-gray-800 flex items-center gap-2">
            <Terminal className="w-8 h-8 text-green-600" />
            MCP Dashboard
          </h1>
          <p className="text-gray-600 max-w-3xl">
            Model Context Protocol (MCP) server status and configuration for external IDE integrations.
          </p>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div className="flex border-b border-gray-200">
          <button
            onClick={() => setActiveTab('status')}
            className={`flex-1 py-4 text-sm font-medium text-center transition-colors flex items-center justify-center gap-2 ${
              activeTab === 'status'
                ? 'bg-blue-50 text-blue-700 border-b-2 border-blue-600'
                : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
            }`}
          >
            <Zap className="w-4 h-4" />
            Tools & Status
          </button>
          <button
            onClick={() => setActiveTab('settings')}
            className={`flex-1 py-4 text-sm font-medium text-center transition-colors flex items-center justify-center gap-2 ${
              activeTab === 'settings'
                ? 'bg-blue-50 text-blue-700 border-b-2 border-blue-600'
                : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
            }`}
          >
            <Settings className="w-4 h-4" />
            Server Settings
          </button>
        </div>

        <div className="p-6">
          {activeTab === 'status' ? (
            <div className="animate-fade-in-up space-y-8">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-slate-50 rounded-lg border border-gray-200 p-6">
                  <div className="flex items-center gap-2 mb-2">
                    <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                    <h3 className="font-semibold text-gray-800">Server Status</h3>
                  </div>
                  <p className="text-sm text-gray-600">Online and ready for IDE connections.</p>
                </div>
                <div className="bg-slate-50 rounded-lg border border-gray-200 p-6">
                  <div className="flex items-center gap-2 mb-2">
                    <Server className="w-5 h-5 text-gray-500" />
                    <h3 className="font-semibold text-gray-800">Transport</h3>
                  </div>
                  <p className="text-sm text-gray-600">stdio (Standard I/O)</p>
                </div>
                <div className="bg-slate-50 rounded-lg border border-gray-200 p-6">
                  <div className="flex items-center gap-2 mb-2">
                    <Database className="w-5 h-5 text-indigo-500" />
                    <h3 className="font-semibold text-gray-800">Active Capabilities</h3>
                  </div>
                  <p className="text-sm text-gray-600">{tools?.length || 0} Tools Registered</p>
                </div>
              </div>

              <div className="border border-gray-200 rounded-lg overflow-hidden">
                <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
                  <h2 className="font-semibold text-gray-800">Exposed MCP Tools</h2>
                </div>
                <div className="divide-y divide-gray-100">
                  {tools?.map((tool: any, index: number) => (
                    <div key={index} className="p-6 hover:bg-gray-50 transition-colors">
                      <div className="flex items-start justify-between">
                        <div>
                          <h3 className="text-lg font-mono font-bold text-indigo-600 mb-1">{tool.name}</h3>
                          <p className="text-gray-600 text-sm whitespace-pre-wrap">{tool.description}</p>
                        </div>
                        <span className="bg-green-100 text-green-800 text-xs font-semibold px-2 py-1 rounded">Active</span>
                      </div>
                    </div>
                  ))}
                  {(!tools || tools.length === 0) && (
                    <div className="p-8 text-center text-gray-500">
                      No MCP tools found in server.py
                    </div>
                  )}
                </div>
              </div>
            </div>
          ) : (
            <div className="animate-fade-in-up max-w-3xl space-y-6">
              <div>
                <h2 className="text-xl font-semibold text-gray-800 mb-4">Model & Engine Configuration</h2>
                <p className="text-sm text-gray-500 mb-6">Configure the underlying LLMs and inference engines used by the MCP tools when executing complex reasoning tasks.</p>
              </div>

              <div className="space-y-5 bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Default Model Engine</label>
                  <select
                    value={modelConfig.defaultModel}
                    onChange={(e) => setModelConfig({ ...modelConfig, defaultModel: e.target.value })}
                    className="w-full border-gray-300 border rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 p-2"
                  >
                    <option value="gpt-4o">OpenAI GPT-4o</option>
                    <option value="gpt-4-turbo">OpenAI GPT-4 Turbo</option>
                    <option value="claude-3-5-sonnet">Anthropic Claude 3.5 Sonnet</option>
                    <option value="claude-3-opus">Anthropic Claude 3 Opus</option>
                    <option value="gemini-1.5-pro">Google Gemini 1.5 Pro</option>
                    <option value="custom">Custom Local Engine</option>
                  </select>
                </div>

                {modelConfig.defaultModel === 'custom' && (
                  <div className="animate-fade-in-up space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Custom Engine API URL</label>
                      <div className="relative">
                        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                          <Server className="h-4 w-4 text-gray-400" />
                        </div>
                        <input
                          type="text"
                          placeholder="http://localhost:11434/v1"
                          value={modelConfig.customEngineUrl}
                          onChange={(e) => setModelConfig({ ...modelConfig, customEngineUrl: e.target.value })}
                          className="pl-10 w-full border-gray-300 border rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 p-2"
                        />
                      </div>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Attach Local Model (.gguf / .bin)</label>
                      <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-lg hover:bg-gray-50 transition-colors">
                        <div className="space-y-1 text-center">
                          <Database className="mx-auto h-8 w-8 text-gray-400" />
                          <div className="flex text-sm text-gray-600 justify-center">
                            <label htmlFor="local-model-upload" className="relative cursor-pointer bg-white rounded-md font-medium text-blue-600 hover:text-blue-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-blue-500">
                              <span>Attach model file</span>
                              <input id="local-model-upload" name="local-model-upload" type="file" className="sr-only" accept=".gguf,.bin" />
                            </label>
                            <p className="pl-1">or drag and drop</p>
                          </div>
                          <p className="text-xs text-gray-500">GGUF or BIN model files for local inference</p>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                <hr className="border-gray-100" />

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">OpenAI API Key (Optional)</label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <Key className="h-4 w-4 text-gray-400" />
                    </div>
                    <input
                      type="password"
                      placeholder="sk-..."
                      value={modelConfig.openaiKey}
                      onChange={(e) => setModelConfig({ ...modelConfig, openaiKey: e.target.value })}
                      className="pl-10 w-full border-gray-300 border rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 p-2"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Anthropic API Key (Optional)</label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <Key className="h-4 w-4 text-gray-400" />
                    </div>
                    <input
                      type="password"
                      placeholder="sk-ant-..."
                      value={modelConfig.anthropicKey}
                      onChange={(e) => setModelConfig({ ...modelConfig, anthropicKey: e.target.value })}
                      className="pl-10 w-full border-gray-300 border rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 p-2"
                    />
                  </div>
                </div>
              </div>

              <div className="flex justify-end pt-4">
                <button
                  onClick={handleSaveSettings}
                  disabled={isSaving}
                  className={`px-6 py-2 rounded-lg font-medium shadow-sm transition-colors flex items-center gap-2 ${
                    isSaving ? 'bg-blue-400 text-white cursor-not-allowed' : 'bg-blue-600 text-white hover:bg-blue-700'
                  }`}
                >
                  {isSaving ? 'Saving Configuration...' : 'Save Configuration'}
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
