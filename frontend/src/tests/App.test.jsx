import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { ApiProvider } from '../contexts/ApiContext';
import { SupabaseProvider } from '../contexts/SupabaseContext';
import { ClerkProvider } from '@clerk/clerk-react';
import App from '../App';

// Mock the Clerk provider
jest.mock('@clerk/clerk-react', () => ({
  ClerkProvider: ({ children }) => <div>{children}</div>,
  useUser: () => ({ isSignedIn: true, isLoaded: true }),
  UserButton: () => <div>User Button</div>,
}));

// Mock the contexts
jest.mock('../contexts/ApiContext', () => ({
  ApiProvider: ({ children }) => <div>{children}</div>,
  useApi: () => ({
    isLoading: false,
    scripts: {
      getAll: jest.fn().mockResolvedValue([]),
    },
    auctions: {
      getAll: jest.fn().mockResolvedValue([]),
      getStats: jest.fn().mockResolvedValue({}),
    },
    bidding: {
      getBidConfigs: jest.fn().mockResolvedValue([]),
    },
  }),
}));

jest.mock('../contexts/SupabaseContext', () => ({
  SupabaseProvider: ({ children }) => <div>{children}</div>,
  useSupabase: () => ({
    supabase: {},
    session: null,
    loading: false,
  }),
}));

// Mock the pages
jest.mock('../pages/Dashboard', () => () => <div>Dashboard Page</div>);
jest.mock('../pages/ScriptManagement', () => () => <div>Script Management Page</div>);
jest.mock('../pages/AuctionListing', () => () => <div>Auction Listing Page</div>);
jest.mock('../pages/Statistics', () => () => <div>Statistics Page</div>);

// Mock the components
jest.mock('../components/Layout', () => ({ children }) => (
  <div>
    <div>Layout Component</div>
    {children}
  </div>
));

jest.mock('../components/ProtectedRoute', () => ({ children }) => (
  <div>
    <div>Protected Route</div>
    {children}
  </div>
));

describe('App Component', () => {
  test('renders without crashing', () => {
    render(<App />);
    expect(screen.getByText(/Layout Component/i)).toBeInTheDocument();
  });
});
