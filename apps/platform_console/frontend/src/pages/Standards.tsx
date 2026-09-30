import { Link } from 'react-router-dom';

const standardsList = [
  { area: 'Engine Architecture & Contracts', status: 'Implemented', statusColor: 'bg-emerald-500', evidence: 'Multi-engine interfaces and Engine Optimizer built' },
  { area: 'Code Extraction', status: 'Implemented', statusColor: 'bg-emerald-500', evidence: 'PEP Code Model & Tree-sitter adapter implemented' },
  { area: 'Text Extraction', status: 'Implemented', statusColor: 'bg-emerald-500', evidence: 'PEP Text Model & NLP++/Transformer ensemble implemented' },
  { area: 'Knowledge Convergence', status: 'Implemented', statusColor: 'bg-emerald-500', evidence: 'Unified Evidence Model established' },
  { area: 'Knowledge Compilation', status: 'Implemented', statusColor: 'bg-emerald-500', evidence: 'Knowledge Compiler resolving cross-domain relationships' },
  { area: 'Infrastructure Abstraction', status: 'Implemented', statusColor: 'bg-emerald-500', evidence: 'KnowledgeStore with Neo4j, Qdrant, Postgres providers' },
  { area: 'Intelligence Engines', status: 'Implemented', statusColor: 'bg-emerald-500', evidence: 'Security, Architecture, Quality, and Organization analysis' },
  { area: 'Assessments & Traceability', status: 'Implemented', statusColor: 'bg-emerald-500', evidence: 'Recommendations strictly mapped to source Evidence' },
  { area: 'Decision Board (ADRs)', status: 'Implemented', statusColor: 'bg-emerald-500', evidence: 'Automated engineering Decision model established' },
  { area: 'Evolution & Drift Tracking', status: 'Implemented', statusColor: 'bg-emerald-500', evidence: 'Evolution Engine detects semantic T1 vs T2 drift' },
];

const evidenceLevels = [
  { level: 'LEVEL 0 — CONCEPT', desc: 'The requirement has been identified.', evidence: 'Architecture discussion / requirement.', progress: '100%', color: 'bg-emerald-500' },
  { level: 'LEVEL 1 — DESIGNED', desc: 'The architecture or interface has been defined.', evidence: 'Schema / interface / architecture specification.', progress: '100%', color: 'bg-emerald-500' },
  { level: 'LEVEL 2 — IMPLEMENTED', desc: 'The capability exists in the codebase.', evidence: 'Implementation + successful test.', progress: '100%', color: 'bg-emerald-500' },
  { level: 'LEVEL 3 — VALIDATED', desc: 'The capability has been tested against representative workloads.', evidence: 'Integration/E2E test, benchmark, or evaluation results.', progress: '65%', color: 'bg-teal-500' },
  { level: 'LEVEL 4 — PRODUCTION VERIFIED', desc: 'The capability has demonstrated reliability under actual operational conditions.', evidence: 'Production metrics, incident history, operational validation.', progress: '10%', color: 'bg-blue-600' },
];

