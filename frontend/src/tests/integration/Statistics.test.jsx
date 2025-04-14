import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { ApiProvider } from '../contexts/ApiContext';
import Statistics from '../pages/Statistics';

// Mock the chart components
jest.mock('react-chartjs-2', () => ({
  Bar: () => <div data-testid="bar-chart">Bar Chart</div>,
  Pie: () => <div data-testid="pie-chart">Pie Chart</div>,
  Line: () => <div data-testid="line-chart">Line Chart</div>
}));

// Mock the API services
jest.mock('../api/services', () => ({
  __esModule: true,
  default: {
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
  }
}));

describe('Statistics Integration Test', () => {
  test('fetches statistics from API and displays them', async () => {
    render(
      <ApiProvider>
        <Statistics />
      </ApiProvider>
    );
    
    // Wait for statistics to load
    await waitFor(() => {
      expect(screen.getByText(/Total Auctions: 25/i)).toBeInTheDocument();
    });
    
    // Check that stats are displayed
    expect(screen.getByText(/Active Auctions: 10/i)).toBeInTheDocument();
    expect(screen.getByText(/Won Auctions: 5/i)).toBeInTheDocument();
    expect(screen.getByText(/Total Spent: 1500/i)).toBeInTheDocument();
    
    // Check that charts are rendered
    expect(screen.getByTestId('bar-chart')).toBeInTheDocument();
    expect(screen.getByTestId('pie-chart')).toBeInTheDocument();
    expect(screen.getByTestId('line-chart')).toBeInTheDocument();
    
    // Verify API service was called
    expect(require('../api/services').default.auctions.getStats).toHaveBeenCalled();
  });
  
  test('displays loading state while fetching data', () => {
    // Override the mock to delay resolution
    jest.mock('../api/services', () => ({
      __esModule: true,
      default: {
        auctions: {
          getStats: jest.fn().mockImplementation(() => new Promise(resolve => {
            setTimeout(() => {
              resolve({
                total_auctions: 25,
                active_auctions: 10,
                ended_auctions: 15,
                won_auctions: 5,
                lost_auctions: 10,
                total_spent: 1500
              });
            }, 1000);
          }))
        }
      }
    }), { virtual: true });
    
    render(
      <ApiProvider>
        <Statistics />
      </ApiProvider>
    );
    
    // Check for loading indicator
    expect(screen.getByText(/Loading statistics/i)).toBeInTheDocument();
  });
});
