import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

export const getDomains = async () => {
  const { data } = await api.get('/domains');
  return data.data;
};

export const getWorkspaces = async () => {
  const { data } = await api.get('/workspaces');
  return data.data;
};

export const createDomain = async (name: string, absolutePath?: string) => {
  const { data } = await api.post('/domains', { name, absolute_path: absolutePath });
  return data;
};

export const getAgents = async () => {
  const { data } = await api.get('/agents');
  return data.data;
};

export const getStandards = async () => {
  const { data } = await api.get('/standards');
  return data.data;
};

export const runAgent = async ({ agentId, targetDomain, absolutePath }: { agentId: string, targetDomain: string, absolutePath?: string }) => {
  const payload: any = { agent_id: agentId, target_domain: targetDomain };
  if (absolutePath) {
    payload.absolute_path = absolutePath;
  }
  const { data } = await api.post('/agents/run', payload);
  return data;
};

export const runGeneration = async ({ targetDomain }: { targetDomain: string }) => {
  const { data } = await api.post('/generation/run', { target_domain: targetDomain, agent_id: 'gen' });
  return data;
};

export const runDeployment = async ({ targetDomain }: { targetDomain: string }) => {
  const { data } = await api.post('/deployment/run', { target_domain: targetDomain, agent_id: 'dep' });
  return data;
};

export const getAgentDetails = async (agentId: string) => {
  const { data } = await api.get(`/agents/${agentId}`);
  return data;
};

export const createAgent = async (agentId: string) => {
  const { data } = await api.post('/agents', { agent_id: agentId });
  return data;
};

export const updateAgent = async (agentId: string, code: string) => {
  const { data } = await api.put(`/agents/${agentId}`, { code });
  return data;
};

export const getFindings = async () => {
  const { data } = await api.get('/findings');
  return data.data;
};

export const getReports = async () => {
  const { data } = await api.get('/reports');
  return data.data;
};

export const deleteDomain = async (domainId: string) => {
  const { data } = await api.delete(`/domains/${domainId}`);
  return data;
};

export const toggleAgent = async (agentId: string, status: 'active' | 'disabled') => {
  const { data } = await api.patch(`/agents/${agentId}`, { status });
  return data;
};

export const clearReports = async () => {
  const { data } = await api.delete('/reports');
  return data;
};

export const getMessages = async () => {
  const { data } = await api.get('/messages');
  return data.data;
};

export const clearMessages = async () => {
  const { data } = await api.delete('/messages');
  return data;
};

export const getMcpTools = async () => {
  const { data } = await api.get('/mcp/tools');
  return data.data;
};
