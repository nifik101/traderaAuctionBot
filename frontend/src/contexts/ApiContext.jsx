import React, { useContext, createContext, useState, useEffect } from 'react';
import apiServices from '../api/services';

// Create API context
const ApiContext = createContext(null);

export function ApiProvider({ children }) {
  const [isLoading, setIsLoading] = useState(false);

  // Create API service wrappers with loading state
  const scripts = {
    getAll: async () => {
      setIsLoading(true);
      try {
        return await apiServices.scripts.getAll();
      } catch (error) {
        console.error('Error fetching scripts:', error);
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    getById: async (id) => {
      setIsLoading(true);
      try {
        return await apiServices.scripts.getById(id);
      } catch (error) {
        console.error(`Error fetching script ${id}:`, error);
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    create: async (script) => {
      setIsLoading(true);
      try {
        return await apiServices.scripts.create(script);
      } catch (error) {
        console.error('Error creating script:', error);
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    update: async (id, script) => {
      setIsLoading(true);
      try {
        return await apiServices.scripts.update(id, script);
      } catch (error) {
        console.error(`Error updating script ${id}:`, error);
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    delete: async (id) => {
      setIsLoading(true);
      try {
        return await apiServices.scripts.delete(id);
      } catch (error) {
        console.error(`Error deleting script ${id}:`, error);
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    toggle: async (id) => {
      setIsLoading(true);
      try {
        return await apiServices.scripts.toggle(id);
      } catch (error) {
        console.error(`Error toggling script ${id}:`, error);
        throw error;
      } finally {
        setIsLoading(false);
      }
    }
  };

  const auctions = {
    getAll: async (filters = {}) => {
      setIsLoading(true);
      try {
        return await apiServices.auctions.getAll(filters);
      } catch (error) {
        console.error('Error fetching auctions:', error);
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    getById: async (id) => {
      setIsLoading(true);
      try {
        return await apiServices.auctions.getById(id);
      } catch (error) {
        console.error(`Error fetching auction ${id}:`, error);
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    getStats: async () => {
      setIsLoading(true);
      try {
        return await apiServices.auctions.getStats();
      } catch (error) {
        console.error('Error fetching auction stats:', error);
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    search: async (searchParams) => {
      setIsLoading(true);
      try {
        return await apiServices.auctions.search(searchParams);
      } catch (error) {
        console.error('Error searching auctions:', error);
        throw error;
      } finally {
        setIsLoading(false);
      }
    }
  };

  const bidding = {
    getBidConfigs: async () => {
      setIsLoading(true);
      try {
        return await apiServices.bidding.getBidConfigs();
      } catch (error) {
        console.error('Error fetching bid configs:', error);
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    createBidConfig: async (auctionId, bidConfig) => {
      setIsLoading(true);
      try {
        return await apiServices.bidding.createBidConfig(auctionId, bidConfig);
      } catch (error) {
        console.error(`Error creating bid config for auction ${auctionId}:`, error);
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    updateBidConfig: async (auctionId, bidConfig) => {
      setIsLoading(true);
      try {
        return await apiServices.bidding.updateBidConfig(auctionId, bidConfig);
      } catch (error) {
        console.error(`Error updating bid config for auction ${auctionId}:`, error);
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    deleteBidConfig: async (auctionId) => {
      setIsLoading(true);
      try {
        return await apiServices.bidding.deleteBidConfig(auctionId);
      } catch (error) {
        console.error(`Error deleting bid config for auction ${auctionId}:`, error);
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    getBids: async () => {
      setIsLoading(true);
      try {
        return await apiServices.bidding.getBids();
      } catch (error) {
        console.error('Error fetching bids:', error);
        throw error;
      } finally {
        setIsLoading(false);
      }
    }
  };

  const value = {
    isLoading,
    scripts,
    auctions,
    bidding
  };

  return <ApiContext.Provider value={value}>{children}</ApiContext.Provider>;
}

export function useApi() {
  const context = useContext(ApiContext);
  if (context === null) {
    throw new Error('useApi must be used within an ApiProvider');
  }
  return context;
}
