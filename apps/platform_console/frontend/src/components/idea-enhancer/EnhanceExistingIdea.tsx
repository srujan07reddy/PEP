import { useState } from 'react';

const mockExistingIdeas = [
  { id: 1, title: 'Workflow Automation Agent', status: 'In Progress', content: 'Architecture diagram and initial scripts for automating JIRA to GitHub issues.' },
  { id: 2, title: 'Data Ingestion Pipeline', status: 'Saved', content: 'Python script for reading CSV and inserting into Postgres with chunking.' }
];

const EnhanceExistingIdea = () => {
  const [selectedIdea, setSelectedIdea] = useState<any>(null);
  const [inputText, setInputText] = useState('');
  const [files, setFiles] = useState<FileList | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisComplete, setAnalysisComplete] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  const handleSelectIdea = (idea: any) => {
    setSelectedIdea(idea);
    setInputText(idea.content);
    setAnalysisComplete(false);
  };

  const handleAnalyze = () => {
    setIsAnalyzing(true);
    setTimeout(() => {
      setIsAnalyzing(false);
      setAnalysisComplete(true);
    }, 2000);
  };

  const handleSaveProgress = () => {
    setIsSaving(true);
    setTimeout(() => {
      setIsSaving(false);
      alert('Progress saved successfully!');
    }, 1000);
  };

  return (
    <div className="flex flex-col md:flex-row gap-6">
      {/* Sidebar for Existing Ideas */}
      <div className="w-full md:w-1/3 space-y-4 border-r border-gray-200 pr-4">
        <h3 className="font-semibold text-gray-800">Your Existing Ideas</h3>
        <div className="space-y-3">
          {mockExistingIdeas.map((idea) => (
            <div
              key={idea.id}
              onClick={() => handleSelectIdea(idea)}
              className={`p-3 rounded-lg border cursor-pointer transition-colors ${selectedIdea?.id === idea.id ? 'border-indigo-500 bg-indigo-50' : 'border-gray-200 hover:border-indigo-300 hover:bg-gray-50'}`}
            >
              <h4 className="font-medium text-sm text-gray-900">{idea.title}</h4>
              <span className={`text-xs px-2 py-0.5 rounded-full mt-2 inline-block ${idea.status === 'In Progress' ? 'bg-blue-100 text-blue-700' : 'bg-green-100 text-green-700'}`}>
                {idea.status}
              </span>
            </div>
          ))}
        </div>
        <button
          onClick={() => { setSelectedIdea(null); setInputText(''); setAnalysisComplete(false); }}
          className="w-full py-2 border border-dashed border-gray-300 text-sm text-gray-600 rounded-lg hover:bg-gray-50 hover:text-gray-900 transition-colors"
        >
          + Enhance New Idea
        </button>
      </div>

      {/* Main Content Area */}
      <div className="w-full md:w-2/3 space-y-6">
        {!analysisComplete ? (
          <div className="space-y-4 fade-in">
            <h2 className="text-xl font-semibold text-gray-800">
              {selectedIdea ? `Enhancing: ${selectedIdea.title}` : 'Enhance Existing Idea'}
            </h2>
            <p className="text-sm text-gray-500">Upload code snippets, architecture diagrams, or documentation to get AI-driven analysis and ideation for improvements.</p>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Context / Documentation</label>
              <textarea
                className="w-full border-gray-300 border rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 p-3 h-48 font-mono text-sm"
                placeholder="Paste your existing code, JSON, or markdown here..."
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Upload Additional Context</label>
              <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-lg hover:bg-gray-50 transition-colors">
                <div className="space-y-1 text-center">
                  <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
                    <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                  <div className="flex text-sm text-gray-600 justify-center">
                    <label htmlFor="enhance-file-upload" className="relative cursor-pointer bg-white rounded-md font-medium text-blue-600 hover:text-blue-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-blue-500">
                      <span>Upload files</span>
                      <input id="enhance-file-upload" name="enhance-file-upload" type="file" className="sr-only" multiple onChange={(e) => setFiles(e.target.files)} accept=".pdf,.doc,.docx,.csv,.xlsx,.xls,.md,.txt,.py,.ts,.tsx,.js,.json" />
                    </label>
                    <p className="pl-1">or drag and drop</p>
                  </div>
                  <p className="text-xs text-gray-500">Supports code files and documents up to 10MB</p>
                  {files && files.length > 0 && (
                    <div className="mt-2 text-sm text-green-600">
                      {files.length} file(s) selected
                    </div>
                  )}
                </div>
              </div>
            </div>

            <button
              onClick={handleAnalyze}
              disabled={isAnalyzing || (!inputText && !files)}
              className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white ${isAnalyzing || (!inputText && !files) ? 'bg-indigo-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700'}`}
            >
              {isAnalyzing ? (
                <span className="flex items-center gap-2">
                  <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Analyzing Context...
                </span>
              ) : 'Analyze and Ideate'}
            </button>
          </div>
        ) : (
          <div className="space-y-6 animate-fade-in-up">
            <div className="flex justify-between items-center border-b border-gray-200 pb-4">
              <h3 className="text-2xl font-bold text-gray-900">Analysis & Ideation Results</h3>
              <button onClick={() => setAnalysisComplete(false)} className="text-sm text-blue-600 hover:text-blue-800">Edit Context</button>
            </div>

            <div className="grid grid-cols-1 gap-6">
              <div className="bg-white p-5 border border-gray-200 rounded-xl shadow-sm">
                <h4 className="text-lg font-semibold text-gray-800 flex items-center gap-2 mb-4">
                  <span className="text-purple-500">Analysis</span> Deep Analysis
                </h4>
                <div className="space-y-3 text-sm text-gray-600">
                  <p><strong>Architecture Overview:</strong> {selectedIdea ? 'This relates to your existing architecture design. Validating current state.' : 'The provided code appears to be a React component utilizing state management.'}</p>
                  <p><strong>Identified Bottlenecks:</strong> Current state updates might cause unnecessary re-renders when the file list is large.</p>
                </div>
              </div>

              <div className="bg-gradient-to-br from-indigo-50 to-blue-50 p-5 border border-indigo-100 rounded-xl shadow-sm">
                <h4 className="text-lg font-semibold text-indigo-900 flex items-center gap-2 mb-4">
                  <span className="text-yellow-500">Ideas</span> Enhancement Ideas
                </h4>
                <ul className="space-y-4 text-sm text-indigo-800">
                  <li className="flex gap-2">
                    <input type="checkbox" className="mt-1 rounded text-indigo-600 focus:ring-indigo-500" defaultChecked />
                    <span><strong>Implement Debouncing:</strong> Add debouncing to text inputs to reduce the frequency of AI analysis triggers.</span>
                  </li>
                  <li className="flex gap-2">
                    <input type="checkbox" className="mt-1 rounded text-indigo-600 focus:ring-indigo-500" />
                    <span><strong>Chunked Uploads:</strong> Switch to a chunked upload mechanism to improve reliability and provide progress bars.</span>
                  </li>
                </ul>
              </div>
            </div>
            
            <div className="pt-4 flex gap-3">
               <button 
                 onClick={handleSaveProgress}
                 disabled={isSaving}
                 className={`flex-1 text-white py-2 rounded-lg font-medium shadow-sm transition-colors flex justify-center items-center gap-2 ${isSaving ? 'bg-indigo-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700'}`}
               >
                 {isSaving ? 'Saving...' : (selectedIdea ? 'Update Existing Idea' : 'Save as New Idea')}
               </button>
               <button className="flex-1 bg-white border border-gray-300 text-gray-700 py-2 rounded-lg font-medium hover:bg-gray-50 transition-colors shadow-sm">Export Report</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default EnhanceExistingIdea;
