import { useEffect, useState } from 'react';
import { RefreshCw, ShieldCheck } from 'lucide-react';

type SecurityReport = {
  controls: {
    cors_origins: string[];
    authentication_required: boolean;
    max_upload_bytes: number;
    security_headers: string[];
    workspace_path_restriction: boolean;
    upload_extension_allowlist: boolean;
  };
  findings: Array<{
    id: string;
    tool: string;
    severity: string;
    rule: string;
    title: string;
    description: string;
    file: string;
    line: number;
  }>;
  summary: { total: number; high: number; medium: number; low: number };
};

export default function Security() {
  const [report, setReport] = useState<SecurityReport | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const runScan = () => {
    setLoading(true);
    setError('');
    fetch('http://localhost:8000/security/scan')
      .then((response) => {
        if (!response.ok) throw new Error(`Security scan failed (${response.status})`);
        return response.json();
      })
      .then(setReport)
      .catch((scanError) => setError(scanError.message))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    runScan();
  }, []);

  if (loading && !report) {
    return <div className="flex items-center gap-3 text-slate-500"><RefreshCw className="h-5 w-5 animate-spin" /> Running security checks...</div>;
  }

  return (
    <div className="mx-auto max-w-7xl space-y-8">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="mb-2 text-xs font-semibold uppercase tracking-[0.2em] text-teal-700">OWASP readiness</p>
          <h1 className="text-4xl font-bold tracking-tight text-slate-900">Security Center</h1>
          <p className="mt-2 max-w-2xl text-slate-500">Current static-analysis findings and API boundary controls for this workspace.</p>
        </div>
        <button onClick={runScan} disabled={loading} className="flex items-center gap-2 rounded-lg bg-teal-600 px-4 py-2 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-teal-700 disabled:opacity-60">
          <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} /> Rescan project
        </button>
      </div>

      {error && <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-800">{error}</div>}

      {report && (
        <>
          <div className="grid gap-4 sm:grid-cols-4">
            {[
              ['Total findings', report.summary.total, 'text-slate-900'],
              ['High', report.summary.high, 'text-red-700'],
              ['Medium', report.summary.medium, 'text-amber-700'],
              ['Low', report.summary.low, 'text-slate-600'],
            ].map(([label, value, color]) => (
              <div key={label} className="rounded-2xl border border-white/80 bg-white/70 p-5 shadow-sm backdrop-blur-xl">
                <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">{label}</p>
                <p className={`mt-2 text-3xl font-bold ${color}`}>{value}</p>
              </div>
            ))}
          </div>

          <section className="rounded-3xl border border-white/80 bg-white/75 p-6 shadow-xl shadow-slate-200/60 backdrop-blur-xl">
            <div className="mb-5 flex items-center gap-3">
              <ShieldCheck className="h-6 w-6 text-teal-700" />
              <div><h2 className="font-bold text-slate-900">API controls</h2><p className="text-sm text-slate-500">Protections currently active at the FastAPI boundary.</p></div>
            </div>
            <div className="grid gap-3 md:grid-cols-2">
              {[
                `CORS origins: ${report.controls.cors_origins.join(', ')}`,
                report.controls.authentication_required ? 'Production API authentication enabled' : 'Local development authentication mode',
                `Upload limit: ${(report.controls.max_upload_bytes / 1024 / 1024).toFixed(0)} MB`,
                `Security headers: ${report.controls.security_headers.length} enabled`,
                report.controls.workspace_path_restriction ? 'Workspace path restriction enabled' : 'Workspace path restriction disabled',
                report.controls.upload_extension_allowlist ? 'Upload extension allow-list enabled' : 'Upload extension allow-list disabled',
              ].map((control) => <div key={control} className="rounded-xl bg-teal-50 px-4 py-3 text-sm text-teal-900">{control}</div>)}
            </div>
          </section>

          <section className="overflow-hidden rounded-3xl border border-white/80 bg-white/75 shadow-xl shadow-slate-200/60 backdrop-blur-xl">
            <div className="border-b border-slate-100 px-6 py-5"><h2 className="font-bold text-slate-900">SAST findings</h2><p className="text-sm text-slate-500">Bandit findings are listed with their source location for remediation.</p></div>
            {report.findings.length === 0 ? (
              <div className="flex items-center gap-3 p-8 text-teal-800"><ShieldCheck className="h-5 w-5" /> No Bandit findings detected.</div>
            ) : (
              <div className="divide-y divide-slate-100">
                {report.findings.map((finding) => (
                  <div key={finding.id} className="grid gap-3 px-6 py-5 md:grid-cols-[100px_1fr_240px]">
                    <span className={`h-fit w-fit rounded-full px-2.5 py-1 text-xs font-bold ${finding.severity.toUpperCase() === 'HIGH' ? 'bg-red-100 text-red-800' : finding.severity.toUpperCase() === 'MEDIUM' ? 'bg-amber-100 text-amber-800' : 'bg-slate-100 text-slate-700'}`}>{finding.severity}</span>
                    <div><p className="font-semibold text-slate-900">{finding.title}</p><p className="mt-1 text-sm text-slate-600">{finding.description}</p><p className="mt-2 text-xs font-mono text-slate-500">{finding.rule}</p></div>
                    <p className="text-xs font-mono break-all text-slate-500">{finding.file}:{finding.line}</p>
                  </div>
                ))}
              </div>
            )}
          </section>
        </>
      )}
    </div>
  );
}
