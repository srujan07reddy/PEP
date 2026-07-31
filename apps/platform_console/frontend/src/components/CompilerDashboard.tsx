import { useState } from 'react';
import { Database, FolderTree, Network, RefreshCw, CheckCircle, AlertTriangle } from 'lucide-react';

export default function CompilerDashboard({ stats, setStats, selectedFile, setSelectedFile }: any) {
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const compileBlueprint = async () => {
    if (!selectedFile) {
      alert("Please select a JSON or YAML blueprint file first.");
      return;
    }
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch('http://localhost:8000/organization/compile', {
        method: 'POST',
        body: formData // No Content-Type header needed; fetch sets multipart/form-data boundary automatically
      });
      const data = await response.json();
      setStats(data);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex justify-between items-start mb-6">
        <div>
          <h2 className="text-xl font-bold flex items-center gap-2">
            <Database className="text-blue-600" /> Organizational Knowledge Compiler (OKC)
          </h2>
          <p className="text-sm text-gray-500 mt-1">
            The OKC acts as a foundational pre-processor. It ingests raw organizational blueprints (YAML/JSON) 
            and compiles them into a traversable Graph Database.
          </p>
        </div>
        <div className="flex flex-col items-end gap-2">
          <input 
            type="file" 
            accept=".json,.yaml,.yml"
            onChange={handleFileChange}
            className="text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
          <button 
            onClick={compileBlueprint}
            disabled={loading || !selectedFile}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded shadow flex items-center gap-2 disabled:opacity-50"
          >
            {loading ? <RefreshCw className="animate-spin w-4 h-4" /> : <Network className="w-4 h-4" />}
            Compile Organization Blueprint
          </button>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-6 mt-6">
        <div className="border border-gray-200 p-4 rounded bg-gray-50 flex items-center gap-4">
          <div className="p-3 bg-blue-100 text-blue-600 rounded-full"><FolderTree /></div>
          <div>
            <div className="text-sm text-gray-500">Nodes Extracted</div>
            <div className="text-2xl font-bold">{stats ? stats.nodes : '--'}</div>
          </div>
        </div>
        
        <div className="border border-gray-200 p-4 rounded bg-gray-50 flex items-center gap-4">
          <div className="p-3 bg-indigo-100 text-indigo-600 rounded-full"><Network /></div>
          <div>
            <div className="text-sm text-gray-500">Relationships (Edges)</div>
            <div className="text-2xl font-bold">{stats ? stats.edges : '--'}</div>
          </div>
        </div>

        <div className="border border-gray-200 p-4 rounded flex items-center gap-4">
          <div className={`p-3 rounded-full ${stats ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-400'}`}>
            {stats ? <CheckCircle /> : <AlertTriangle />}
          </div>
          <div>
            <div className="text-sm text-gray-500">Compiler Status</div>
            <div className="font-semibold text-sm">{stats ? stats.message : 'Awaiting compilation'}</div>
          </div>
        </div>
      </div>
      
      {stats && (
        <div className="mt-8 p-4 bg-blue-50 border border-blue-200 rounded text-sm text-blue-800">
          <strong>Success!</strong> The blueprint was parsed recursively. Departments, Roles, Workflows, and Policies were typed and versioned. The Relationship Extractor dynamically built edges for <code>reports_to</code> and <code>depends_on</code> foreign keys. The graph is ready for routing!
        </div>
      )}
    </div>
  );
}
