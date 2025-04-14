import unittest
import os
import sys
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from routes.bidding import tradera_api

class TestBiddingRoutes(unittest.TestCase):
    """Test cases for bidding routes with Tradera API integration"""
    
    def setUp(self):
        """Set up test environment"""
        self.client = TestClient(app)
        
        # Sample bid result
        self.sample_bid_result = {
            "status": "Bought",
            "next_bid": 600,
            "success": True
        }
        
        # Mock Supabase client
        self.mock_supabase_patcher = patch('routes.bidding.get_supabase_client')
        self.mock_supabase = self.mock_supabase_patcher.start()
        
        # Mock Supabase table operations
        self.mock_table = MagicMock()
        self.mock_select = MagicMock()
        self.mock_insert = MagicMock()
        self.mock_update = MagicMock()
        self.mock_delete = MagicMock()
        self.mock_eq = MagicMock()
        self.mock_execute = MagicMock()
        
        self.mock_table.select.return_value = self.mock_select
        self.mock_select.eq.return_value = self.mock_eq
        self.mock_eq.execute.return_value = self.mock_execute
        self.mock_table.insert.return_value = self.mock_insert
        self.mock_insert.execute.return_value = self.mock_execute
        self.mock_table.update.return_value = self.mock_update
        self.mock_update.eq.return_value = self.mock_eq
        self.mock_table.delete.return_value = self.mock_delete
        self.mock_delete.eq.return_value = self.mock_eq
        
        self.mock_supabase.return_value.table.return_value = self.mock_table
        
        # Mock TraderaAPI
        self.mock_tradera_api_patcher = patch('routes.bidding.tradera_api')
        self.mock_tradera_api = self.mock_tradera_api_patcher.start()
    
    def tearDown(self):
        """Clean up after tests"""
        self.mock_supabase_patcher.stop()
        self.mock_tradera_api_patcher.stop()
    
    def test_get_bid_configs(self):
        """Test get_bid_configs endpoint"""
        # Configure mock
        self.mock_execute.data = [
            {
                "id": 1,
                "auction_id": 123,
                "max_bid_amount": 1000,
                "bid_seconds_before_end": 10,
                "is_active": True,
                "status": "pending",
                "created_at": "2025-04-14T10:00:00Z",
                "updated_at": "2025-04-14T10:00:00Z"
            },
            {
                "id": 2,
                "auction_id": 456,
                "max_bid_amount": 2000,
                "bid_seconds_before_end": 5,
                "is_active": True,
                "status": "pending",
                "created_at": "2025-04-14T11:00:00Z",
                "updated_at": "2025-04-14T11:00:00Z"
            }
        ]
        
        # Make request
        response = self.client.get("/api/bid-configs")
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["auction_id"], 123)
        self.assertEqual(data[1]["auction_id"], 456)
        
        # Verify Supabase was called
        self.mock_table.select.assert_called_once_with("*")
    
    def test_create_bid_config(self):
        """Test create_bid_config endpoint"""
        # Configure mock for auction check
        auction_response = MagicMock()
        auction_response.data = [{"id": 123, "tradera_id": "456789", "title": "Test Auction"}]
        
        # Configure mock for existing bid config check
        existing_response = MagicMock()
        existing_response.data = []
        
        # Configure mock for insert
        insert_response = MagicMock()
        insert_response.data = [{
            "id": 1,
            "auction_id": 123,
            "max_bid_amount": 1000,
            "bid_seconds_before_end": 10,
            "is_active": True,
            "status": "pending",
            "created_at": "2025-04-14T10:00:00Z",
            "updated_at": "2025-04-14T10:00:00Z"
        }]
        
        # Set up mock returns for different queries
        self.mock_eq.execute.side_effect = [
            auction_response,    # First call for auction check
            existing_response,   # Second call for existing config check
            insert_response      # Third call for insert result
        ]
        
        # Make request
        response = self.client.post(
            "/api/auctions/123/bid-config",
            json={
                "max_bid_amount": 1000,
                "bid_seconds_before_end": 10,
                "is_active": True
            }
        )
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["auction_id"], 123)
        self.assertEqual(data["max_bid_amount"], 1000)
        self.assertEqual(data["bid_seconds_before_end"], 10)
        self.assertTrue(data["is_active"])
        
        # Verify Supabase was called correctly
        self.assertEqual(self.mock_table.select.call_count, 2)
        self.assertEqual(self.mock_table.insert.call_count, 1)
    
    def test_create_bid_config_auction_not_found(self):
        """Test create_bid_config endpoint with non-existent auction"""
        # Configure mock for auction check
        auction_response = MagicMock()
        auction_response.data = []
        
        # Set up mock returns
        self.mock_eq.execute.return_value = auction_response
        
        # Make request
        response = self.client.post(
            "/api/auctions/999/bid-config",
            json={
                "max_bid_amount": 1000,
                "bid_seconds_before_end": 10,
                "is_active": True
            }
        )
        
        # Check response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Auction not found")
    
    def test_create_bid_config_already_exists(self):
        """Test create_bid_config endpoint with existing config"""
        # Configure mock for auction check
        auction_response = MagicMock()
        auction_response.data = [{"id": 123, "tradera_id": "456789", "title": "Test Auction"}]
        
        # Configure mock for existing bid config check
        existing_response = MagicMock()
        existing_response.data = [{
            "id": 1,
            "auction_id": 123,
            "max_bid_amount": 1000,
            "bid_seconds_before_end": 10,
            "is_active": True
        }]
        
        # Set up mock returns for different queries
        self.mock_eq.execute.side_effect = [
            auction_response,    # First call for auction check
            existing_response    # Second call for existing config check
        ]
        
        # Make request
        response = self.client.post(
            "/api/auctions/123/bid-config",
            json={
                "max_bid_amount": 1000,
                "bid_seconds_before_end": 10,
                "is_active": True
            }
        )
        
        # Check response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Bid configuration already exists for this auction")
    
    def test_update_bid_config(self):
        """Test update_bid_config endpoint"""
        # Configure mock for existing bid config check
        existing_response = MagicMock()
        existing_response.data = [{
            "id": 1,
            "auction_id": 123,
            "max_bid_amount": 1000,
            "bid_seconds_before_end": 10,
            "is_active": True
        }]
        
        # Configure mock for update
        update_response = MagicMock()
        update_response.data = [{
            "id": 1,
            "auction_id": 123,
            "max_bid_amount": 1500,
            "bid_seconds_before_end": 5,
            "is_active": True,
            "updated_at": "2025-04-14T11:00:00Z"
        }]
        
        # Set up mock returns for different queries
        self.mock_eq.execute.side_effect = [
            existing_response,   # First call for existing config check
            update_response      # Second call for update result
        ]
        
        # Make request
        response = self.client.put(
            "/api/auctions/123/bid-config",
            json={
                "max_bid_amount": 1500,
                "bid_seconds_before_end": 5,
                "is_active": True
            }
        )
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["auction_id"], 123)
        self.assertEqual(data["max_bid_amount"], 1500)
        self.assertEqual(data["bid_seconds_before_end"], 5)
        self.assertTrue(data["is_active"])
        
        # Verify Supabase was called correctly
        self.assertEqual(self.mock_table.select.call_count, 1)
        self.assertEqual(self.mock_table.update.call_count, 1)
    
    def test_update_bid_config_not_found(self):
        """Test update_bid_config endpoint with non-existent config"""
        # Configure mock for existing bid config check
        existing_response = MagicMock()
        existing_response.data = []
        
        # Set up mock returns
        self.mock_eq.execute.return_value = existing_response
        
        # Make request
        response = self.client.put(
            "/api/auctions/999/bid-config",
            json={
                "max_bid_amount": 1500,
                "bid_seconds_before_end": 5,
                "is_active": True
            }
        )
        
        # Check response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Bid configuration not found")
    
    def test_delete_bid_config(self):
        """Test delete_bid_config endpoint"""
        # Configure mock for existing bid config check
        existing_response = MagicMock()
        existing_response.data = [{
            "id": 1,
            "auction_id": 123,
            "max_bid_amount": 1000,
            "bid_seconds_before_end": 10,
            "is_active": True
        }]
        
        # Configure mock for delete
        delete_response = MagicMock()
        delete_response.data = []
        
        # Set up mock returns for different queries
        self.mock_eq.execute.side_effect = [
            existing_response,   # First call for existing config check
            delete_response      # Second call for delete result
        ]
        
        # Make request
        response = self.client.delete("/api/auctions/123/bid-config")
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Bid configuration deleted successfully")
        
        # Verify Supabase was called correctly
        self.assertEqual(self.mock_table.select.call_count, 1)
        self.assertEqual(self.mock_table.delete.call_count, 1)
    
    def test_delete_bid_config_not_found(self):
        """Test delete_bid_config endpoint with non-existent config"""
        # Configure mock for existing bid config check
        existing_response = MagicMock()
        existing_response.data = []
        
        # Set up mock returns
        self.mock_eq.execute.return_value = existing_response
        
        # Make request
        response = self.client.delete("/api/auctions/999/bid-config")
        
        # Check response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Bid configuration not found")
    
    def test_place_bid(self):
        """Test place_bid endpoint"""
        # Configure mock for auction check
        auction_response = MagicMock()
        auction_response.data = [{
            "id": 123,
            "tradera_id": "456789",
            "title": "Test Auction",
            "bid_count": 2
        }]
        
        # Configure mock for bid insert
        bid_response = MagicMock()
        bid_response.data = [{
            "id": 1,
            "auction_id": 123,
            "amount": 1000,
            "status": "won",
            "created_at": "2025-04-14T10:00:00Z",
            "tradera_response": str(self.sample_bid_result)
        }]
        
        # Set up mock returns for different queries
        self.mock_eq.execute.side_effect = [
            auction_response,    # First call for auction check
            bid_response         # Second call for bid insert
        ]
        
        # Configure TraderaAPI mock
        self.mock_tradera_api.place_bid.return_value = self.sample_bid_result
        
        # Make request
        response = self.client.post(
            "/api/auctions/123/bid",
            json={
                "auction_id": 123,
                "amount": 1000,
                "user_id": 12345,
                "token": "test_token"
            }
        )
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["auction_id"], 123)
        self.assertEqual(data["amount"], 1000)
        self.assertEqual(data["status"], "won")
        self.assertEqual(data["tradera_status"], "Bought")
        self.assertEqual(data["next_bid"], 600)
        
        # Verify TraderaAPI was called with correct parameters
        self.mock_tradera_api.set_user_token.assert_called_once_with(12345, "test_token")
        self.mock_tradera_api.place_bid.assert_called_once_with(
            item_id=int("456789"),
            bid_amount=1000
        )
        
        # Verify Supabase was called correctly
        self.assertEqual(self.mock_table.select.call_count, 1)
        self.assertEqual(self.mock_table.insert.call_count, 1)
        self.assertEqual(self.mock_table.update.call_count, 1)
    
    def test_place_bid_auction_not_found(self):
        """Test place_bid endpoint with non-existent auction"""
        # Configure mock for auction check
        auction_response = MagicMock()
        auction_response.data = []
        
        # Set up mock returns
        self.mock_eq.execute.return_value = auction_response
        
        # Make request
        response = self.client.post(
            "/api/auctions/999/bid",
            json={
                "auction_id": 999,
                "amount": 1000
            }
        )
        
        # Check response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Auction not found")
    
    def test_place_bid_api_error(self):
        """Test place_bid endpoint with API error"""
        # Configure mock for auction check
        auction_response = MagicMock()
        auction_response.data = [{
            "id": 123,
            "tradera_id": "456789",
            "title": "Test Auction"
        }]
        
        # Set up mock returns
        self.mock_eq.execute.return_value = auction_response
        
        # Configure TraderaAPI mock
        self.mock_tradera_api.place_bid.return_value = {"error": "API error"}
        
        # Make request
        response = self.client.post(
            "/api/auctions/123/bid",
            json={
                "auction_id": 123,
                "amount": 1000
            }
        )
        
        # Check response
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()["detail"], "API error")
    
    def test_get_bids(self):
        """Test get_bids endpoint"""
        # Configure mock
        self.mock_execute.data = [
            {
                "id": 1,
                "auction_id": 123,
                "amount": 1000,
                "status": "won",
                "created_at": "2025-04-14T10:00:00Z"
            },
            {
                "id": 2,
                "auction_id": 456,
                "amount": 2000,
                "status": "failed",
                "created_at": "2025-04-14T11:00:00Z"
            }
        ]
        
        # Make request
        response = self.client.get("/api/bids")
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["auction_id"], 123)
        self.assertEqual(data[1]["auction_id"], 456)
        
        # Verify Supabase was called
        self.mock_table.select.assert_called_once_with("*")

if __name__ == '__main__':
    unittest.main()
