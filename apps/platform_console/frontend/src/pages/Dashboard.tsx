import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { getDomains, getAgents, getMcpServers } from '../lib/api';

export default function Dashboard() {
  const { data: domains } = useQuery({ queryKey: ['domains'], queryFn: getDomains });
  const { data: agents } = useQuery({ queryKey: ['agents'], queryFn: getAgents });
  const { data: mcpServers } = useQuery({ queryKey: ['mcp-servers'], queryFn: getMcpServers });

  return (
    <div className="min-h-full -m-8 bg-gradient-to-br from-slate-50 via-teal-50/30 to-cyan-100/40 p-8">
      <h1 className="mb-8 text-3xl font-bold text-slate-800">Platform Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="group">
          <Link to="/domains" className="flex min-h-40 items-end rounded-2xl border border-white/80 bg-white/55 p-6 shadow-lg shadow-slate-300/30 backdrop-blur-xl transition-all hover:-translate-y-1 hover:bg-white/70 hover:shadow-xl hover:shadow-teal-200/40 cursor-pointer">
            <p className="text-5xl font-bold tracking-tight text-teal-700">{domains?.length || 0}</p>
          </Link>
          <h2 className="mt-3 px-1 text-sm font-semibold uppercase tracking-[0.18em] text-slate-600">Active Domains</h2>
        </div>
        <div className="group">
          <Link to="/agents" className="flex min-h-40 items-end rounded-2xl border border-white/80 bg-white/55 p-6 shadow-lg shadow-slate-300/30 backdrop-blur-xl transition-all hover:-translate-y-1 hover:bg-white/70 hover:shadow-xl hover:shadow-emerald-200/40 cursor-pointer">
            <p className="text-5xl font-bold tracking-tight text-emerald-700">{agents?.length || 0}</p>
          </Link>
          <h2 className="mt-3 px-1 text-sm font-semibold uppercase tracking-[0.18em] text-slate-600">Registered Agents</h2>
        </div>
        <div className="group">
          <Link to="/standards" className="flex min-h-40 items-end rounded-2xl border border-white/80 bg-white/55 p-6 shadow-lg shadow-slate-300/30 backdrop-blur-xl transition-all hover:-translate-y-1 hover:bg-white/70 hover:shadow-xl hover:shadow-cyan-200/40 cursor-pointer">
            <p className="text-5xl font-bold tracking-tight text-cyan-700">12</p>
          </Link>
          <h2 className="mt-3 px-1 text-sm font-semibold uppercase tracking-[0.18em] text-slate-600">Platform Standards</h2>
        </div>
        <div className="group">
          <Link to="/mcp" className="flex min-h-40 items-end rounded-2xl border border-white/80 bg-white/55 p-6 shadow-lg shadow-slate-300/30 backdrop-blur-xl transition-all hover:-translate-y-1 hover:bg-white/70 hover:shadow-xl hover:shadow-cyan-200/40 cursor-pointer">
            <p className="text-5xl font-bold tracking-tight text-cyan-700">{mcpServers?.length || 0}</p>
          </Link>
          <h2 className="mt-3 px-1 text-sm font-semibold uppercase tracking-[0.18em] text-slate-600">MCP Servers</h2>
        </div>
      </div>
    </div>
  );
}
