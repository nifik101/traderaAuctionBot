import { useState, useEffect } from 'react';
import { useApi } from '../contexts/ApiContext';
import '../styles/Dashboard.css';

const Dashboard = () => {
  const { scripts, auctions, bidding, isLoading } = useApi();
  const [stats, setStats] = useState({
    totalAuctions: 0,
    activeAuctions: 0,
    pendingBids: 0,
    wonAuctions: 0,
    totalSpent: 0
  });
  const [recentAuctions, setRecentAuctions] = useState([]);
  const [activeScripts, setActiveScripts] = useState([]);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // Fetch auctions
        const auctionsData = await auctions.getAll();
        setRecentAuctions(auctionsData.slice(0, 5)); // Get 5 most recent auctions
        
        // Fetch scripts
        const scriptsData = await scripts.getAll();
        setActiveScripts(scriptsData.filter(script => script.is_active));
        
        // Fetch bid configs
        const bidConfigsData = await bidding.getBidConfigs();
        
        // Calculate stats
        const activeAuctions = auctionsData.filter(auction => auction.status === 'active').length;
        const wonAuctions = auctionsData.filter(auction => auction.status === 'won').length;
        const pendingBids = bidConfigsData.filter(config => config.status === 'pending').length;
        const totalSpent = auctionsData
          .filter(auction => auction.status === 'won')
          .reduce((sum, auction) => sum + auction.current_price, 0);
        
        setStats({
          totalAuctions: auctionsData.length,
          activeAuctions,
          pendingBids,
          wonAuctions,
          totalSpent
        });
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      }
    };
    
    fetchDashboardData();
  }, []);

  if (isLoading) {
    return <div className="loading">Loading dashboard data...</div>;
  }

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      
      <div className="stats-cards">
        <div className="stat-card">
          <h3>Total Auctions</h3>
          <div className="stat-value">{stats.totalAuctions}</div>
        </div>
        <div className="stat-card">
          <h3>Active Auctions</h3>
          <div className="stat-value">{stats.activeAuctions}</div>
        </div>
        <div className="stat-card">
          <h3>Pending Bids</h3>
          <div className="stat-value">{stats.pendingBids}</div>
        </div>
        <div className="stat-card">
          <h3>Won Auctions</h3>
          <div className="stat-value">{stats.wonAuctions}</div>
        </div>
        <div className="stat-card">
          <h3>Total Spent</h3>
          <div className="stat-value">{stats.totalSpent.toFixed(2)} kr</div>
        </div>
      </div>
      
      <div className="dashboard-sections">
        <div className="dashboard-section">
          <h2>Recent Auctions</h2>
          {recentAuctions.length > 0 ? (
            <table className="auctions-table">
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Current Price</th>
                  <th>End Time</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {recentAuctions.map(auction => (
                  <tr key={auction.id}>
                    <td>{auction.title}</td>
                    <td>{auction.current_price} kr</td>
                    <td>{new Date(auction.end_time).toLocaleString()}</td>
                    <td>{auction.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>No auctions found.</p>
          )}
        </div>
        
        <div className="dashboard-section">
          <h2>Active Scripts</h2>
          {activeScripts.length > 0 ? (
            <table className="scripts-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Schedule</th>
                  <th>Last Run</th>
                </tr>
              </thead>
              <tbody>
                {activeScripts.map(script => (
                  <tr key={script.id}>
                    <td>{script.name}</td>
                    <td>{script.schedule}</td>
                    <td>{script.last_run_at ? new Date(script.last_run_at).toLocaleString() : 'Never'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>No active scripts found.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
