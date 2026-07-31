import { useState } from 'react';
import CompilerDashboard from '../components/CompilerDashboard';
import ValidationReport from '../components/ValidationReport';

export default function KnowledgeCompilerPage() {
  const [compilerStats, setCompilerStats] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);

  return (
    <div className="flex flex-col gap-8 h-full overflow-auto">
      <div>
        <h1 className="text-3xl font-bold mb-2">Organizational Knowledge Compiler</h1>
        <p className="text-gray-600">
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
