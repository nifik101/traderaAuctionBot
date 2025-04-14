import React from 'react';
import { useEffect, useState } from 'react';
import { useApi } from '../contexts/ApiContext';

const AuctionListing = () => {
  const [auctions, setAuctions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { auctionsApi } = useApi();

  useEffect(() => {
    const fetchAuctions = async () => {
      try {
        setLoading(true);
        const response = await auctionsApi.getAuctions();
        setAuctions(response.data || []);
        setError(null);
      } catch (err) {
        console.error('Error fetching auctions:', err);
        setError('Failed to load auctions. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchAuctions();
  }, [auctionsApi]);

  const handleBidConfig = (auctionId) => {
    // This would open a modal or navigate to bid configuration
    console.log(`Configure bid for auction ${auctionId}`);
  };

  if (loading) {
    return <div className="loading">Loading auctions...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="auction-listing">
      <h1>Monitored Auctions</h1>
      
      {auctions.length === 0 ? (
        <div className="no-auctions">
          <p>No auctions found. Create a search script to start monitoring auctions.</p>
        </div>
      ) : (
        <div className="auctions-grid">
          {auctions.map((auction) => (
            <div key={auction.id} className="auction-card">
              <div className="auction-image">
                {auction.image_url ? (
                  <img src={auction.image_url} alt={auction.title} />
                ) : (
                  <div className="no-image">No Image</div>
                )}
              </div>
              <div className="auction-details">
                <h3>{auction.title}</h3>
                <p className="auction-price">Current Price: {auction.current_price} SEK</p>
                <p className="auction-end-time">
                  Ends: {new Date(auction.end_time).toLocaleString()}
                </p>
                <p className="auction-bids">Bids: {auction.bid_count}</p>
                <button 
                  className="bid-config-button"
                  onClick={() => handleBidConfig(auction.id)}
                >
                  Configure Bid
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AuctionListing;
