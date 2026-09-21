import { useState } from 'react';
import { AlertTriangle, CheckCircle, Database, FileJson, FolderTree, Network, RefreshCw, Upload } from 'lucide-react';

export default function CompilerDashboard({ stats, setStats, selectedFile, setSelectedFile }: any) {
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) setSelectedFile(e.target.files[0]);
  };

  const compileBlueprint = async () => {
    if (!selectedFile) {
      alert('Please select a JSON or YAML blueprint file first.');
      return;
    }
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      const response = await fetch('http://localhost:8000/organization/compile', { method: 'POST', body: formData });
      setStats(await response.json());
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-lg shadow-slate-200/60">
      <div className="border-b border-slate-100 p-6 sm:p-8">
        <div className="flex flex-col justify-between gap-6 lg:flex-row lg:items-start">
          <div className="max-w-2xl">
            <div className="mb-4 flex items-center gap-3">
              <span className="rounded-xl bg-blue-50 p-3 text-blue-600"><Database className="h-6 w-6" /></span>
              <div><p className="text-xs font-semibold uppercase tracking-[0.16em] text-blue-600">Compiler workspace</p><h2 className="mt-1 text-xl font-bold text-slate-900">Organizational Knowledge Compiler <span className="text-slate-400">(OKC)</span></h2></div>
            </div>
            <p className="text-sm leading-6 text-slate-500">The OKC acts as a foundational pre-processor. It ingests raw organizational blueprints (YAML/JSON) and compiles them into a traversable Graph Database.</p>
          </div>
          <div className="flex w-full flex-col gap-3 lg:w-auto lg:min-w-[320px]">
            <div className="flex items-center gap-3 rounded-xl border border-dashed border-slate-300 bg-slate-50 p-2">
              <label className="flex shrink-0 cursor-pointer items-center gap-2 rounded-lg bg-white px-3 py-2 text-sm font-semibold text-slate-700 shadow-sm ring-1 ring-slate-200 transition hover:bg-blue-50 hover:text-blue-700"><Upload className="h-4 w-4" />Choose File<input type="file" accept=".json,.yaml,.yml" onChange={handleFileChange} className="sr-only" /></label>
              <span className="min-w-0 truncate text-sm text-slate-500" title={selectedFile?.name || 'No file chosen'}>{selectedFile?.name || 'No file chosen'}</span>
            </div>
            <button onClick={compileBlueprint} disabled={loading || !selectedFile} className="flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-3 text-sm font-semibold text-white shadow-md shadow-blue-600/20 transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50">
              {loading ? <RefreshCw className="h-4 w-4 animate-spin" /> : <Network className="h-4 w-4" />}Compile Organization Blueprint
            </button>
          </div>
        </div>
      </div>
      <div className="grid gap-px bg-slate-200 sm:grid-cols-3">
        <div className="flex items-center gap-4 bg-white p-5 sm:p-6"><div className="rounded-xl bg-blue-50 p-3 text-blue-600"><FolderTree className="h-5 w-5" /></div><div><div className="text-xs font-semibold uppercase tracking-wide text-slate-400">Nodes Extracted</div><div className="mt-1 text-2xl font-bold text-slate-900">{stats ? stats.nodes : '--'}</div></div></div>
        <div className="flex items-center gap-4 bg-white p-5 sm:p-6"><div className="rounded-xl bg-indigo-50 p-3 text-indigo-600"><Network className="h-5 w-5" /></div><div><div className="text-xs font-semibold uppercase tracking-wide text-slate-400">Relationships / Edges</div><div className="mt-1 text-2xl font-bold text-slate-900">{stats ? stats.edges : '--'}</div></div></div>
        <div className="flex items-center gap-4 bg-white p-5 sm:p-6"><div className={`rounded-xl p-3 ${stats ? 'bg-emerald-50 text-emerald-600' : 'bg-amber-50 text-amber-600'}`}>{stats ? <CheckCircle className="h-5 w-5" /> : <AlertTriangle className="h-5 w-5" />}</div><div><div className="text-xs font-semibold uppercase tracking-wide text-slate-400">Compiler Status</div><div className="mt-1 text-sm font-semibold text-slate-700">{stats ? stats.message : 'Awaiting compilation'}</div></div></div>
      </div>
      {stats && <div className="m-6 flex gap-3 rounded-xl border border-blue-100 bg-blue-50 p-4 text-sm leading-6 text-blue-900 sm:m-8"><FileJson className="mt-0.5 h-5 w-5 shrink-0 text-blue-600" /><p><strong>Blueprint compiled.</strong> Departments, roles, workflows, and policies were typed and versioned. The relationship extractor built edges for <code className="rounded bg-white/70 px-1">reports_to</code> and <code className="rounded bg-white/70 px-1">depends_on</code>.</p></div>}
    </section>
  );
}
