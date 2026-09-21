import { useState } from 'react';
import CompilerDashboard from '../components/CompilerDashboard';
import ValidationReport from '../components/ValidationReport';

export default function KnowledgeCompilerPage() {
  const [compilerStats, setCompilerStats] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);

  return (
    <div className="mx-auto flex h-full w-full max-w-6xl flex-col gap-8 overflow-auto pb-8">
      <div className="max-w-3xl">
        <p className="mb-3 text-xs font-semibold uppercase tracking-[0.2em] text-blue-600">Knowledge systems / compiler</p>
        <h1 className="text-4xl font-bold tracking-tight text-slate-900">Organizational Knowledge Compiler</h1>
        <p className="mt-3 text-base leading-7 text-slate-500">
          Upload and compile your organizational blueprint into a traversable Knowledge Graph.
          Once compiled, validate the graph to ensure no circular dependencies or orphaned roles exist.
        </p>
      </div>
      
      <CompilerDashboard 
        stats={compilerStats} 
        setStats={setCompilerStats} 
        selectedFile={selectedFile} 
        setSelectedFile={setSelectedFile} 
      />
      <ValidationReport orgName={compilerStats ? "uploaded_org" : "mock_org"} />
    </div>
  );
}
