import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import App from '../App';
import { ApiProvider } from '../contexts/ApiContext';
import { SupabaseProvider } from '../contexts/SupabaseContext';

// Mock the Clerk provider
jest.mock('@clerk/clerk-react', () => ({
  ClerkProvider: ({ children }) => <div>{children}</div>,
  useUser: () => ({ isSignedIn: true, isLoaded: true }),
  UserButton: () => <div>User Button</div>,
}));

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

describe('App Integration Test', () => {
  test('renders the application with authenticated user and loads data', async () => {
    render(
      <BrowserRouter>
        <ApiProvider>
          <SupabaseProvider>
            <App />
          </SupabaseProvider>
        </ApiProvider>
      </BrowserRouter>
    );
    
    // Check that the layout is rendered
    expect(screen.getByText(/Tradera Assistant/i)).toBeInTheDocument();
    
    // Wait for dashboard to load (default route)
    await waitFor(() => {
      expect(screen.getByText(/Dashboard/i)).toBeInTheDocument();
    });
    
    // Verify API services were called
    expect(require('../api/services').default.scripts.getAll).toHaveBeenCalled();
    expect(require('../api/services').default.auctions.getAll).toHaveBeenCalled();
  });
});
