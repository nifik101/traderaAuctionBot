import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ApiProvider } from '../contexts/ApiContext';
import AuctionListing from '../pages/AuctionListing';

// Mock the API services
jest.mock('../api/services', () => ({
  __esModule: true,
  default: {
    auctions: {
      getAll: jest.fn().mockResolvedValue([
        {
          id: 1,
          tradera_id: '12345',
          title: 'Test Auction',
          description: 'This is a test auction',
          current_price: 150.0,
          buy_now_price: 300.0,
          shipping_cost: 50.0,
          image_urls: ['http://example.com/image1.jpg'],
          start_time: '2025-04-14T10:00:00Z',
          end_time: '2025-04-21T10:00:00Z',
          url: 'http://tradera.com/item/12345',
          bid_count: 3,
          status: 'active'
        },
        {
          id: 2,
          tradera_id: '67890',
          title: 'Another Test Auction',
          description: 'This is another test auction',
          current_price: 200.0,
          buy_now_price: null,
          shipping_cost: 75.0,
          image_urls: ['http://example.com/image2.jpg'],
          start_time: '2025-04-14T11:00:00Z',
          end_time: '2025-04-21T11:00:00Z',
          url: 'http://tradera.com/item/67890',
          bid_count: 0,
          status: 'active'
        }
      ]),
      getById: jest.fn().mockImplementation((id) => {
        const auctions = [
          {
            id: 1,
            tradera_id: '12345',
            title: 'Test Auction',
            description: 'This is a test auction',
            current_price: 150.0,
            buy_now_price: 300.0,
            shipping_cost: 50.0,
            image_urls: ['http://example.com/image1.jpg'],
            start_time: '2025-04-14T10:00:00Z',
            end_time: '2025-04-21T10:00:00Z',
            url: 'http://tradera.com/item/12345',
            bid_count: 3,
            status: 'active'
          },
          {
            id: 2,
            tradera_id: '67890',
            title: 'Another Test Auction',
            description: 'This is another test auction',
            current_price: 200.0,
            buy_now_price: null,
            shipping_cost: 75.0,
            image_urls: ['http://example.com/image2.jpg'],
            start_time: '2025-04-14T11:00:00Z',
            end_time: '2025-04-21T11:00:00Z',
            url: 'http://tradera.com/item/67890',
            bid_count: 0,
            status: 'active'
          }
        ];
        return Promise.resolve(auctions.find(a => a.id === id));
      })
    },
    bidding: {
      getBidConfigs: jest.fn().mockResolvedValue([
        {
          id: 1,
          auction_id: 1,
          max_bid_amount: 200.0,
          bid_seconds_before_end: 5,
          is_active: true,
          status: 'pending'
        }
      ]),
      createBidConfig: jest.fn().mockImplementation((auctionId, bidConfig) => Promise.resolve({
        id: 2,
        auction_id: auctionId,
        ...bidConfig,
        created_at: '2025-04-14T12:00:00Z',
        updated_at: '2025-04-14T12:00:00Z'
      })),
      updateBidConfig: jest.fn().mockImplementation((auctionId, bidConfig) => Promise.resolve({
        id: 1,
        auction_id: auctionId,
        ...bidConfig,
        updated_at: '2025-04-14T12:00:00Z'
      }))
    }
  }
}));

describe('AuctionListing Integration Test', () => {
  test('fetches auctions from API and displays them', async () => {
    render(
      <ApiProvider>
        <AuctionListing />
      </ApiProvider>
    );
    
    // Wait for auctions to load
    await waitFor(() => {
      expect(screen.getByText(/Test Auction/i)).toBeInTheDocument();
      expect(screen.getByText(/Another Test Auction/i)).toBeInTheDocument();
    });
    
    // Verify API service was called
    expect(require('../api/services').default.auctions.getAll).toHaveBeenCalled();
  });
  
  test('creates bid configuration via API when bid button is clicked', async () => {
    render(
      <ApiProvider>
        <AuctionListing />
      </ApiProvider>
    );
    
    // Wait for auctions to load
    await waitFor(() => {
      expect(screen.getByText(/Test Auction/i)).toBeInTheDocument();
    });
    
    // Click the bid button on the second auction (which doesn't have a bid config yet)
    const bidButtons = screen.getAllByText(/Bid/i);
    fireEvent.click(bidButtons[1]);
    
    // Fill out the bid form
    fireEvent.change(screen.getByLabelText(/Maximum Bid Amount/i), {
      target: { value: '250' }
    });
    
    fireEvent.change(screen.getByLabelText(/Seconds Before End/i), {
      target: { value: '3' }
    });
    
    // Submit the form
    fireEvent.click(screen.getByText(/Save Bid Configuration/i));
    
    // Verify API service was called with correct data
    await waitFor(() => {
      expect(require('../api/services').default.bidding.createBidConfig).toHaveBeenCalled();
      const createCall = require('../api/services').default.bidding.createBidConfig.mock.calls[0];
      expect(createCall[0]).toBe(2); // auction_id
      expect(createCall[1].max_bid_amount).toBe(250);
      expect(createCall[1].bid_seconds_before_end).toBe(3);
    });
  });
  
  test('filters auctions based on status selection', async () => {
    render(
      <ApiProvider>
        <AuctionListing />
      </ApiProvider>
    );
    
    // Wait for auctions to load
    await waitFor(() => {
      expect(screen.getByText(/Test Auction/i)).toBeInTheDocument();
    });
    
    // Change the status filter
    fireEvent.change(screen.getByLabelText(/Status/i), {
      target: { value: 'active' }
    });
    
    // Verify API service was called with correct filter
    await waitFor(() => {
      const getAllCalls = require('../api/services').default.auctions.getAll.mock.calls;
      const lastCall = getAllCalls[getAllCalls.length - 1];
      expect(lastCall[0].status).toBe('active');
    });
  });
});
