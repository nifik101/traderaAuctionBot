import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Dashboard from '../pages/Dashboard';

// Mock the API context
jest.mock('../contexts/ApiContext', () => ({
  useApi: () => ({
    isLoading: false,
    scripts: {
      getAll: jest.fn().mockResolvedValue([
        {
          id: 1,
          name: 'Test Script',
          is_active: true,
          schedule: '0 * * * *',
          last_run_at: '2025-04-14T10:00:00Z'
        }
      ]),
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
    },
    bidding: {
      getBidConfigs: jest.fn().mockResolvedValue([
        {
          id: 1,
          auction_id: 1,
          max_bid_amount: 200,
          status: 'pending'
        }
      ]),
    },
  }),
}));

describe('Dashboard Component', () => {
  test('renders dashboard with stats and tables', async () => {
    render(<Dashboard />);
    
    // Check for dashboard title
    expect(screen.getByText(/Dashboard/i)).toBeInTheDocument();
    
    // Check for stat cards (these might be async, so we use findByText)
    expect(await screen.findByText(/Total Auctions/i)).toBeInTheDocument();
    expect(await screen.findByText(/Active Auctions/i)).toBeInTheDocument();
    expect(await screen.findByText(/Pending Bids/i)).toBeInTheDocument();
    
    // Check for section headers
    expect(screen.getByText(/Recent Auctions/i)).toBeInTheDocument();
    expect(screen.getByText(/Active Scripts/i)).toBeInTheDocument();
    
    // Check for table headers
    expect(screen.getByText(/Title/i)).toBeInTheDocument();
    expect(screen.getByText(/Current Price/i)).toBeInTheDocument();
    expect(screen.getByText(/End Time/i)).toBeInTheDocument();
    expect(screen.getByText(/Status/i)).toBeInTheDocument();
  });
  
  test('displays loading state when data is loading', () => {
    // Override the mock to simulate loading
    jest.mock('../contexts/ApiContext', () => ({
      useApi: () => ({
        isLoading: true,
        scripts: { getAll: jest.fn() },
        auctions: { getAll: jest.fn() },
        bidding: { getBidConfigs: jest.fn() },
      }),
    }), { virtual: true });
    
    render(<Dashboard />);
    
    // Check for loading indicator
    expect(screen.getByText(/Loading dashboard data/i)).toBeInTheDocument();
  });
});
