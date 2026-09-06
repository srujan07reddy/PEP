import React, { useState } from 'react';

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
    <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Intelligence Hub</h1>

      <div className="flex space-x-4 mb-8 border-b pb-2">
        <button 
          onClick={() => setActiveTab('repo')}
          className={`px-4 py-2 rounded ${activeTab === 'repo' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}>
          Code Graph
        </button>
        <button 
          onClick={() => setActiveTab('process')}
          className={`px-4 py-2 rounded ${activeTab === 'process' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}>
          Process Miner
        </button>
        <button 
          onClick={() => setActiveTab('document')}
          className={`px-4 py-2 rounded ${activeTab === 'document' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}>
          Document Parser
        </button>
      </div>

      {/* REPOSITORY SCANNER TAB */}
      {activeTab === 'repo' && (
        <div className="bg-white p-6 rounded shadow">
          <h2 className="text-xl font-bold mb-4">Tree-sitter Repository Scanner</h2>
          <p className="text-gray-600 mb-4">
            Scan the entire workspace using Tree-sitter to build a foundational code graph of classes, functions, and imports.
          </p>
          <button 
            onClick={handleScanRepo}
            disabled={scanning}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50">
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
        <div className="bg-white p-6 rounded shadow">
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
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50">
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
        <div className="bg-white p-6 rounded shadow">
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
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50">
            {uploading ? 'Parsing Document...' : 'Parse Document'}
          </button>

          {docResult && (
            <div className="mt-6 p-4 bg-gray-50 border rounded">
              <h3 className="font-bold mb-2">Extracted Payload:</h3>
              <pre className="text-xs overflow-auto bg-gray-800 text-blue-300 p-4 rounded max-h-96">
                {JSON.stringify(docResult, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}

    </div>
  );
};

export default IntelligenceHub;
