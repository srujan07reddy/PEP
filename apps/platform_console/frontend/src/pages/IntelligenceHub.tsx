import React, { useState } from 'react';
import { ArrowRight, FileText, Network, Workflow } from 'lucide-react';

const IntelligenceHub: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'repo' | 'process' | 'document'>('repo');

  // Repo Scanner State
  const [repoResult, setRepoResult] = useState<any>(null);
  const [scanning, setScanning] = useState(false);

  // Process State
  const [camundaUrl, setCamundaUrl] = useState('');
  const [processId, setProcessId] = useState('');
  const [logPath, setLogPath] = useState('');
  const [processResult, setProcessResult] = useState<any>(null);
  const [processing, setProcessing] = useState(false);

  // Document State
  const [file, setFile] = useState<File | null>(null);
  const [docResult, setDocResult] = useState<any>(null);
  const [uploading, setUploading] = useState(false);

  const sections = [
    {
      id: 'repo' as const,
      title: 'Code Graph',
      description: 'Map classes, functions, imports, and calls across your workspace.',
      icon: Network,
      accent: 'cyan',
    },
    {
      id: 'process' as const,
      title: 'Process Miner',
      description: 'Compare expected workflows with the reality in your event logs.',
      icon: Workflow,
      accent: 'emerald',
    },
    {
      id: 'document' as const,
      title: 'Document Parser',
      description: 'Extract structured intelligence from PDFs, images, and office files.',
      icon: FileText,
      accent: 'violet',
    },
  ];

  const activeSection = sections.find((section) => section.id === activeTab)!;

  const handleScanRepo = async () => {
    setScanning(true);
    try {
      const res = await fetch('http://localhost:8000/api/intelligence/scan-repo', {
        method: 'POST'
      });
      const data = await res.json();
      setRepoResult(data);
    } catch (e) {
      console.error(e);
    }
    setScanning(false);
  };

  const handleProcess = async () => {
    setProcessing(true);
    try {
      const res = await fetch('http://localhost:8000/api/intelligence/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          camunda_url: camundaUrl,
          process_id: processId,
          event_log_path: logPath
        })
      });
      const data = await res.json();
      setProcessResult(data);
    } catch (e) {
      console.error(e);
    }
    setProcessing(false);
  };

  const handleDocUpload = async () => {
    if (!file) return;
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('http://localhost:8000/api/intelligence/document', {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      setDocResult(data);
    } catch (e) {
      console.error(e);
    }
    setUploading(false);
  };

  return (
    <div className="mx-auto max-w-6xl space-y-8">
      <div>
        <p className="mb-2 text-xs font-semibold uppercase tracking-[0.2em] text-cyan-600">Operational intelligence</p>
        <h1 className="text-4xl font-bold tracking-tight text-slate-900">Intelligence Hub</h1>
        <p className="mt-2 max-w-2xl text-slate-500">Choose a lens to turn code, process, and document signals into useful decisions.</p>
      </div>

      <div className="grid gap-6 lg:grid-cols-[280px_minmax(0,1fr)] lg:items-start">
        <aside className="space-y-3">
          <div className="mb-4 px-1">
            <p className="text-sm font-semibold text-slate-800">Select an intelligence tool</p>
            <p className="mt-1 text-xs leading-relaxed text-slate-500">The active workspace opens beside the selected tile.</p>
          </div>
          {sections.map((section) => {
            const Icon = section.icon;
            const isActive = activeTab === section.id;

            return (
              <button
                key={section.id}
                onClick={() => setActiveTab(section.id)}
                className={`group relative w-full overflow-hidden rounded-2xl border p-4 text-left transition-all duration-300 ${
                  isActive
                    ? 'border-cyan-200 bg-white shadow-lg shadow-cyan-100/70 lg:translate-x-2'
                    : 'border-white/80 bg-white/55 shadow-sm hover:-translate-y-0.5 hover:border-slate-200 hover:bg-white hover:shadow-md'
                }`}
              >
                <div className="flex items-start gap-3">
                  <span className={`rounded-xl p-2.5 ${
                    section.accent === 'cyan' ? 'bg-cyan-100 text-cyan-700' :
                    section.accent === 'emerald' ? 'bg-emerald-100 text-emerald-700' :
                    'bg-violet-100 text-violet-700'
                  }`}>
                    <Icon className="h-5 w-5" />
                  </span>
                  <span className="min-w-0 flex-1">
                    <span className="block text-sm font-semibold text-slate-800">{section.title}</span>
                    <span className="mt-1 block text-xs leading-relaxed text-slate-500">{section.description}</span>
                  </span>
                  <ArrowRight className={`mt-1 h-4 w-4 shrink-0 transition-transform ${isActive ? 'translate-x-0 text-cyan-600' : '-translate-x-1 text-slate-300 group-hover:translate-x-0 group-hover:text-slate-500'}`} />
                </div>
              </button>
            );
          })}
        </aside>

        <section key={activeTab} className="min-w-0 animate-[slide-in_350ms_ease-out] rounded-3xl border border-white/80 bg-white/75 p-5 shadow-xl shadow-slate-200/60 backdrop-blur-xl sm:p-8">
          <div className="mb-6 flex items-center gap-3 border-b border-slate-100 pb-5">
            <span className="rounded-xl bg-slate-100 p-2 text-slate-600"><activeSection.icon className="h-5 w-5" /></span>
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.16em] text-cyan-600">Active tool</p>
              <h2 className="mt-1 text-xl font-bold text-slate-900">{activeSection.title}</h2>
            </div>
          </div>

          {/* REPOSITORY SCANNER TAB */}
          {activeTab === 'repo' && (
        <div>
          <h2 className="text-xl font-bold mb-4">Tree-sitter Repository Scanner</h2>
          <p className="text-gray-600 mb-4">
            Scan the entire workspace using Tree-sitter to build a foundational code graph of classes, functions, and imports.
          </p>
          <button 
            onClick={handleScanRepo}
            disabled={scanning}
            className="rounded-lg bg-teal-600 px-4 py-2 text-white shadow-sm transition-colors hover:bg-teal-700 disabled:opacity-50">
            {scanning ? 'Scanning Workspace...' : 'Run Full Scan'}
          </button>
          
          {repoResult && (
            <div className="mt-6 p-4 bg-gray-50 border rounded">
              <h3 className="font-bold mb-2">Scan Results:</h3>
              {repoResult.status === 'success' ? (
                <ul className="list-disc pl-5">
                  <li><strong>Classes Found:</strong> {repoResult.data.classes?.length || 0}</li>
                  <li><strong>Functions Found:</strong> {repoResult.data.functions?.length || 0}</li>
                  <li><strong>Imports Detected:</strong> {repoResult.data.imports?.length || 0}</li>
                  <li><strong>Function Calls:</strong> {repoResult.data.calls?.length || 0}</li>
                </ul>
              ) : (
                <p className="text-red-500">Error: {repoResult.message}</p>
              )}
            </div>
          )}
        </div>
          )}

      {/* PROCESS MINER TAB */}
          {activeTab === 'process' && (
        <div>
          <h2 className="text-xl font-bold mb-4">Process Intelligence (Camunda vs PM4Py)</h2>
          <p className="text-gray-600 mb-4">
            Compare expected BPMN models from Camunda against actual event logs mined via PM4Py.
          </p>
          <div className="space-y-4 max-w-md">
            <div>
              <label className="block text-sm font-medium mb-1">Camunda REST API URL</label>
              <input type="text" className="w-full border p-2 rounded" placeholder="http://localhost:8080" value={camundaUrl} onChange={e => setCamundaUrl(e.target.value)} />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Process ID</label>
              <input type="text" className="w-full border p-2 rounded" placeholder="Order_Process_v1" value={processId} onChange={e => setProcessId(e.target.value)} />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Event Log Path (.csv or .xes)</label>
              <input type="text" className="w-full border p-2 rounded" placeholder="/path/to/logs.csv" value={logPath} onChange={e => setLogPath(e.target.value)} />
            </div>
            <button 
              onClick={handleProcess}
              disabled={processing}
              className="rounded-lg bg-teal-600 px-4 py-2 text-white shadow-sm transition-colors hover:bg-teal-700 disabled:opacity-50">
              {processing ? 'Analyzing...' : 'Run Conformance Check'}
            </button>
          </div>

          {processResult && (
            <div className="mt-6 p-4 bg-gray-50 border rounded">
              <h3 className="font-bold mb-2">Difference Engine Output:</h3>
              <pre className="text-xs overflow-auto bg-gray-800 text-green-400 p-4 rounded">
                {JSON.stringify(processResult, null, 2)}
              </pre>
            </div>
          )}
        </div>
          )}

      {/* DOCUMENT PARSER TAB */}
          {activeTab === 'document' && (
        <div>
          <h2 className="text-xl font-bold mb-4">Unstructured Document Parser</h2>
          <p className="text-gray-600 mb-4">
            Upload PDFs, Images, or Office Docs to extract structured text via Docling, Unstructured, or Tika.
          </p>
          <div className="mb-4">
            <input 
              type="file" 
              className="border p-2 rounded w-full max-w-md"
              onChange={e => setFile(e.target.files?.[0] || null)}
            />
          </div>
          <button 
            onClick={handleDocUpload}
            disabled={uploading || !file}
            className="rounded-lg bg-teal-600 px-4 py-2 text-white shadow-sm transition-colors hover:bg-teal-700 disabled:opacity-50">
            {uploading ? 'Parsing Document...' : 'Parse Document'}
          </button>

          {docResult && (
            <div className="mt-6 p-4 bg-gray-50 border rounded">
              <h3 className="font-bold mb-2">Extracted Payload:</h3>
              <pre className="max-h-96 overflow-auto rounded bg-slate-900 p-4 text-xs text-cyan-300">
                {JSON.stringify(docResult, null, 2)}
              </pre>
            </div>
          )}
        </div>
          )}
        </section>
      </div>
    </div>
  );
};

export default IntelligenceHub;
