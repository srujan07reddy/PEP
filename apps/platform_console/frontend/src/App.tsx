import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import pepLogo from './assets/pep-logo.svg';
import Dashboard from './pages/Dashboard';
import Domains from './pages/Domains';
import Workspaces from './pages/Workspaces';
import Agents from './pages/Agents';
import A2a from './pages/A2a';
import Mcp from './pages/Mcp';
import Findings from './pages/Findings';
import Reports from './pages/Reports';
import KnowledgeCompilerPage from './pages/KnowledgeCompilerPage';
import IntelligenceHub from './pages/IntelligenceHub';
import IdeaEnhancer from './pages/IdeaEnhancer';
import Standards from './pages/Standards';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="flex min-h-screen flex-col bg-transparent">
          <nav className="sticky top-0 z-10 flex w-full flex-wrap items-center gap-4 border-b border-slate-800/80 bg-[#17212b]/95 px-4 py-3 text-white shadow-xl shadow-slate-900/10 backdrop-blur-xl lg:px-6">
            <h1 className="mr-2 flex shrink-0 items-center gap-2 text-xl font-bold">
              <img src={pepLogo} alt="PEP" className="h-9 w-9 shrink-0" />
              PEP Console
            </h1>
            <ul className="flex min-w-0 flex-1 flex-wrap items-center gap-1">
              <li>
                <NavLink to="/" className={({ isActive }) => `block rounded-lg px-3 py-2 text-sm transition-all hover:-translate-y-0.5 hover:bg-slate-700 hover:text-white ${isActive ? 'bg-teal-500/90 font-bold text-white hover:bg-teal-400' : 'text-slate-300'}`}>Dashboard</NavLink>
              </li>
              <li>
                <NavLink to="/idea-enhancer" className={({ isActive }) => `flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition-all hover:-translate-y-0.5 hover:bg-slate-700 hover:text-white ${isActive ? 'bg-teal-500/90 font-bold text-white hover:bg-teal-400' : 'text-slate-300'}`}>
                  Idea Enhancer
                </NavLink>
              </li>
              <li>
                <NavLink to="/intelligence" className={({ isActive }) => `block rounded-lg px-3 py-2 text-sm transition-all hover:-translate-y-0.5 hover:bg-slate-700 hover:text-white ${isActive ? 'bg-teal-500/90 font-bold text-white hover:bg-teal-400' : 'text-slate-300'}`}>Intelligence Hub</NavLink>
              </li>
              <li>
                <NavLink to="/compiler" className={({ isActive }) => `block rounded-lg px-3 py-2 text-sm transition-all hover:-translate-y-0.5 hover:bg-slate-700 hover:text-white ${isActive ? 'bg-teal-500/90 font-bold text-white hover:bg-teal-400' : 'text-slate-300'}`}>Knowledge Compiler</NavLink>
              </li>
              <li>
                <NavLink to="/domains" className={({ isActive }) => `block rounded-lg px-3 py-2 text-sm transition-all hover:-translate-y-0.5 hover:bg-slate-700 hover:text-white ${isActive ? 'bg-teal-500/90 font-bold text-white hover:bg-teal-400' : 'text-slate-300'}`}>Domains</NavLink>
              </li>
              <li>
                <NavLink to="/workspaces" className={({ isActive }) => `block rounded-lg px-3 py-2 text-sm transition-all hover:-translate-y-0.5 hover:bg-slate-700 hover:text-white ${isActive ? 'bg-teal-500/90 font-bold text-white hover:bg-teal-400' : 'text-slate-300'}`}>Workspaces</NavLink>
              </li>
              <li>
                <NavLink to="/agents" className={({ isActive }) => `block rounded-lg px-3 py-2 text-sm transition-all hover:-translate-y-0.5 hover:bg-slate-700 hover:text-white ${isActive ? 'bg-teal-500/90 font-bold text-white hover:bg-teal-400' : 'text-slate-300'}`}>Agents</NavLink>
              </li>
              <li>
                <NavLink to="/a2a" className={({ isActive }) => `block rounded-lg px-3 py-2 text-sm transition-all hover:-translate-y-0.5 hover:bg-slate-700 hover:text-white ${isActive ? 'bg-teal-500/90 font-bold text-white hover:bg-teal-400' : 'text-slate-300'}`}>A2A Dashboard</NavLink>
              </li>
              <li>
                <NavLink to="/mcp" className={({ isActive }) => `block rounded-lg px-3 py-2 text-sm transition-all hover:-translate-y-0.5 hover:bg-slate-700 hover:text-white ${isActive ? 'bg-teal-500/90 font-bold text-white hover:bg-teal-400' : 'text-slate-300'}`}>MCP Server</NavLink>
              </li>
              <li>
                <NavLink to="/findings" className={({ isActive }) => `block rounded-lg px-3 py-2 text-sm transition-all hover:-translate-y-0.5 hover:bg-slate-700 hover:text-white ${isActive ? 'bg-teal-500/90 font-bold text-white hover:bg-teal-400' : 'text-slate-300'}`}>Findings</NavLink>
              </li>
              <li>
                <NavLink to="/reports" className={({ isActive }) => `block rounded-lg px-3 py-2 text-sm transition-all hover:-translate-y-0.5 hover:bg-slate-700 hover:text-white ${isActive ? 'bg-teal-500/90 font-bold text-white hover:bg-teal-400' : 'text-slate-300'}`}>Reports</NavLink>
              </li>
            </ul>
          </nav>
          <main className="flex-1 overflow-auto p-8 text-gray-900">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/intelligence" element={<IntelligenceHub />} />
              <Route path="/compiler" element={<KnowledgeCompilerPage />} />
              <Route path="/domains" element={<Domains />} />
              <Route path="/workspaces" element={<Workspaces />} />
              <Route path="/agents" element={<Agents />} />
              <Route path="/a2a" element={<A2a />} />
              <Route path="/mcp" element={<Mcp />} />
              <Route path="/findings" element={<Findings />} />
              <Route path="/reports" element={<Reports />} />
              <Route path="/standards" element={<Standards />} />
              <Route path="/idea-enhancer" element={<IdeaEnhancer />} />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
