import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Dashboard from './pages/Dashboard';
import Domains from './pages/Domains';
import Workspaces from './pages/Workspaces';
import Agents from './pages/Agents';
import A2a from './pages/A2a';
import Mcp from './pages/Mcp';
import Findings from './pages/Findings';
import Reports from './pages/Reports';
import ExecutiveEngineeringConsole from './pages/ExecutiveEngineeringConsole';
import KnowledgeCompilerPage from './pages/KnowledgeCompilerPage';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="flex h-screen bg-gray-100">
          <nav className="w-64 bg-slate-900 text-white p-4 shadow-lg z-10 flex flex-col">
            <h1 className="text-xl font-bold mb-8 flex items-center gap-2">
              <span className="text-blue-400">⚡</span> PEP Console
            </h1>
            <ul className="space-y-2 flex-1">
              <li>
                <NavLink to="/" className={({ isActive }) => `block px-4 py-2 rounded transition-colors ${isActive ? 'bg-blue-600 hover:bg-blue-500 font-bold' : 'hover:bg-slate-800'}`}>Dashboard</NavLink>
              </li>
              <li>
                <NavLink to="/compiler" className={({ isActive }) => `block px-4 py-2 rounded transition-colors ${isActive ? 'bg-blue-600 hover:bg-blue-500 font-bold' : 'hover:bg-slate-800'}`}>Knowledge Compiler</NavLink>
              </li>
              <li>
                <NavLink to="/erp" className={({ isActive }) => `block px-4 py-2 rounded transition-colors ${isActive ? 'bg-blue-600 hover:bg-blue-500 font-bold' : 'hover:bg-slate-800'}`}>Executive Console</NavLink>
              </li>
              <li>
                <NavLink to="/domains" className={({ isActive }) => `block px-4 py-2 rounded transition-colors ${isActive ? 'bg-blue-600 hover:bg-blue-500 font-bold' : 'hover:bg-slate-800'}`}>Domains</NavLink>
              </li>
              <li>
                <NavLink to="/workspaces" className={({ isActive }) => `block px-4 py-2 rounded transition-colors ${isActive ? 'bg-blue-600 hover:bg-blue-500 font-bold' : 'hover:bg-slate-800'}`}>Workspaces</NavLink>
              </li>
              <li>
                <NavLink to="/agents" className={({ isActive }) => `block px-4 py-2 rounded transition-colors ${isActive ? 'bg-blue-600 hover:bg-blue-500 font-bold' : 'hover:bg-slate-800'}`}>Agents</NavLink>
              </li>
              <li>
                <NavLink to="/a2a" className={({ isActive }) => `block px-4 py-2 rounded transition-colors ${isActive ? 'bg-blue-600 hover:bg-blue-500 font-bold' : 'hover:bg-slate-800'}`}>A2A Dashboard</NavLink>
              </li>
              <li>
                <NavLink to="/mcp" className={({ isActive }) => `block px-4 py-2 rounded transition-colors ${isActive ? 'bg-blue-600 hover:bg-blue-500 font-bold' : 'hover:bg-slate-800'}`}>MCP Server</NavLink>
              </li>
              <li>
                <NavLink to="/findings" className={({ isActive }) => `block px-4 py-2 rounded transition-colors ${isActive ? 'bg-blue-600 hover:bg-blue-500 font-bold' : 'hover:bg-slate-800'}`}>Findings</NavLink>
              </li>
              <li>
                <NavLink to="/reports" className={({ isActive }) => `block px-4 py-2 rounded transition-colors ${isActive ? 'bg-blue-600 hover:bg-blue-500 font-bold' : 'hover:bg-slate-800'}`}>Reports</NavLink>
              </li>
            </ul>
          </nav>
          <main className="flex-1 p-8 overflow-auto text-gray-900">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/compiler" element={<KnowledgeCompilerPage />} />
              <Route path="/erp" element={<ExecutiveEngineeringConsole />} />
              <Route path="/domains" element={<Domains />} />
              <Route path="/workspaces" element={<Workspaces />} />
              <Route path="/agents" element={<Agents />} />
              <Route path="/a2a" element={<A2a />} />
              <Route path="/mcp" element={<Mcp />} />
              <Route path="/findings" element={<Findings />} />
              <Route path="/reports" element={<Reports />} />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
