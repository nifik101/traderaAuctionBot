import sys
import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from routes.auctions import router as auctions_router
from models import Auction, User

# Create a test client
client = TestClient(app)

# Mock user for testing
@pytest.fixture
def mock_user():
    return User(
        id=1,
        clerk_user_id="user_123",
        email="test@example.com",
        name="Test User"
    )

# Mock dependencies
@pytest.fixture
def mock_get_auctions():
    mock_auctions = [
        {
            "id": 1,
            "tradera_id": "12345",
            "title": "Test Auction",
            "description": "This is a test auction",
            "category_id": 123,
            "seller_id": "seller123",
            "seller_name": "Test Seller",
            "current_price": 150.0,
            "buy_now_price": 300.0,
            "shipping_cost": 50.0,
            "image_urls": ["http://example.com/image1.jpg"],
            "start_time": "2025-04-14T10:00:00Z",
            "end_time": "2025-04-21T10:00:00Z",
            "url": "http://tradera.com/item/12345",
            "bid_count": 3,
            "status": "active",
            "script_id": 1,
            "created_at": "2025-04-14T10:00:00Z",
            "updated_at": "2025-04-14T10:00:00Z"
        },
        {
            "id": 2,
            "tradera_id": "67890",
            "title": "Another Test Auction",
            "description": "This is another test auction",
            "category_id": 456,
            "seller_id": "seller456",
            "seller_name": "Another Seller",
            "current_price": 200.0,
            "buy_now_price": None,
            "shipping_cost": 75.0,
            "image_urls": ["http://example.com/image2.jpg"],
            "start_time": "2025-04-14T11:00:00Z",
            "end_time": "2025-04-21T11:00:00Z",
            "url": "http://tradera.com/item/67890",
            "bid_count": 0,
            "status": "active",
            "script_id": 1,
            "created_at": "2025-04-14T11:00:00Z",
            "updated_at": "2025-04-14T11:00:00Z"
        }
    ]
    
    # Create a mock for the get_auctions function
    async def mock_get_auctions_func(filters=None):
        if filters is None:
            return mock_auctions
        
        if 'id' in filters:
            return [a for a in mock_auctions if a['id'] == filters['id']]
        
        if 'status' in filters:
            if isinstance(filters['status'], list):
                return [a for a in mock_auctions if a['status'] in filters['status']]
            return [a for a in mock_auctions if a['status'] == filters['status']]
        
        return mock_auctions
    
    # Create and apply the patch
    with patch('routes.auctions.get_auctions', side_effect=mock_get_auctions_func):
        yield mock_auctions

# Test health check endpoint
def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "healthy"
    assert "timestamp" in response.json()

# Test root endpoint
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Tradera Assistant API"}
