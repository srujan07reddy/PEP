import { useState } from 'react';
import { Key, Server, Database, Brain, CheckCircle2 } from 'lucide-react';

const IdeaEnhancerSettings = () => {
  const [config, setConfig] = useState({
    aiProvider: '',
    apiKey: '',
    useLocalEngine: false,
    localModelUrl: '',
    tokenLimit: 2000,
  });
  const [isSaving, setIsSaving] = useState(false);
  const [isCheckingTokens, setIsCheckingTokens] = useState(false);
  const [tokenBalance, setTokenBalance] = useState<number | null>(null);

  const handleApiKeyChange = (key: string) => {
    let newProvider = '';
    if (key.startsWith('sk-ant-')) {
      newProvider = 'Anthropic (Claude)';
    } else if (key.startsWith('sk-') && !key.startsWith('sk-ant-')) {
      newProvider = 'OpenAI (GPT)';
    } else if (key.startsWith('AIza')) {
      newProvider = 'Google (Gemini)';
    } else if (key.length > 10) {
      newProvider = 'Unknown Provider';
    }
    
    setConfig({ ...config, apiKey: key, aiProvider: newProvider });
    
    if (key.length > 10 && newProvider && newProvider !== 'Unknown Provider') {
      setIsCheckingTokens(true);
      setTokenBalance(null);
      setTimeout(() => {
        setIsCheckingTokens(false);
        setTokenBalance(Math.floor(Math.random() * 5000000) + 1000000); // Mock between 1m - 6m tokens
      }, 1200);
    } else {
      setTokenBalance(null);
    }
  };

  const handleSave = () => {
    setIsSaving(true);
    setTimeout(() => {
      setIsSaving(false);
      alert('Idea Enhancer settings saved!');
    }, 800);
  };

  return (
    <div className="max-w-3xl space-y-6 animate-fade-in-up">
      <div>
        <h2 className="text-xl font-semibold text-gray-800 mb-2">AI Configuration</h2>
        <p className="text-sm text-gray-500 mb-6">Configure the AI connection used by the Idea Enhancer for processing and ideation.</p>
      </div>

      <div className="space-y-6 bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
        
        {/* Toggle for Local vs Cloud */}
        <div className="flex items-center gap-3 pb-4 border-b border-gray-100">
          <input
            type="checkbox"
            id="use-local-engine"
            checked={config.useLocalEngine}
            onChange={(e) => setConfig({ ...config, useLocalEngine: e.target.checked })}
            className="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
          />
          <label htmlFor="use-local-engine" className="text-sm font-medium text-gray-700">
            Use Local / Custom AI Engine
          </label>
        </div>

        {config.useLocalEngine ? (
          <div className="animate-fade-in-up space-y-5">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Local Model API URL</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Server className="h-4 w-4 text-gray-400" />
                </div>
                <input
                  type="text"
                  placeholder="http://localhost:11434/api/generate"
                  value={config.localModelUrl}
                  onChange={(e) => setConfig({ ...config, localModelUrl: e.target.value })}
                  className="pl-10 w-full border-gray-300 border rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 p-2 text-sm"
                />
              </div>
              <p className="text-xs text-gray-500 mt-2">Connect to Ollama, vLLM, or any compatible local endpoint.</p>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Token Limit</label>
              <div className="p-3 bg-green-50 rounded-lg border border-green-200 flex items-center gap-2">
                <Database className="w-5 h-5 text-green-600" />
                <span className="text-sm font-medium text-green-800">Unlimited Tokens (Local Execution)</span>
              </div>
            </div>
          </div>
        ) : (
          <div className="animate-fade-in-up space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">API Key</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Key className="h-4 w-4 text-gray-400" />
                </div>
                <input
                  type="password"
                  placeholder="Paste your sk-..., sk-ant-..., or AIza... key here"
                  value={config.apiKey}
                  onChange={(e) => handleApiKeyChange(e.target.value)}
                  className="pl-10 w-full border-gray-300 border rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 p-2 text-sm"
                />
              </div>
            </div>

            {config.aiProvider && (
              <div className="animate-fade-in-up p-4 bg-blue-50 rounded-lg border border-blue-100 flex items-center gap-3">
                <Brain className="w-5 h-5 text-blue-600" />
                <div>
                  <p className="text-xs text-blue-600 uppercase font-bold tracking-wider">Detected Provider</p>
                  <p className="text-sm font-medium text-blue-900">{config.aiProvider}</p>
                </div>
                {config.aiProvider !== 'Unknown Provider' && <CheckCircle2 className="w-5 h-5 text-green-500 ml-auto" />}
              </div>
            )}

            {config.apiKey.length > 10 && config.aiProvider && config.aiProvider !== 'Unknown Provider' && (
              <div className="animate-fade-in-up space-y-5 pt-2 border-t border-gray-100">
                <div>
                  <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Database className="w-4 h-4 text-indigo-500" />
                      <span className="text-sm font-medium text-slate-700">Account Balance</span>
                    </div>
                    {isCheckingTokens ? (
                      <span className="text-sm text-slate-500 animate-pulse">Checking tokens...</span>
                    ) : tokenBalance !== null ? (
                      <span className="text-sm font-bold text-green-600">
                        {tokenBalance.toLocaleString()} tokens remaining
                      </span>
                    ) : null}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Token Limit per Request</label>
                  <div className="relative">
                     <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <Database className="h-4 w-4 text-gray-400" />
                     </div>
                    <input
                      type="number"
                      min="100"
                      max="128000"
                      value={config.tokenLimit}
                      onChange={(e) => setConfig({ ...config, tokenLimit: parseInt(e.target.value) || 2000 })}
                      className="pl-10 w-full border-gray-300 border rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 p-2 text-sm"
                    />
                  </div>
                  <p className="text-xs text-gray-500 mt-2">Maximum number of tokens to use for a single enhancement process to manage costs.</p>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      <div className="flex justify-end pt-2">
        <button
          onClick={handleSave}
          disabled={isSaving}
          className={`px-6 py-2 rounded-lg font-medium shadow-sm transition-colors flex items-center gap-2 ${
            isSaving ? 'bg-indigo-400 text-white cursor-not-allowed' : 'bg-indigo-600 text-white hover:bg-indigo-700'
          }`}
        >
          {isSaving ? 'Saving...' : 'Save AI Configuration'}
        </button>
      </div>
    </div>
  );
};

export default IdeaEnhancerSettings;
