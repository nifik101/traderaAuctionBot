import api from './index';

// Scripts API
export const scriptsApi = {
  getAll: async () => {
    const response = await api.get('/api/scripts');
    return response.data;
  },
  
  getById: async (id) => {
    const response = await api.get(`/api/scripts/${id}`);
    return response.data;
  },
  
  create: async (script) => {
    const response = await api.post('/api/scripts', script);
    return response.data;
  },
  
  update: async (id, script) => {
    const response = await api.put(`/api/scripts/${id}`, script);
    return response.data;
  },
  
  delete: async (id) => {
    await api.delete(`/api/scripts/${id}`);
    return true;
  },
  
  toggle: async (id) => {
    const response = await api.put(`/api/scripts/${id}/toggle`);
    return response.data;
  }
};
