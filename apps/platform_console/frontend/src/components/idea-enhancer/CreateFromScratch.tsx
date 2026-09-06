import { useState } from 'react';

const CreateFromScratch = () => {
  const [problemStatement, setProblemStatement] = useState('');
  const [ideaText, setIdeaText] = useState('');
  const [files, setFiles] = useState<FileList | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [formGenerated, setFormGenerated] = useState(false);

  const handleGenerateForm = () => {
    setIsGenerating(true);
    // Simulate AI form generation
    setTimeout(() => {
      setIsGenerating(false);
      setFormGenerated(true);
    }, 1500);
  };

  return (
    <div className="space-y-6">
      <div className="space-y-4">
        <h2 className="text-xl font-semibold text-gray-800">Describe Your Idea</h2>
        <p className="text-sm text-gray-500">Provide documentation, research, or simply describe what you want to build. We support PDF, DOCX, CSV, Excel, MD, and more.</p>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Problem Statement</label>
          <textarea
            className="w-full border-gray-300 border rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 p-3 h-24 mb-4"
            placeholder="What problem are you trying to solve? e.g. Customer support queries take too long to process manually."
            value={problemStatement}
            onChange={(e) => setProblemStatement(e.target.value)}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Idea Description</label>
          <textarea
            className="w-full border-gray-300 border rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 p-3 h-32"
            placeholder="Type your idea here..."
            value={ideaText}
            onChange={(e) => setIdeaText(e.target.value)}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Upload Documents</label>
          <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-lg hover:bg-gray-50 transition-colors">
            <div className="space-y-1 text-center">
              <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
                <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
              <div className="flex text-sm text-gray-600 justify-center">
                <label htmlFor="file-upload" className="relative cursor-pointer bg-white rounded-md font-medium text-blue-600 hover:text-blue-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-blue-500">
                  <span>Upload a file</span>
                  <input id="file-upload" name="file-upload" type="file" className="sr-only" multiple onChange={(e) => setFiles(e.target.files)} accept=".pdf,.doc,.docx,.csv,.xlsx,.xls,.md,.txt" />
                </label>
                <p className="pl-1">or drag and drop</p>
              </div>
              <p className="text-xs text-gray-500">PDF, DOCX, CSV, Excel, MD up to 10MB</p>
              {files && files.length > 0 && (
                <div className="mt-2 text-sm text-green-600">
                  {files.length} file(s) selected
                </div>
              )}
            </div>
          </div>
        </div>

        <button
          onClick={handleGenerateForm}
          disabled={isGenerating || (!(problemStatement || ideaText) && !files)}
          className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white ${isGenerating || (!(problemStatement || ideaText) && !files) ? 'bg-blue-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'}`}
        >
          {isGenerating ? (
            <span className="flex items-center gap-2">
              <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Analyzing Idea...
            </span>
          ) : 'Generate Enhancement Form'}
        </button>
      </div>

      {formGenerated && (
        <div className="mt-8 pt-8 border-t border-gray-200 animate-fade-in-up">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Enhancement Questionnaire</h3>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <p className="text-sm text-blue-800 flex items-start gap-2">
              <span>💡</span>
              AI Assistant: I've analyzed your input. Let's clarify a few points to make this idea robust and actionable. Please answer the following questions.
            </p>
          </div>
          
          <form className="space-y-6">
            <div className="bg-white p-5 border border-gray-200 rounded-lg shadow-sm">
               <label className="block text-sm font-medium text-gray-800 mb-2">1. Who is the primary target audience for this feature?</label>
               <input type="text" className="w-full border-gray-300 border rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 p-2" placeholder="e.g. Enterprise Administrators" />
            </div>
            <div className="bg-white p-5 border border-gray-200 rounded-lg shadow-sm">
               <label className="block text-sm font-medium text-gray-800 mb-2">2. How does this improve upon existing solutions?</label>
               <p className="text-xs text-gray-500 mb-2">I noticed you mentioned a faster workflow, but can you quantify or specify the bottleneck?</p>
               <textarea className="w-full border-gray-300 border rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 p-2 h-24" placeholder="Your response..." />
            </div>
            <div className="bg-white p-5 border border-gray-200 rounded-lg shadow-sm">
               <label className="block text-sm font-medium text-gray-800 mb-2">3. What are the key technical constraints or dependencies?</label>
               <p className="text-xs text-gray-500 mb-2">Based on the problem statement, are there specific frameworks, APIs, or legacy systems we must integrate with?</p>
               <textarea className="w-full border-gray-300 border rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 p-2 h-24" placeholder="Your response..." />
            </div>
            <div className="bg-blue-50 p-5 border border-blue-200 rounded-lg shadow-sm">
               <label className="block text-sm font-medium text-blue-900 mb-2 flex items-center gap-2">
                 <span>🛠️</span> 4. How do you need PEP to help build the software model?
               </label>
               <p className="text-xs text-blue-700 mb-2">Do you need PEP to generate the backend logic, design the database schema, scaffold the UI, or all of the above?</p>
               <textarea className="w-full border-blue-300 border rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 p-2 h-24" placeholder="e.g., I need PEP to generate the database schema and the API endpoints..." />
            </div>
            
            <div className="flex justify-end gap-3 pt-4">
              <button type="button" className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">Save Draft</button>
              <button type="button" className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700">Submit Answers for Enhancement</button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};

export default CreateFromScratch;
