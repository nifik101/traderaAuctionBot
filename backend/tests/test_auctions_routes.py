import unittest
import os
import sys
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from routes.auctions import tradera_api

class TestAuctionsRoutes(unittest.TestCase):
    """Test cases for auctions routes with Tradera API integration"""
    
    def setUp(self):
        """Set up test environment"""
        self.client = TestClient(app)
        
        # Sample search results
        self.sample_search_results = {
            "total_items": 2,
            "total_pages": 1,
            "items": [
                {
                    "id": 123456,
                    "tradera_id": "123456",
                    "title": "Test Item 1",
                    "description": "This is a test item description",
                    "current_price": 500,
                    "buy_now_price": 1000,
                    "seller_id": 9876,
                    "seller_alias": "TestSeller",
                    "end_date": "2025-05-01T12:00:00+00:00",
                    "next_bid": 550,
                    "has_bids": True,
                    "is_ended": False,
                    "item_type": "Auction",
                    "url": "http://tradera.com/item/123456",
                    "category_id": 100,
                    "bid_count": 3,
                    "thumbnail_url": "http://example.com/thumb1.jpg",
                    "image_urls": ["http://example.com/image1.jpg"],
                    "status": "active"
                },
                {
                    "id": 789012,
                    "tradera_id": "789012",
                    "title": "Test Item 2",
                    "description": "This is another test item description",
                    "current_price": 1200,
                    "buy_now_price": 2000,
                    "seller_id": 9876,
                    "seller_alias": "TestSeller",
                    "end_date": "2025-05-02T12:00:00+00:00",
                    "next_bid": 1250,
                    "has_bids": True,
                    "is_ended": False,
                    "item_type": "Auction",
                    "url": "http://tradera.com/item/789012",
                    "category_id": 100,
                    "bid_count": 5,
                    "thumbnail_url": "http://example.com/thumb2.jpg",
                    "image_urls": ["http://example.com/image2.jpg"],
                    "status": "active"
                }
            ],
            "errors": []
        }
        
        # Mock Supabase client
        self.mock_supabase_patcher = patch('routes.auctions.get_supabase_client')
        self.mock_supabase = self.mock_supabase_patcher.start()
        
        # Mock Supabase table operations
        self.mock_table = MagicMock()
        self.mock_select = MagicMock()
        self.mock_insert = MagicMock()
        self.mock_update = MagicMock()
        self.mock_eq = MagicMock()
        self.mock_execute = MagicMock()
        
        self.mock_table.select.return_value = self.mock_select
        self.mock_select.eq.return_value = self.mock_eq
        self.mock_eq.execute.return_value = self.mock_execute
        self.mock_table.insert.return_value = self.mock_insert
        self.mock_insert.execute.return_value = self.mock_execute
        self.mock_table.update.return_value = self.mock_update
        self.mock_update.eq.return_value = self.mock_eq
        
        self.mock_supabase.return_value.table.return_value = self.mock_table
        
        # Mock TraderaAPI
        self.mock_tradera_api_patcher = patch('routes.auctions.tradera_api')
        self.mock_tradera_api = self.mock_tradera_api_patcher.start()
    
    def tearDown(self):
        """Clean up after tests"""
        self.mock_supabase_patcher.stop()
        self.mock_tradera_api_patcher.stop()
    
    def test_search_auctions(self):
        """Test search_auctions endpoint"""
        # Configure mock
        self.mock_tradera_api.search_advanced.return_value = self.sample_search_results
        self.mock_execute.data = []  # No existing auctions
        
        # Make request
        response = self.client.post(
            "/api/auctions/search",
            json={
                "search_words": "test",
                "category_id": 100,
                "price_minimum": 100,
                "price_maximum": 2000,
                "page_number": 1,
                "items_per_page": 25
            }
        )
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_items"], 2)
        self.assertEqual(data["total_pages"], 1)
        self.assertEqual(len(data["items"]), 2)
        
        # Verify TraderaAPI was called with correct parameters
        self.mock_tradera_api.search_advanced.assert_called_once_with(
            search_words="test",
            category_id=100,
            price_minimum=100,
            price_maximum=2000,
            item_type=None,
            item_status=None,
            items_per_page=25,
            page_number=1,
            order_by="EndDateAscending"
        )
        
        # Verify items were stored in database
        self.assertEqual(self.mock_table.insert.call_count, 2)
    
    def test_search_auctions_with_error(self):
        """Test search_auctions endpoint with API error"""
        # Configure mock
        self.mock_tradera_api.search_advanced.return_value = {"error": "API error"}
        
        # Make request
        response = self.client.post(
            "/api/auctions/search",
            json={
                "search_words": "test",
                "category_id": 100
            }
        )
        
        # Check response
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()["detail"], "API error")
    
    def test_get_auctions(self):
        """Test get_auctions endpoint"""
        # Configure mock
        self.mock_execute.data = [
            {
                "id": 1,
                "tradera_id": "123456",
                "title": "Test Item 1",
                "current_price": 500,
                "end_time": "2025-05-01T12:00:00+00:00",
                "status": "active"
            },
            {
                "id": 2,
                "tradera_id": "789012",
                "title": "Test Item 2",
                "current_price": 1200,
                "end_time": "2025-05-02T12:00:00+00:00",
                "status": "active"
            }
        ]
        
        # Make request
        response = self.client.get("/api/auctions/")
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["title"], "Test Item 1")
        self.assertEqual(data[1]["title"], "Test Item 2")
        
        # Verify Supabase was called
        self.mock_table.select.assert_called_once_with("*")
    
    def test_get_auctions_with_status_filter(self):
        """Test get_auctions endpoint with status filter"""
        # Configure mock
        self.mock_execute.data = [
            {
                "id": 1,
                "tradera_id": "123456",
                "title": "Test Item 1",
                "current_price": 500,
                "end_time": "2025-05-01T12:00:00+00:00",
                "status": "active"
            }
        ]
        
        # Make request
        response = self.client.get("/api/auctions/?status=active")
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Test Item 1")
        
        # Verify Supabase was called with filter
        self.mock_select.eq.assert_called_once_with("status", "active")
    
    def test_get_auction_by_id(self):
        """Test get_auction endpoint"""
        # Configure mock
        self.mock_execute.data = [
            {
                "id": 1,
                "tradera_id": "123456",
                "title": "Test Item 1",
                "current_price": 500,
                "end_time": "2025-05-01T12:00:00+00:00",
                "status": "active"
            }
        ]
        
        # Make request
        response = self.client.get("/api/auctions/1")
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["title"], "Test Item 1")
        
        # Verify Supabase was called with correct ID
        self.mock_select.eq.assert_called_once_with("id", 1)
    
    def test_get_auction_not_found(self):
        """Test get_auction endpoint with non-existent ID"""
        # Configure mock
        self.mock_execute.data = []
        
        # Make request
        response = self.client.get("/api/auctions/999")
        
        # Check response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Auction not found")
    
    def test_get_auction_stats(self):
        """Test get_auction_stats endpoint"""
        # Configure mocks for different queries
        total_response = MagicMock()
        total_response.count = 10
        
        active_response = MagicMock()
        active_response.count = 5
        
        won_response = MagicMock()
        won_response.count = 3
        
        spent_response = MagicMock()
        spent_response.data = [{"amount": 100}, {"amount": 200}, {"amount": 300}]
        
        categories_response = MagicMock()
        categories_response.data = [
            {"category_id": "100"},
            {"category_id": "100"},
            {"category_id": "200"}
        ]
        
        end_times_response = MagicMock()
        end_times_response.data = [
            {"end_time": "2025-05-01T12:00:00Z"},
            {"end_time": "2025-05-01T13:00:00Z"},
            {"end_time": "2025-05-02T12:00:00Z"}
        ]
        
        # Set up mock returns for different queries
        self.mock_select.count = "exact"  # For count queries
        
        # Need to handle different query chains
        self.mock_supabase.return_value.table.side_effect = lambda table_name: {
            "auctions": self.mock_table,
            "bids": MagicMock(select=lambda *args, **kwargs: MagicMock(
                eq=lambda *args, **kwargs: MagicMock(execute=lambda: spent_response)
            ))
        }.get(table_name, self.mock_table)
        
        # Set up different responses for different queries
        self.mock_eq.execute.side_effect = [
            total_response,  # First call for total count
            active_response,  # Second call for active count
            won_response,    # Third call for won count
            categories_response,  # Fourth call for categories
            end_times_response    # Fifth call for end times
        ]
        
        # Make request
        response = self.client.get("/api/auctions/stats")
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_auctions"], 10)
        self.assertEqual(data["active_auctions"], 5)
        self.assertEqual(data["won_auctions"], 3)
        self.assertEqual(data["total_spent"], 600)  # Sum of amounts
        self.assertEqual(len(data["categories"]), 2)  # Unique categories
        self.assertEqual(len(data["end_time_distribution"]), 2)  # Unique dates

if __name__ == '__main__':
    unittest.main()
