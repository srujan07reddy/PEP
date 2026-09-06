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
import IntelligenceHub from './pages/IntelligenceHub';
import IdeaEnhancer from './pages/IdeaEnhancer';

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
                <NavLink to="/idea-enhancer" className={({ isActive }) => `block px-4 py-2 rounded transition-colors flex items-center gap-2 ${isActive ? 'bg-blue-600 hover:bg-blue-500 font-bold' : 'hover:bg-slate-800'}`}>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path></svg>
                  Idea Enhancer
                </NavLink>
              </li>
              <li>
                <NavLink to="/intelligence" className={({ isActive }) => `block px-4 py-2 rounded transition-colors ${isActive ? 'bg-blue-600 hover:bg-blue-500 font-bold' : 'hover:bg-slate-800'}`}>Intelligence Hub</NavLink>
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
              <Route path="/intelligence" element={<IntelligenceHub />} />
              <Route path="/compiler" element={<KnowledgeCompilerPage />} />
              <Route path="/erp" element={<ExecutiveEngineeringConsole />} />
              <Route path="/domains" element={<Domains />} />
              <Route path="/workspaces" element={<Workspaces />} />
              <Route path="/agents" element={<Agents />} />
              <Route path="/a2a" element={<A2a />} />
              <Route path="/mcp" element={<Mcp />} />
              <Route path="/findings" element={<Findings />} />
              <Route path="/reports" element={<Reports />} />
              <Route path="/idea-enhancer" element={<IdeaEnhancer />} />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