export default function Standards() {
  return (
    <div className="min-h-full -m-8 bg-slate-50 p-8 text-slate-800">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">PEP Platform Standards</h1>
          <p className="mt-2 text-slate-600 max-w-3xl">
            PEP follows a standardized processing framework for transforming heterogeneous resources into structured, contextualized, and traceable intelligence.
          </p>
        </div>
        <Link to="/" className="text-sm font-medium text-teal-600 hover:text-teal-700 hover:underline">
          &larr; Back to Dashboard
        </Link>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column - Standards Table */}
        <div className="lg:col-span-2 space-y-8">
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="mb-4 text-xl font-semibold text-slate-800 border-b pb-3">Platform Readiness & Implementation</h2>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm text-slate-600">
                <thead className="bg-slate-50 text-xs uppercase text-slate-500">
                  <tr>
                    <th className="px-4 py-3 font-medium">Area</th>
                    <th className="px-4 py-3 font-medium">Status</th>
                    <th className="px-4 py-3 font-medium">Evidence State</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {standardsList.map((st, i) => (
                    <tr key={i} className="hover:bg-slate-50 transition-colors">
                      <td className="px-4 py-3 font-medium text-slate-700">{st.area}</td>
                      <td className="px-4 py-3">
                        <span className="inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-medium bg-slate-100 text-slate-700">
                          <span className={`h-2 w-2 rounded-full ${st.statusColor}`}></span>
                          {st.status}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-slate-500">{st.evidence}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="mb-4 text-xl font-semibold text-slate-800 border-b pb-3">PEP Working Procedure Pipeline</h2>
            <div className="relative mt-6 flex flex-col items-start gap-4 pb-4">
              {[
                { name: '1. Extraction', desc: 'Tree-sitter, NLP++, Semgrep' },
                { name: '2. Normalization', desc: 'PEP Code Model & Text Model' },
                { name: '3. Convergence', desc: 'Unified Evidence Model' },
                { name: '4. Compilation', desc: 'Knowledge Graph Construction' },
                { name: '5. Analysis', desc: 'Intelligence Engines (Security, Architecture)' },
                { name: '6. Traceability', desc: 'Findings & Recommendations' },
                { name: '7. Action', desc: 'Decision Board (Automated ADRs)' },
                { name: '8. Evolution', desc: 'T1 vs T2 Semantic Drift Detection' }
              ].map((step, idx, arr) => (
                <div key={idx} className="relative flex w-full items-start gap-4 group">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-teal-100 text-teal-700 font-bold shadow-sm z-10 group-hover:scale-110 transition-transform">
                    {idx + 1}
                  </div>
                  {idx !== arr.length - 1 && (
                    <div className="absolute left-5 top-10 bottom-[-16px] w-[2px] bg-teal-100 -translate-x-1/2"></div>
                  )}
                  <div className="flex-1 rounded-lg border border-slate-100 bg-slate-50 p-4 transition-all group-hover:border-teal-200 group-hover:shadow-md">
                    <h3 className="font-semibold text-slate-800 uppercase tracking-wider text-sm">{step.name}</h3>
                    <p className="mt-1 text-sm text-slate-500">{step.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column - Evidence Maturity */}
        <div className="space-y-8">
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="mb-4 text-xl font-semibold text-slate-800 border-b pb-3">Evidence Maturity Model</h2>
            <div className="space-y-6 mt-4">
              {evidenceLevels.map((lvl, i) => (
                <div key={i}>
                  <div className="flex justify-between items-center mb-1">
                    <h3 className="text-sm font-bold text-slate-700">{lvl.level}</h3>
                    <span className="text-xs font-medium text-slate-500">{lvl.progress}</span>
                  </div>
                  <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden mb-2">
                    <div className={`h-full ${lvl.color} rounded-full transition-all duration-1000`} style={{ width: lvl.progress }}></div>
                  </div>
                  <p className="text-xs text-slate-600">{lvl.desc}</p>
                  <p className="text-xs text-slate-500 mt-1"><span className="font-semibold">Evidence:</span> {lvl.evidence}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-xl border border-slate-200 bg-teal-50 p-6 shadow-sm">
            <h2 className="mb-2 text-lg font-semibold text-teal-900">The PEP Contract</h2>
            <ul className="list-disc pl-5 text-sm text-teal-800 space-y-2 mt-4">
              <li>Every external input is treated as untrusted.</li>
              <li>Every major resource receives a stable UUID identity.</li>
              <li>Processing components expose defined inputs and outputs (BaseEngine).</li>
              <li>Extracted information retains source provenance wherever possible (Evidence Model).</li>
              <li>Core application logic must not depend directly on a single AI/parsing provider (Engine Optimizer).</li>
              <li>Secrets must never be exposed through source code, logs, prompts, or responses.</li>
              <li>Decisions must be 100% explainable and traceable back to source evidence.</li>
            </ul>
            <p className="mt-4 text-xs font-medium text-teal-700 italic border-t border-teal-200 pt-3">
              "No green status without proof."
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
