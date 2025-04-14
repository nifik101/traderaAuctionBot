import api from './index';

// Bidding API
export const biddingApi = {
  getBidConfigs: async () => {
    const response = await api.get('/api/bid-configs');
    return response.data;
  },
  
  createBidConfig: async (auctionId, bidConfig) => {
    const response = await api.post(`/api/auctions/${auctionId}/bid-config`, bidConfig);
    return response.data;
  },
  
  updateBidConfig: async (auctionId, bidConfig) => {
    const response = await api.put(`/api/auctions/${auctionId}/bid-config`, bidConfig);
    return response.data;
  },
  
  deleteBidConfig: async (auctionId) => {
    await api.delete(`/api/auctions/${auctionId}/bid-config`);
    return true;
  },
  
  getBids: async () => {
    const response = await api.get('/api/bids');
    return response.data;
  }
};
