import { useState } from 'react';
import { ArrowRight, Edit3, Lightbulb, Settings } from 'lucide-react';
import CreateFromScratch from '../components/idea-enhancer/CreateFromScratch';
import EnhanceExistingIdea from '../components/idea-enhancer/EnhanceExistingIdea';
import IdeaEnhancerSettings from '../components/idea-enhancer/IdeaEnhancerSettings';

const IdeaEnhancer = () => {
  const [activeTab, setActiveTab] = useState<'create' | 'enhance' | 'settings'>('create');

  const sections = [
    {
      id: 'create' as const,
      title: 'Create from Scratch',
      description: 'Turn a raw concept into a clear, actionable brief.',
      icon: Lightbulb,
      accent: 'amber',
    },
    {
      id: 'enhance' as const,
      title: 'Enhance Existing Idea',
      description: 'Analyze documentation and uncover stronger directions.',
      icon: Edit3,
      accent: 'blue',
    },
    {
      id: 'settings' as const,
      title: 'AI Settings',
      description: 'Configure the model and connection used for ideation.',
      icon: Settings,
      accent: 'violet',
    },
  ];

  const activeSection = sections.find((section) => section.id === activeTab)!;

  return (
    <div className="mx-auto max-w-7xl space-y-8">
      <div>
        <p className="mb-2 text-xs font-semibold uppercase tracking-[0.2em] text-teal-700">Workspace</p>
        <h1 className="flex items-center gap-3 text-4xl font-bold tracking-tight text-slate-900">
          <span className="rounded-2xl bg-amber-100 p-2.5 text-amber-700 shadow-sm">
            <Lightbulb className="h-7 w-7" />
          </span>
          Idea Enhancer
        </h1>
        <p className="mt-2 max-w-2xl text-slate-500">Shape early thinking into something your team can build, test, and improve.</p>
      </div>

      <div className="grid gap-6 lg:grid-cols-[280px_minmax(0,1fr)] lg:items-start">
        <aside className="space-y-3">
          <div className="mb-4 px-1">
            <p className="text-sm font-semibold text-slate-800">Choose a direction</p>
            <p className="mt-1 text-xs leading-relaxed text-slate-500">Your workspace opens beside the selected tool.</p>
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
                    ? 'border-teal-200 bg-white shadow-lg shadow-teal-100/70 lg:translate-x-2'
                    : 'border-white/80 bg-white/55 shadow-sm hover:-translate-y-0.5 hover:border-slate-200 hover:bg-white hover:shadow-md'
                }`}
              >
                <div className="flex items-start gap-3">
                  <span className={`rounded-xl p-2.5 ${
                    section.accent === 'amber' ? 'bg-amber-100 text-amber-700' :
                    section.accent === 'blue' ? 'bg-cyan-100 text-cyan-700' :
                    'bg-violet-100 text-violet-700'
                  }`}>
                    <Icon className="h-5 w-5" />
                  </span>
                  <span className="min-w-0 flex-1">
                    <span className="block text-sm font-semibold text-slate-800">{section.title}</span>
                    <span className="mt-1 block text-xs leading-relaxed text-slate-500">{section.description}</span>
                  </span>
                  <ArrowRight className={`mt-1 h-4 w-4 shrink-0 transition-transform ${isActive ? 'translate-x-0 text-teal-700' : '-translate-x-1 text-slate-300 group-hover:translate-x-0 group-hover:text-slate-500'}`} />
                </div>
              </button>
            );
          })}
        </aside>

        <section key={activeTab} className="min-w-0 animate-[slide-in_350ms_ease-out] rounded-3xl border border-white/80 bg-white/75 p-5 shadow-xl shadow-slate-200/60 backdrop-blur-xl sm:p-8">
          <div className="mb-6 flex items-center gap-3 border-b border-slate-100 pb-5">
            <span className="rounded-xl bg-slate-100 p-2 text-slate-600"><activeSection.icon className="h-5 w-5" /></span>
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.16em] text-teal-700">Active tool</p>
              <h2 className="mt-1 text-xl font-bold text-slate-900">{activeSection.title}</h2>
            </div>
          </div>
          {activeTab === 'create' && <CreateFromScratch />}
          {activeTab === 'enhance' && <EnhanceExistingIdea />}
          {activeTab === 'settings' && <IdeaEnhancerSettings />}
        </section>
      </div>
    </div>
  );
};

export default IdeaEnhancer;
