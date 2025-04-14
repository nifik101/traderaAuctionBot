import sys
import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routes.bidding import router as bidding_router
from models import BidConfig, User, get_current_user

# Create a test client
from fastapi import FastAPI
test_app = FastAPI()
test_app.include_router(bidding_router)
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
def mock_bid_configs(monkeypatch):
    mock_configs = [
        {
            "id": 1,
            "auction_id": 1,
            "user_id": 1,
            "max_bid_amount": 200.0,
            "bid_seconds_before_end": 5,
            "is_active": True,
            "status": "pending",
            "error_message": None,
            "created_at": "2025-04-14T10:00:00Z",
            "updated_at": "2025-04-14T10:00:00Z"
        },
        {
            "id": 2,
            "auction_id": 2,
            "user_id": 1,
            "max_bid_amount": 300.0,
            "bid_seconds_before_end": 3,
            "is_active": True,
            "status": "pending",
            "error_message": None,
            "created_at": "2025-04-14T11:00:00Z",
            "updated_at": "2025-04-14T11:00:00Z"
        }
    ]
    
    async def mock_get_bid_configs_func(user_id):
        return [c for c in mock_configs if c['user_id'] == user_id]
    
    async def mock_create_bid_config_func(bid_config_data):
        new_config = {
            "id": 3,
            "created_at": "2025-04-14T12:00:00Z",
            "updated_at": "2025-04-14T12:00:00Z",
            **bid_config_data
        }
        return new_config
    
    with patch('routes.bidding.get_bid_configs', side_effect=mock_get_bid_configs_func):
        with patch('routes.bidding.create_bid_config', side_effect=mock_create_bid_config_func):
            yield mock_configs

# Test get_user_bid_configs endpoint
@patch('models.get_current_user')
def test_get_user_bid_configs(mock_get_current_user, mock_user, mock_bid_configs):
    mock_get_current_user.return_value = mock_user
    
    response = client.get("/api/bid-configs")
    
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["auction_id"] == 1
    assert response.json()[1]["auction_id"] == 2

# Test create_auction_bid_config endpoint
@patch('models.get_current_user')
def test_create_auction_bid_config(mock_get_current_user, mock_user, mock_bid_configs):
    mock_get_current_user.return_value = mock_user
    
    bid_config_data = {
        "auction_id": 3,  # Required field in the model
        "max_bid_amount": 250.0,
        "bid_seconds_before_end": 4,
        "is_active": True
    }
    
    response = client.post(
        "/api/auctions/3/bid-config",
        json=bid_config_data
    )
    
    assert response.status_code == 201
    assert response.json()["auction_id"] == 3
    assert response.json()["max_bid_amount"] == 250.0
    assert response.json()["user_id"] == 1

# Test get_user_bids endpoint
@patch('models.get_current_user')
def test_get_user_bids(mock_get_current_user, mock_user):
    mock_get_current_user.return_value = mock_user
    
    response = client.get("/api/bids")
    
    assert response.status_code == 200
    # Currently returns an empty list as per implementation
    assert response.json() == []
