import { useState } from 'react';
import { useApi } from '../contexts/ApiContext';
import '../styles/Sidebar.css';

const Sidebar = () => {
  const [isExpanded, setIsExpanded] = useState(true);
  const { auctions, scripts } = useApi();
  const [stats, setStats] = useState({
    activeScripts: 0,
    pendingBids: 0,
    endingSoon: 0
  });

  // Fetch stats on component mount
  useState(() => {
    const fetchStats = async () => {
      try {
        const scriptData = await scripts.getAll();
        const activeScripts = scriptData.filter(script => script.is_active).length;
        
        const auctionData = await auctions.getAll({ status: 'active' });
        const endingSoon = auctionData.filter(auction => {
          const endTime = new Date(auction.end_time);
          const now = new Date();
          const hoursDiff = (endTime - now) / (1000 * 60 * 60);
          return hoursDiff <= 24;
        }).length;
        
        setStats({
          activeScripts,
          pendingBids: 0, // This would come from a real API call
          endingSoon
        });
      } catch (error) {
        console.error('Error fetching sidebar stats:', error);
      }
    };
    
    fetchStats();
  }, []);

  return (
    <aside className={`sidebar ${isExpanded ? 'expanded' : 'collapsed'}`}>
      <div className="sidebar-toggle" onClick={() => setIsExpanded(!isExpanded)}>
        {isExpanded ? '«' : '»'}
      </div>
      
      {isExpanded && (
        <div className="sidebar-content">
          <div className="sidebar-section">
            <h3>Status</h3>
            <div className="status-item">
              <span className="status-label">Active Scripts:</span>
              <span className="status-value">{stats.activeScripts}</span>
            </div>
            <div className="status-item">
              <span className="status-label">Pending Bids:</span>
              <span className="status-value">{stats.pendingBids}</span>
            </div>
            <div className="status-item">
              <span className="status-label">Ending Soon:</span>
              <span className="status-value">{stats.endingSoon}</span>
            </div>
          </div>
          
          <div className="sidebar-section">
            <h3>Quick Actions</h3>
            <button className="action-button">Run All Scripts</button>
            <button className="action-button">Refresh Auctions</button>
          </div>
          
          <div className="sidebar-section">
            <h3>Filters</h3>
            <div className="filter-group">
              <label>
                <input type="checkbox" /> Show Active Only
              </label>
            </div>
            <div className="filter-group">
              <label>
                <input type="checkbox" /> Ending Today
              </label>
            </div>
            <div className="filter-group">
              <label>
                <input type="checkbox" /> With Bids
              </label>
            </div>
          </div>
        </div>
      )}
    </aside>
  );
};

export default Sidebar;
