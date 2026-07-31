import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { getDomains, getAgents, getStandards } from '../lib/api';

export default function Dashboard() {
  const { data: domains } = useQuery({ queryKey: ['domains'], queryFn: getDomains });
  const { data: agents } = useQuery({ queryKey: ['agents'], queryFn: getAgents });
  const { data: standards } = useQuery({ queryKey: ['standards'], queryFn: getStandards });

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8 text-gray-800">Platform Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Link to="/domains" className="bg-white p-6 rounded-lg shadow-sm border border-gray-100 hover:shadow-md transition-shadow cursor-pointer block">
          <h2 className="text-lg font-medium text-gray-500 mb-2">Active Domains</h2>
          <p className="text-4xl font-bold text-blue-600">{domains?.length || 0}</p>
        </Link>
        <Link to="/agents" className="bg-white p-6 rounded-lg shadow-sm border border-gray-100 hover:shadow-md transition-shadow cursor-pointer block">
          <h2 className="text-lg font-medium text-gray-500 mb-2">Registered Agents</h2>
          <p className="text-4xl font-bold text-green-600">{agents?.length || 0}</p>
        </Link>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100 opacity-50 cursor-not-allowed">
          <h2 className="text-lg font-medium text-gray-500 mb-2">Platform Standards</h2>
          <p className="text-4xl font-bold text-purple-600">{standards?.length || 0}</p>
        </div>
      </div>
    </div>
  );
}
