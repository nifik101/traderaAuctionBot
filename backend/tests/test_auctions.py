import sys
import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routes.auctions import router as auctions_router
from models import Auction, User, get_current_user

# Create a test client
from fastapi import FastAPI, Depends
test_app = FastAPI()
test_app.include_router(auctions_router)
client = TestClient(test_app)

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

# Override the dependency in the test app
@test_app.dependency_overrides[get_current_user]
async def override_get_current_user():
    return User(
        id=1,
        clerk_user_id="user_123",
        email="test@example.com",
        name="Test User"
    )

# Test get_all_auctions endpoint
def test_get_all_auctions(mock_get_auctions):
    response = client.get("/api/auctions/")
    
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["title"] == "Test Auction"
    assert response.json()[1]["title"] == "Another Test Auction"

# Test get_auction by ID endpoint
def test_get_auction_by_id(mock_get_auctions):
    response = client.get("/api/auctions/1")
    
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Test Auction"

# Test get_auction with invalid ID
def test_get_auction_invalid_id(mock_get_auctions):
    response = client.get("/api/auctions/999")
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

# Test get_auction_stats endpoint
def test_get_auction_stats():
    response = client.get("/api/auctions/stats")
    
    assert response.status_code == 200
    assert "total_auctions" in response.json()
    assert "active_auctions" in response.json()
    assert "won_auctions" in response.json()
