import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { ApiProvider } from '../contexts/ApiContext';
import Dashboard from '../pages/Dashboard';

// Mock the API services
jest.mock('../api/services', () => ({
  __esModule: true,
  default: {
    scripts: {
      getAll: jest.fn().mockResolvedValue([
        {
          id: 1,
          name: 'Test Script',
          is_active: true,
          schedule: '0 * * * *',
          last_run_at: '2025-04-14T10:00:00Z'
        }
      ])
    },
    auctions: {
      getAll: jest.fn().mockResolvedValue([
        {
          id: 1,
          title: 'Test Auction',
          current_price: 150,
          end_time: '2025-04-21T10:00:00Z',
          status: 'active'
        },
        {
          id: 2,
          title: 'Another Auction',
          current_price: 200,
          end_time: '2025-04-22T10:00:00Z',
          status: 'active'
        }
      ]),
      getStats: jest.fn().mockResolvedValue({
        total_auctions: 25,
        active_auctions: 10,
        won_auctions: 5,
        total_spent: 1500
      })
    },
    bidding: {
      getBidConfigs: jest.fn().mockResolvedValue([
        {
          id: 1,
          auction_id: 1,
          max_bid_amount: 200,
          status: 'pending'
        }
      ])
    }
  }
}));

describe('Dashboard Integration Test', () => {
  test('fetches and displays data from API services', async () => {
    render(
      <ApiProvider>
        <Dashboard />
      </ApiProvider>
    );
    
    // Check for loading state initially
    expect(screen.getByText(/Loading dashboard data/i)).toBeInTheDocument();
    
    // Wait for data to load
    await waitFor(() => {
      expect(screen.getByText(/Test Auction/i)).toBeInTheDocument();
    });
    
    // Check that stats are displayed
    expect(screen.getByText(/Total Auctions/i)).toBeInTheDocument();
    expect(screen.getByText(/Active Auctions/i)).toBeInTheDocument();
    
    // Check that script data is displayed
    expect(screen.getByText(/Test Script/i)).toBeInTheDocument();
    
    // Verify API services were called
    expect(require('../api/services').default.scripts.getAll).toHaveBeenCalled();
    expect(require('../api/services').default.auctions.getAll).toHaveBeenCalled();
    expect(require('../api/services').default.bidding.getBidConfigs).toHaveBeenCalled();
  });
});
