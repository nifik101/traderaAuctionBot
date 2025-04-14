import { useState, useEffect } from 'react';
import { useApi } from '../contexts/ApiContext';
import '../styles/ScriptManagement.css';

const ScriptManagement = () => {
  const { scripts, isLoading } = useApi();
  const [scriptsList, setScriptsList] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentScript, setCurrentScript] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    schedule: '0 * * * *', // Default: Every hour
    search_parameters: {
      keywords: '',
      categoryId: '',
      regionId: '',
      minPrice: '',
      maxPrice: '',
      sort: 'EndDateAscending',
      buyNowOnly: false,
      showEnded: false
    },
    is_active: true
  });

  useEffect(() => {
    fetchScripts();
  }, []);

  const fetchScripts = async () => {
    try {
      const data = await scripts.getAll();
      setScriptsList(data);
    } catch (error) {
      console.error('Error fetching scripts:', error);
    }
  };

  const handleToggleScript = async (id) => {
    try {
      await scripts.toggle(id);
      fetchScripts();
    } catch (error) {
      console.error('Error toggling script:', error);
    }
  };

  const handleEditScript = (script) => {
    setCurrentScript(script);
    setFormData({
      name: script.name,
      schedule: script.schedule,
      search_parameters: script.search_parameters,
      is_active: script.is_active
    });
    setIsModalOpen(true);
  };

  const handleCreateScript = () => {
    setCurrentScript(null);
    setFormData({
      name: '',
      schedule: '0 * * * *',
      search_parameters: {
        keywords: '',
        categoryId: '',
        regionId: '',
        minPrice: '',
        maxPrice: '',
        sort: 'EndDateAscending',
        buyNowOnly: false,
        showEnded: false
      },
      is_active: true
    });
    setIsModalOpen(true);
  };

  const handleDeleteScript = async (id) => {
    if (window.confirm('Are you sure you want to delete this script?')) {
      try {
        await scripts.delete(id);
        fetchScripts();
      } catch (error) {
        console.error('Error deleting script:', error);
      }
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    if (name.startsWith('search_parameters.')) {
      const paramName = name.split('.')[1];
      setFormData({
        ...formData,
        search_parameters: {
          ...formData.search_parameters,
          [paramName]: type === 'checkbox' ? checked : value
        }
      });
    } else {
      setFormData({
        ...formData,
        [name]: type === 'checkbox' ? checked : value
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      if (currentScript) {
        await scripts.update(currentScript.id, formData);
      } else {
        await scripts.create(formData);
      }
      
      setIsModalOpen(false);
      fetchScripts();
    } catch (error) {
      console.error('Error saving script:', error);
    }
  };

  if (isLoading) {
    return <div className="loading">Loading scripts...</div>;
  }

  return (
    <div className="script-management">
      <div className="page-header">
        <h1>Script Management</h1>
        <button className="create-button" onClick={handleCreateScript}>
          Create New Script
        </button>
      </div>

      {scriptsList.length > 0 ? (
        <table className="scripts-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Keywords</th>
              <th>Schedule</th>
              <th>Status</th>
              <th>Last Run</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {scriptsList.map(script => (
              <tr key={script.id}>
                <td>{script.name}</td>
                <td>{script.search_parameters.keywords || 'None'}</td>
                <td>{script.schedule}</td>
                <td>
                  <span className={`status-badge ${script.is_active ? 'active' : 'inactive'}`}>
                    {script.is_active ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td>{script.last_run_at ? new Date(script.last_run_at).toLocaleString() : 'Never'}</td>
                <td className="actions">
                  <button 
                    className="toggle-button"
                    onClick={() => handleToggleScript(script.id)}
                  >
                    {script.is_active ? 'Disable' : 'Enable'}
                  </button>
                  <button 
                    className="edit-button"
                    onClick={() => handleEditScript(script)}
                  >
                    Edit
                  </button>
                  <button 
                    className="delete-button"
                    onClick={() => handleDeleteScript(script.id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <div className="no-scripts">
          <p>No search scripts found. Create your first script to start monitoring auctions.</p>
        </div>
      )}

      {isModalOpen && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h2>{currentScript ? 'Edit Script' : 'Create New Script'}</h2>
              <button className="close-button" onClick={() => setIsModalOpen(false)}>×</button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="name">Script Name</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="schedule">Schedule (Cron Format)</label>
                <input
                  type="text"
                  id="schedule"
                  name="schedule"
                  value={formData.schedule}
                  onChange={handleInputChange}
                  required
                />
                <div className="help-text">
                  Format: minute hour day month weekday (e.g., "0 * * * *" for every hour)
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="is_active">Status</label>
                <div className="checkbox-group">
                  <input
                    type="checkbox"
                    id="is_active"
                    name="is_active"
                    checked={formData.is_active}
                    onChange={handleInputChange}
                  />
                  <label htmlFor="is_active">Active</label>
                </div>
              </div>

              <h3>Search Parameters</h3>

              <div className="form-group">
                <label htmlFor="keywords">Keywords</label>
                <input
                  type="text"
                  id="keywords"
                  name="search_parameters.keywords"
                  value={formData.search_parameters.keywords}
                  onChange={handleInputChange}
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="categoryId">Category ID</label>
                  <input
                    type="number"
                    id="categoryId"
                    name="search_parameters.categoryId"
                    value={formData.search_parameters.categoryId}
                    onChange={handleInputChange}
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="regionId">Region ID</label>
                  <input
                    type="number"
                    id="regionId"
                    name="search_parameters.regionId"
                    value={formData.search_parameters.regionId}
                    onChange={handleInputChange}
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="minPrice">Min Price (kr)</label>
                  <input
                    type="number"
                    id="minPrice"
                    name="search_parameters.minPrice"
                    value={formData.search_parameters.minPrice}
                    onChange={handleInputChange}
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="maxPrice">Max Price (kr)</label>
                  <input
                    type="number"
                    id="maxPrice"
                    name="search_parameters.maxPrice"
                    value={formData.search_parameters.maxPrice}
                    onChange={handleInputChange}
                  />
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="sort">Sort Order</label>
                <select
                  id="sort"
                  name="search_parameters.sort"
                  value={formData.search_parameters.sort}
                  onChange={handleInputChange}
                >
                  <option value="EndDateAscending">End Date (Ascending)</option>
                  <option value="EndDateDescending">End Date (Descending)</option>
                  <option value="PriceAscending">Price (Ascending)</option>
                  <option value="PriceDescending">Price (Descending)</option>
                  <option value="NewestFirst">Newest First</option>
                </select>
              </div>

              <div className="form-row checkbox-row">
                <div className="form-group">
                  <div className="checkbox-group">
                    <input
                      type="checkbox"
                      id="buyNowOnly"
                      name="search_parameters.buyNowOnly"
                      checked={formData.search_parameters.buyNowOnly}
                      onChange={handleInputChange}
                    />
                    <label htmlFor="buyNowOnly">Buy Now Only</label>
                  </div>
                </div>

                <div className="form-group">
                  <div className="checkbox-group">
                    <input
                      type="checkbox"
                      id="showEnded"
                      name="search_parameters.showEnded"
                      checked={formData.search_parameters.showEnded}
                      onChange={handleInputChange}
                    />
                    <label htmlFor="showEnded">Include Ended Items</label>
                  </div>
                </div>
              </div>

              <div className="form-actions">
                <button type="button" className="cancel-button" onClick={() => setIsModalOpen(false)}>
                  Cancel
                </button>
                <button type="submit" className="save-button">
                  {currentScript ? 'Update Script' : 'Create Script'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default ScriptManagement;
