import React from 'react';
import { useEffect, useState } from 'react';
import { useApi } from '../contexts/ApiContext';

const Statistics = () => {
  const [stats, setStats] = useState({
    totalAuctions: 0,
    totalBids: 0,
    successfulBids: 0,
    averageSavings: 0,
    activeScripts: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { statisticsApi } = useApi();

  useEffect(() => {
    const fetchStatistics = async () => {
      try {
        setLoading(true);
        // In a real implementation, this would call the API
        // const response = await statisticsApi.getStatistics();
        // setStats(response.data || defaultStats);
        
        // Mock data for now
        setTimeout(() => {
          setStats({
            totalAuctions: 157,
            totalBids: 42,
            successfulBids: 28,
            averageSavings: 15.3,
            activeScripts: 12
          });
          setLoading(false);
        }, 1000);
        
        setError(null);
      } catch (err) {
        console.error('Error fetching statistics:', err);
        setError('Failed to load statistics. Please try again later.');
        setLoading(false);
      }
    };

    fetchStatistics();
  }, []);

  if (loading) {
    return <div className="loading">Loading statistics...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="statistics-page">
      <h1>Bidding Statistics</h1>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Auctions Monitored</h3>
          <div className="stat-value">{stats.totalAuctions}</div>
        </div>
        
        <div className="stat-card">
          <h3>Total Bids Placed</h3>
          <div className="stat-value">{stats.totalBids}</div>
        </div>
        
        <div className="stat-card">
          <h3>Successful Bids</h3>
          <div className="stat-value">{stats.successfulBids}</div>
          <div className="stat-percentage">
            {stats.totalBids > 0 ? 
              `${Math.round((stats.successfulBids / stats.totalBids) * 100)}%` : 
              '0%'}
          </div>
        </div>
        
        <div className="stat-card">
          <h3>Average Savings</h3>
          <div className="stat-value">{stats.averageSavings}%</div>
          <div className="stat-description">compared to similar items</div>
        </div>
        
        <div className="stat-card">
          <h3>Active Search Scripts</h3>
          <div className="stat-value">{stats.activeScripts}</div>
        </div>
      </div>
      
      <div className="stats-charts">
        <h2>Bidding History</h2>
        <div className="chart-placeholder">
          <p>Charts will be displayed here in the production version</p>
        </div>
      </div>
    </div>
  );
};

export default Statistics;
