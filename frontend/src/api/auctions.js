import api from './index';

// Auctions API
export const auctionsApi = {
  getAll: async (filters = {}) => {
    const response = await api.get('/api/auctions', { params: filters });
    return response.data;
  },
  
  getById: async (id) => {
    const response = await api.get(`/api/auctions/${id}`);
    return response.data;
  },
  
  getStats: async () => {
    const response = await api.get('/api/auctions/stats');
    return response.data;
  },
  
  search: async (searchParams) => {
    const response = await api.post('/api/search', searchParams);
    return response.data;
  }
};
