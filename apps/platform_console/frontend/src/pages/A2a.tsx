import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getMessages, clearMessages } from '../lib/api';
import { Mail, RefreshCw, Trash2, ArrowRight } from 'lucide-react';

export default function A2a() {
  const queryClient = useQueryClient();
  const { data: messages, isLoading } = useQuery({ queryKey: ['messages'], queryFn: getMessages });

  const clearMessagesMutation = useMutation({
    mutationFn: clearMessages,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['messages'] });
    }
  });

  if (isLoading) return <div className="text-gray-500 flex items-center gap-2"><RefreshCw className="animate-spin w-4 h-4" /> Loading A2A messages...</div>;

  return (
    <div>
      <div className="flex justify-between items-start mb-6">
        <div>
          <h1 className="text-3xl font-bold mb-2 text-gray-800 flex items-center gap-2">
            <Mail className="w-8 h-8 text-blue-600" />
            A2A Dashboard
          </h1>
          <p className="text-gray-600 max-w-3xl">
            Live feed of asynchronous Agent-to-Agent (A2A) messages sent during pipeline executions.
          </p>
        </div>
        
        <button 
          onClick={() => {
            if(window.confirm('Are you sure you want to clear all A2A messages?')) {
              clearMessagesMutation.mutate();
            }
          }}
          disabled={!messages || messages.length === 0}
          className="text-sm bg-white border border-red-200 hover:bg-red-50 text-red-600 px-4 py-2 rounded-md shadow-sm transition-colors shrink-0 flex items-center gap-2 disabled:opacity-50"
        >
          <Trash2 className="w-4 h-4" />
          Clear Mailbox
        </button>
      </div>

      <div className="space-y-4">
        {(!messages || messages.length === 0) ? (
          <div className="bg-white border border-gray-200 rounded-lg p-12 text-center">
            <Mail className="w-12 h-12 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-1">Mailbox is empty</h3>
            <p className="text-gray-500">Run a domain execution pipeline to see agents collaborate.</p>
          </div>
        ) : (
          messages.map((msg: any, index: number) => (
            <div key={index} className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
              <div className="bg-slate-50 px-4 py-3 border-b border-gray-200 flex justify-between items-center">
                <div className="flex items-center gap-3">
                  <span className="font-mono text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded-md">{msg.sender}</span>
                  <ArrowRight className="w-4 h-4 text-gray-400" />
                  <span className="font-mono text-sm bg-purple-100 text-purple-800 px-2 py-1 rounded-md">{msg.receiver}</span>
                </div>
                <div className="flex items-center gap-4 text-sm text-gray-500">
                  <span className="bg-gray-200 text-gray-700 px-2 py-1 rounded text-xs font-semibold uppercase tracking-wider">{msg.topic}</span>
                  <span>{new Date(msg.timestamp).toLocaleString()}</span>
                </div>
              </div>
              <div className="p-4 bg-gray-900 text-gray-100 font-mono text-sm overflow-x-auto">
                <pre>{JSON.stringify(msg.payload, null, 2)}</pre>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
