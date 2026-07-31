import { useQuery } from '@tanstack/react-query';
import { getMcpTools } from '../lib/api';
import { Terminal, Settings, Zap } from 'lucide-react';

export default function Mcp() {
  const { data: tools, isLoading } = useQuery({ queryKey: ['mcp_tools'], queryFn: getMcpTools });

  if (isLoading) return <div className="text-gray-500">Loading MCP status...</div>;

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-3xl font-bold mb-2 text-gray-800 flex items-center gap-2">
          <Terminal className="w-8 h-8 text-green-600" />
          MCP Dashboard
        </h1>
        <p className="text-gray-600 max-w-3xl">
          Model Context Protocol (MCP) server status and registered capabilities for external IDE integrations.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
            <h3 className="font-semibold text-gray-800">Server Status</h3>
          </div>
          <p className="text-sm text-gray-600">Online and ready for IDE connections.</p>
        </div>
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center gap-2 mb-2">
            <Settings className="w-5 h-5 text-gray-500" />
            <h3 className="font-semibold text-gray-800">Transport</h3>
          </div>
          <p className="text-sm text-gray-600">stdio (Standard I/O)</p>
        </div>
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center gap-2 mb-2">
            <Zap className="w-5 h-5 text-yellow-500" />
            <h3 className="font-semibold text-gray-800">Active Capabilities</h3>
          </div>
          <p className="text-sm text-gray-600">{tools?.length || 0} Tools Registered</p>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <div className="bg-slate-50 px-6 py-4 border-b border-gray-200">
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
  );
}
