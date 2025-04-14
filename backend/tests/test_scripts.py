import sys
import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routes.scripts import router as scripts_router
from models import SearchScript, SearchParameters, User, get_current_user

# Create a test client
from fastapi import FastAPI
test_app = FastAPI()
test_app.include_router(scripts_router)
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
def mock_get_scripts(monkeypatch):
    mock_scripts = [
        {
            "id": 1,
            "name": "Test Script",
            "search_parameters": {
                "keywords": "test",
                "categoryId": 123,
                "regionId": None,
                "minPrice": 100,
                "maxPrice": 1000,
                "sort": "EndDateAscending",
                "buyNowOnly": False,
                "showEnded": False
            },
            "is_active": True,
            "schedule": "0 * * * *",
            "created_at": "2025-04-14T10:00:00Z",
            "updated_at": "2025-04-14T10:00:00Z",
            "last_run_at": None
        }
    ]
    
    async def mock_get_search_scripts(user_id):
        return mock_scripts
    
    with patch('routes.scripts.get_search_scripts', side_effect=mock_get_search_scripts):
        yield mock_scripts

# Test get_scripts endpoint
@patch('models.get_current_user')
def test_get_scripts(mock_get_current_user, mock_user, mock_get_scripts):
    mock_get_current_user.return_value = mock_user
    
    response = client.get("/api/scripts/")
    
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Test Script"
    assert response.json()[0]["is_active"] == True

# Test get_script by ID endpoint
@patch('models.get_current_user')
def test_get_script_by_id(mock_get_current_user, mock_user, mock_get_scripts):
    mock_get_current_user.return_value = mock_user
    
    response = client.get("/api/scripts/1")
    
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "Test Script"

# Test get_script with invalid ID
@patch('models.get_current_user')
def test_get_script_invalid_id(mock_get_current_user, mock_user, mock_get_scripts):
    mock_get_current_user.return_value = mock_user
    
    response = client.get("/api/scripts/999")
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
