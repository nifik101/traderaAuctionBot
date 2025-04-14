import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import AuctionListing from '../pages/AuctionListing';

// Mock the API context
jest.mock('../contexts/ApiContext', () => ({
  useApi: () => ({
    isLoading: false,
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
      createBidConfig: jest.fn().mockResolvedValue({
        id: 2,
        auction_id: 2,
        max_bid_amount: 250.0,
        bid_seconds_before_end: 3,
        is_active: true,
        status: 'pending'
      }),
      updateBidConfig: jest.fn().mockResolvedValue({})
    }
  }),
}));

describe('AuctionListing Component', () => {
  test('renders auction listing page with auctions', async () => {
    render(<AuctionListing />);
    
    // Check for page title
    expect(screen.getByText(/Auctions/i)).toBeInTheDocument();
    
    // Check for filter controls
    expect(screen.getByText(/Filter/i)).toBeInTheDocument();
    
    // Check for auction data
    expect(await screen.findByText(/Test Auction/i)).toBeInTheDocument();
    expect(await screen.findByText(/Another Test Auction/i)).toBeInTheDocument();
    expect(await screen.findByText(/150.0 kr/i)).toBeInTheDocument();
    expect(await screen.findByText(/200.0 kr/i)).toBeInTheDocument();
    
    // Check for action buttons
    expect(screen.getAllByText(/View/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/Bid/i).length).toBeGreaterThan(0);
  });
  
  test('displays empty state when no auctions', () => {
    // Override the mock to return empty array
    jest.mock('../contexts/ApiContext', () => ({
      useApi: () => ({
        isLoading: false,
        auctions: {
          getAll: jest.fn().mockResolvedValue([]),
          getById: jest.fn()
        },
        bidding: {
          getBidConfigs: jest.fn().mockResolvedValue([]),
          createBidConfig: jest.fn(),
          updateBidConfig: jest.fn()
        }
      }),
    }), { virtual: true });
    
    render(<AuctionListing />);
    
    // Check for empty state message
    expect(screen.getByText(/No auctions found/i)).toBeInTheDocument();
  });
  
  test('opens bid modal when bid button is clicked', async () => {
    render(<AuctionListing />);
    
    // Wait for auctions to load
    await screen.findByText(/Test Auction/i);
    
    // Click bid button on first auction
    const bidButtons = screen.getAllByText(/Bid/i);
    fireEvent.click(bidButtons[0]);
    
    // Check if bid modal is open
    expect(screen.getByText(/Configure Bid/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Maximum Bid Amount/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Seconds Before End/i)).toBeInTheDocument();
  });
});
