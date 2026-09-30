import { Link } from 'react-router-dom';

const standardsList = [
  { area: 'Input Standard', status: 'In Progress', statusColor: 'bg-blue-500', evidence: 'Architecture and requirements established' },
  { area: 'Processing Standard', status: 'In Progress', statusColor: 'bg-blue-500', evidence: 'Processing technologies investigated' },
  { area: 'Multimodal Understanding', status: 'In Progress', statusColor: 'bg-blue-500', evidence: 'NLP/diagram/visual requirements established' },
  { area: 'Structured Representation', status: 'Partially Defined', statusColor: 'bg-yellow-500', evidence: 'Data/provenance model established conceptually' },
  { area: 'AI / Model Standard', status: 'In Progress', statusColor: 'bg-blue-500', evidence: 'Provider abstraction and usage requirements defined' },
  { area: 'Context & Retrieval', status: 'Partially Defined', statusColor: 'bg-yellow-500', evidence: 'Retrieval requirements established' },
  { area: 'Reasoning & Grounding', status: 'Partially Defined', statusColor: 'bg-yellow-500', evidence: 'Grounding requirements established' },
  { area: 'Output Standard', status: 'Partially Defined', statusColor: 'bg-yellow-500', evidence: 'Output requirements established' },
  { area: 'Security & Privacy', status: 'Partially Defined', statusColor: 'bg-yellow-500', evidence: 'Security requirements identified' },
  { area: 'Extensibility & Integration', status: 'In Progress', statusColor: 'bg-blue-500', evidence: 'Open-source integration evaluated' },
  { area: 'Reliability & Observability', status: 'Planned', statusColor: 'bg-gray-300', evidence: 'Standards identified, implementation pending' },
  { area: 'Versioning & Governance', status: 'Planned', statusColor: 'bg-gray-300', evidence: 'Requirements identified, implementation pending' },
];

const evidenceLevels = [
  { level: 'LEVEL 0 — CONCEPT', desc: 'The requirement has been identified.', evidence: 'Architecture discussion / requirement.', progress: '100%', color: 'bg-emerald-500' },
  { level: 'LEVEL 1 — DESIGNED', desc: 'The architecture or interface has been defined.', evidence: 'Schema / interface / architecture specification.', progress: '65%', color: 'bg-teal-500' },
  { level: 'LEVEL 2 — IMPLEMENTED', desc: 'The capability exists in the codebase.', evidence: 'Implementation + successful test.', progress: '35%', color: 'bg-cyan-500' },
  { level: 'LEVEL 3 — VALIDATED', desc: 'The capability has been tested against representative workloads.', evidence: 'Integration/E2E test, benchmark, or evaluation results.', progress: '15%', color: 'bg-sky-500' },
  { level: 'LEVEL 4 — PRODUCTION VERIFIED', desc: 'The capability has demonstrated reliability under actual operational conditions.', evidence: 'Production metrics, incident history, operational validation.', progress: '5%', color: 'bg-blue-600' },
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
                { name: 'Input Validation', desc: 'Identity, Content & Integrity' },
                { name: 'Processing', desc: 'Extraction, OCR / NLP, Vision' },
                { name: 'Understanding', desc: 'Text, Tables, Images, Diagrams, Flowcharts' },
                { name: 'Structuring', desc: 'Entities, Relationships, Context' },
                { name: 'AI / Reasoning', desc: 'Models, Context, Retrieval' },
                { name: 'Grounding', desc: 'Evidence, Provenance' },
                { name: 'Output', desc: 'Answer, Citation, Structure' }
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
              <li>Every major resource receives a stable identity.</li>
              <li>Processing components expose defined inputs and outputs.</li>
              <li>Extracted information retains source provenance wherever possible.</li>
              <li>Core application logic must not depend directly on a single AI provider.</li>
              <li>Secrets must never be exposed through source code, logs, prompts, or responses.</li>
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
