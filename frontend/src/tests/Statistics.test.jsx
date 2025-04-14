import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Statistics from '../pages/Statistics';

// Mock the API context
jest.mock('../contexts/ApiContext', () => ({
  useApi: () => ({
    isLoading: false,
    auctions: {
      getStats: jest.fn().mockResolvedValue({
        total_auctions: 25,
        active_auctions: 10,
        ended_auctions: 15,
        won_auctions: 5,
        lost_auctions: 10,
        total_spent: 1500,
        average_price: 300,
        categories: [
          { name: 'Electronics', count: 10 },
          { name: 'Clothing', count: 8 },
          { name: 'Home', count: 7 }
        ],
        end_time_distribution: [
          { date: '2025-04-15', count: 3 },
          { date: '2025-04-16', count: 5 },
          { date: '2025-04-17', count: 2 }
        ]
      })
    }
  }),
}));

// Mock chart components
jest.mock('react-chartjs-2', () => ({
  Bar: () => <div data-testid="bar-chart">Bar Chart</div>,
  Pie: () => <div data-testid="pie-chart">Pie Chart</div>,
  Line: () => <div data-testid="line-chart">Line Chart</div>
}));

describe('Statistics Component', () => {
  test('renders statistics page with data', async () => {
    render(<Statistics />);
    
    // Check for page title
    expect(screen.getByText(/Statistics/i)).toBeInTheDocument();
    
    // Check for summary stats
    expect(await screen.findByText(/Total Auctions: 25/i)).toBeInTheDocument();
    expect(await screen.findByText(/Active Auctions: 10/i)).toBeInTheDocument();
    expect(await screen.findByText(/Won Auctions: 5/i)).toBeInTheDocument();
    expect(await screen.findByText(/Total Spent: 1500/i)).toBeInTheDocument();
    
    // Check for charts
    expect(screen.getByTestId('bar-chart')).toBeInTheDocument();
    expect(screen.getByTestId('pie-chart')).toBeInTheDocument();
    expect(screen.getByTestId('line-chart')).toBeInTheDocument();
  });
  
  test('displays loading state when data is loading', () => {
    // Override the mock to simulate loading
    jest.mock('../contexts/ApiContext', () => ({
      useApi: () => ({
        isLoading: true,
        auctions: {
          getStats: jest.fn()
        }
      }),
    }), { virtual: true });
    
    render(<Statistics />);
    
    // Check for loading indicator
    expect(screen.getByText(/Loading statistics/i)).toBeInTheDocument();
  });
  
  test('allows changing date range for statistics', async () => {
    render(<Statistics />);
    
    // Wait for stats to load
    await screen.findByText(/Total Auctions: 25/i);
    
    // Find date range selector
    const dateRangeSelector = screen.getByLabelText(/Date Range/i);
    
    // Change date range
    fireEvent.change(dateRangeSelector, { target: { value: 'month' } });
    
    // Check that stats were reloaded (this would trigger a new API call in the real component)
    expect(screen.getByText(/Statistics for the last month/i)).toBeInTheDocument();
  });
});
