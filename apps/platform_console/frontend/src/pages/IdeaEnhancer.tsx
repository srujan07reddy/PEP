import { useState } from 'react';
import { Lightbulb, Edit3, Settings } from 'lucide-react';
import CreateFromScratch from '../components/idea-enhancer/CreateFromScratch';
import EnhanceExistingIdea from '../components/idea-enhancer/EnhanceExistingIdea';
import IdeaEnhancerSettings from '../components/idea-enhancer/IdeaEnhancerSettings';

const IdeaEnhancer = () => {
  const [activeTab, setActiveTab] = useState<'create' | 'enhance' | 'settings'>('create');

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 tracking-tight">Idea Enhancer</h1>
          <p className="text-gray-500 mt-2">Elevate your concepts or refine existing documentation with AI.</p>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div className="flex border-b border-gray-200">
          <button
            onClick={() => setActiveTab('create')}
            className={`flex-1 py-4 text-sm font-medium text-center transition-colors flex items-center justify-center gap-2 ${
              activeTab === 'create'
                ? 'bg-blue-50 text-blue-700 border-b-2 border-blue-600'
                : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
            }`}
          >
            <Lightbulb className="w-4 h-4" />
            Create from Scratch
          </button>
          <button
            onClick={() => setActiveTab('enhance')}
            className={`flex-1 py-4 text-sm font-medium text-center transition-colors flex items-center justify-center gap-2 ${
              activeTab === 'enhance'
                ? 'bg-blue-50 text-blue-700 border-b-2 border-blue-600'
                : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
            }`}
          >
            <Edit3 className="w-4 h-4" />
            Enhance Existing Idea
          </button>
          <button
            onClick={() => setActiveTab('settings')}
            className={`flex-1 py-4 text-sm font-medium text-center transition-colors flex items-center justify-center gap-2 ${
              activeTab === 'settings'
                ? 'bg-blue-50 text-blue-700 border-b-2 border-blue-600'
                : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
            }`}
          >
            <Settings className="w-4 h-4" />
            AI Settings
          </button>
        </div>
        
        <div className="p-6">
          {activeTab === 'create' && <CreateFromScratch />}
          {activeTab === 'enhance' && <EnhanceExistingIdea />}
          {activeTab === 'settings' && <IdeaEnhancerSettings />}
        </div>
      </div>
    </div>
  );
};

export default IdeaEnhancer;
