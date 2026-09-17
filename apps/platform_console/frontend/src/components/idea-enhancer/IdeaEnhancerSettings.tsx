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
  const [handshakeStatus, setHandshakeStatus] = useState<{status: 'success' | 'error' | null, message: string}>({status: null, message: ''});

  const handleApiKeyChange = async (key: string) => {
    let newProvider = '';
    if (key.startsWith('sk-ant-')) {
      newProvider = 'Anthropic (Claude)';
    } else if (key.startsWith('sk-') && !key.startsWith('sk-ant-')) {
      newProvider = 'OpenAI (GPT)';
    } else if (key.startsWith('AIza') || key.startsWith('AQ')) {
      newProvider = 'Google (Gemini)';
    } else if (key.length > 10) {
      newProvider = 'Unknown Provider';
    }
    
    setConfig(prev => ({ ...prev, apiKey: key, aiProvider: newProvider }));
    setHandshakeStatus({status: null, message: ''});
    
    if (key.length > 5) {
      setIsCheckingTokens(true);
      setTokenBalance(null);
      
      try {
        const response = await fetch('http://localhost:8000/api/ai/handshake', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ apiKey: key, provider: newProvider }),
        });
        
        const data = await response.json();
        if (data.status === 'success') {
          setConfig(prev => ({ ...prev, aiProvider: data.provider }));
          setHandshakeStatus({status: 'success', message: data.message});
          // Use real quota if provided, otherwise set to null
          setTokenBalance(data.quota?.remaining_tokens ?? null);
        } else {
          setHandshakeStatus({status: 'error', message: data.message});
        }
      } catch (error) {
        setHandshakeStatus({status: 'error', message: 'Failed to connect to backend handshake endpoint'});
      } finally {
        setIsCheckingTokens(false);
      }
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

            {config.apiKey.length > 5 && (
              <div className="animate-fade-in-up space-y-5 pt-2 border-t border-gray-100">
                <div>
                  <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 flex flex-col gap-2">
                    <div className="flex items-center justify-between">
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
                      ) : (
                        <span className="text-sm text-slate-500">
                          Not exposed by provider
                        </span>
                      )}
                    </div>
                    
                    {handshakeStatus.status && (
                      <div className={`mt-2 p-2 text-sm rounded ${handshakeStatus.status === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                        {handshakeStatus.status === 'success' ? '✅ ' : '❌ '} 
                        {handshakeStatus.message}
                      </div>
                    )}
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
