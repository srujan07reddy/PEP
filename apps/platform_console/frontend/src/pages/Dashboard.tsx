import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { getDomains, getAgents, getStandards } from '../lib/api';

export default function Dashboard() {
  const { data: domains } = useQuery({ queryKey: ['domains'], queryFn: getDomains });
  const { data: agents } = useQuery({ queryKey: ['agents'], queryFn: getAgents });
  const { data: standards } = useQuery({ queryKey: ['standards'], queryFn: getStandards });

  return (
    <div className="min-h-full bg-gradient-to-br from-slate-50 via-blue-50/50 to-indigo-100/60 -m-8 p-8">
      <h1 className="text-3xl font-bold mb-8 text-slate-800">Platform Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="group">
          <Link to="/domains" className="flex min-h-40 items-end rounded-2xl border border-white/80 bg-white/55 p-6 shadow-lg shadow-slate-300/30 backdrop-blur-xl transition-all hover:-translate-y-1 hover:bg-white/70 hover:shadow-xl hover:shadow-blue-200/40 cursor-pointer">
            <p className="text-5xl font-bold tracking-tight text-blue-600">{domains?.length || 0}</p>
          </Link>
          <h2 className="mt-3 px-1 text-sm font-semibold uppercase tracking-[0.18em] text-slate-600">Active Domains</h2>
        </div>
        <div className="group">
          <Link to="/agents" className="flex min-h-40 items-end rounded-2xl border border-white/80 bg-white/55 p-6 shadow-lg shadow-slate-300/30 backdrop-blur-xl transition-all hover:-translate-y-1 hover:bg-white/70 hover:shadow-xl hover:shadow-emerald-200/40 cursor-pointer">
            <p className="text-5xl font-bold tracking-tight text-emerald-600">{agents?.length || 0}</p>
          </Link>
          <h2 className="mt-3 px-1 text-sm font-semibold uppercase tracking-[0.18em] text-slate-600">Registered Agents</h2>
        </div>
        <div className="group">
          <div className="flex min-h-40 items-end rounded-2xl border border-white/70 bg-white/40 p-6 opacity-80 shadow-lg shadow-slate-300/25 backdrop-blur-xl cursor-not-allowed">
            <p className="text-5xl font-bold tracking-tight text-indigo-600">{standards?.length || 0}</p>
          </div>
          <h2 className="mt-3 px-1 text-sm font-semibold uppercase tracking-[0.18em] text-slate-500">Platform Standards</h2>
        </div>
      </div>
    </div>
  );
}
