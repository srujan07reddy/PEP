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
        <div className="flex min-h-screen flex-col bg-gray-100">
          <nav className="sticky top-0 z-10 flex w-full flex-wrap items-center gap-4 border-b border-slate-700 bg-slate-900 px-4 py-3 text-white shadow-lg lg:px-6">
            <h1 className="mr-2 flex shrink-0 items-center gap-2 text-xl font-bold">
              <span className="text-blue-400">⚡</span> PEP Console
            </h1>
            <ul className="flex min-w-0 flex-1 flex-wrap items-center gap-1">
              <li>
                <NavLink to="/" className={({ isActive }) => `block rounded-lg px-3 py-2 text-sm transition-all hover:-translate-y-0.5 hover:bg-slate-700 hover:text-white ${isActive ? 'bg-blue-600 font-bold hover:bg-blue-500' : 'text-slate-300'}`}>Dashboard</NavLink>
              </li>
              <li>
                <NavLink to="/idea-enhancer" className={({ isActive }) => `flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition-all hover:-translate-y-0.5 hover:bg-slate-700 hover:text-white ${isActive ? 'bg-blue-600 font-bold hover:bg-blue-500' : 'text-slate-300'}`}>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path></svg>
                  Idea Enhancer
                </NavLink>
              </li>
              <li>
                <NavLink to="/intelligence" className={({ isActive }) => `block rounded-lg px-3 py-2 text-sm transition-all hover:-translate-y-0.5 hover:bg-slate-700 hover:text-white ${isActive ? 'bg-blue-600 font-bold hover:bg-blue-500' : 'text-slate-300'}`}>Intelligence Hub</NavLink>
              </li>
              <li>
                <NavLink to="/compiler" className={({ isActive }) => `block rounded-lg px-3 py-2 text-sm transition-all hover:-translate-y-0.5 hover:bg-slate-700 hover:text-white ${isActive ? 'bg-blue-600 font-bold hover:bg-blue-500' : 'text-slate-300'}`}>Knowledge Compiler</NavLink>
              </li>
              <li>
                <NavLink to="/erp" className={({ isActive }) => `block rounded-lg px-3 py-2 text-sm transition-all hover:-translate-y-0.5 hover:bg-slate-700 hover:text-white ${isActive ? 'bg-blue-600 font-bold hover:bg-blue-500' : 'text-slate-300'}`}>Executive Console</NavLink>
              </li>
              <li>
                <NavLink to="/domains" className={({ isActive }) => `block rounded-lg px-3 py-2 text-sm transition-all hover:-translate-y-0.5 hover:bg-slate-700 hover:text-white ${isActive ? 'bg-blue-600 font-bold hover:bg-blue-500' : 'text-slate-300'}`}>Domains</NavLink>
              </li>
              <li>
                <NavLink to="/workspaces" className={({ isActive }) => `block rounded-lg px-3 py-2 text-sm transition-all hover:-translate-y-0.5 hover:bg-slate-700 hover:text-white ${isActive ? 'bg-blue-600 font-bold hover:bg-blue-500' : 'text-slate-300'}`}>Workspaces</NavLink>
              </li>
              <li>
                <NavLink to="/agents" className={({ isActive }) => `block rounded-lg px-3 py-2 text-sm transition-all hover:-translate-y-0.5 hover:bg-slate-700 hover:text-white ${isActive ? 'bg-blue-600 font-bold hover:bg-blue-500' : 'text-slate-300'}`}>Agents</NavLink>
              </li>
              <li>
                <NavLink to="/a2a" className={({ isActive }) => `block rounded-lg px-3 py-2 text-sm transition-all hover:-translate-y-0.5 hover:bg-slate-700 hover:text-white ${isActive ? 'bg-blue-600 font-bold hover:bg-blue-500' : 'text-slate-300'}`}>A2A Dashboard</NavLink>
              </li>
              <li>
                <NavLink to="/mcp" className={({ isActive }) => `block rounded-lg px-3 py-2 text-sm transition-all hover:-translate-y-0.5 hover:bg-slate-700 hover:text-white ${isActive ? 'bg-blue-600 font-bold hover:bg-blue-500' : 'text-slate-300'}`}>MCP Server</NavLink>
              </li>
              <li>
                <NavLink to="/findings" className={({ isActive }) => `block rounded-lg px-3 py-2 text-sm transition-all hover:-translate-y-0.5 hover:bg-slate-700 hover:text-white ${isActive ? 'bg-blue-600 font-bold hover:bg-blue-500' : 'text-slate-300'}`}>Findings</NavLink>
              </li>
              <li>
                <NavLink to="/reports" className={({ isActive }) => `block rounded-lg px-3 py-2 text-sm transition-all hover:-translate-y-0.5 hover:bg-slate-700 hover:text-white ${isActive ? 'bg-blue-600 font-bold hover:bg-blue-500' : 'text-slate-300'}`}>Reports</NavLink>
              </li>
            </ul>
          </nav>
          <main className="flex-1 overflow-auto p-8 text-gray-900">
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
