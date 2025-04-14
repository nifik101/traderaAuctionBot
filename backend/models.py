from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Security scheme
security = HTTPBearer()

# Models
class SearchParameters(BaseModel):
    keywords: Optional[str] = None
    categoryId: Optional[int] = None
    regionId: Optional[int] = None
    minPrice: Optional[float] = None
    maxPrice: Optional[float] = None
    sort: Optional[str] = "EndDateAscending"
    buyNowOnly: Optional[bool] = False
    showEnded: Optional[bool] = False

class SearchScript(BaseModel):
    id: Optional[int] = None
    name: str
    search_parameters: SearchParameters
    is_active: bool = True
    schedule: str  # cron format
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_run_at: Optional[datetime] = None

class Auction(BaseModel):
    id: Optional[int] = None
    tradera_id: str
    title: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    seller_id: Optional[str] = None
    seller_name: Optional[str] = None
    current_price: float
    buy_now_price: Optional[float] = None
    shipping_cost: Optional[float] = None
    image_urls: List[str] = []
    start_time: datetime
    end_time: datetime
    url: str
    bid_count: int = 0
    status: str = "active"  # active, ended, won, lost
    script_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class BidConfig(BaseModel):
    id: Optional[int] = None
    auction_id: int
    user_id: Optional[int] = None
    max_bid_amount: float
    bid_seconds_before_end: int = 5
    is_active: bool = True
    status: str = "pending"  # pending, bid_placed, won, lost, error
    error_message: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Bid(BaseModel):
    id: Optional[int] = None
    auction_id: int
    bid_config_id: int
    amount: float
    status: str = "scheduled"  # scheduled, placed, failed
    placed_at: Optional[datetime] = None
    response_status: Optional[str] = None
    response_message: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class User(BaseModel):
    id: int
    clerk_user_id: str
    email: Optional[str] = None
    name: Optional[str] = None
    preferences: Dict[str, Any] = {}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# Dependency for getting the current user
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get the current user from the Clerk JWT token.
    In a real implementation, this would validate the token with Clerk.
    For now, we'll return a mock user.
    """
    # Mock user for development
    return User(
        id=1,
        clerk_user_id="user_123",
        email="user@example.com",
        name="Test User"
    )

# Type alias for the user dependency
UserDependency = User
