from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
import logging
from db import get_supabase_client
import sys
import os

# Add the parent directory to sys.path to allow absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tradera_api import TraderaAPI

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(tags=["bidding"])

# Initialize TraderaAPI
tradera_api = TraderaAPI()

# Models
class BidConfigBase(BaseModel):
    auction_id: int
    max_bid_amount: float
    bid_seconds_before_end: int
    is_active: bool = True

class BidConfigCreate(BidConfigBase):
    pass

class BidConfig(BidConfigBase):
    id: int
    status: str = "pending"
    created_at: str
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True

class BidBase(BaseModel):
    auction_id: int
    amount: float
    user_id: Optional[int] = None
    token: Optional[str] = None

class BidCreate(BidBase):
    pass

class Bid(BidBase):
    id: int
    status: str
    created_at: str
    tradera_response: Optional[str] = None
    tradera_status: Optional[str] = None
    next_bid: Optional[float] = None

    class Config:
        orm_mode = True

# Routes
@router.get("/api/bid-configs", response_model=List[BidConfig])
async def get_bid_configs():
    """Get all bid configurations"""
    try:
        supabase = get_supabase_client()
        response = supabase.table("bid_configs").select("*").execute()
        return response.data
    except Exception as e:
        logger.error(f"Error getting bid configs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/auctions/{auction_id}/bid-config", response_model=BidConfig)
async def create_bid_config(auction_id: int, bid_config: BidConfigCreate):
    """Create a new bid configuration for an auction"""
    try:
        supabase = get_supabase_client()
        
        # Check if auction exists
        auction_response = supabase.table("auctions").select("*").eq("id", auction_id).execute()
        if not auction_response.data:
            raise HTTPException(status_code=404, detail="Auction not found")
        
        # Check if bid config already exists
        existing_config = supabase.table("bid_configs").select("*").eq("auction_id", auction_id).execute()
        if existing_config.data:
            raise HTTPException(status_code=400, detail="Bid configuration already exists for this auction")
        
        # Create bid config
        bid_config_data = bid_config.dict()
        bid_config_data["auction_id"] = auction_id
        
        response = supabase.table("bid_configs").insert(bid_config_data).execute()
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating bid config: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/api/auctions/{auction_id}/bid-config", response_model=BidConfig)
async def update_bid_config(auction_id: int, bid_config: BidConfigCreate):
    """Update an existing bid configuration"""
    try:
        supabase = get_supabase_client()
        
        # Check if bid config exists
        existing_config = supabase.table("bid_configs").select("*").eq("auction_id", auction_id).execute()
        if not existing_config.data:
            raise HTTPException(status_code=404, detail="Bid configuration not found")
        
        # Update bid config
        bid_config_data = bid_config.dict()
        config_id = existing_config.data[0]["id"]
        
        response = supabase.table("bid_configs").update(bid_config_data).eq("id", config_id).execute()
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating bid config: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/api/auctions/{auction_id}/bid-config")
async def delete_bid_config(auction_id: int):
    """Delete a bid configuration"""
    try:
        supabase = get_supabase_client()
        
        # Check if bid config exists
        existing_config = supabase.table("bid_configs").select("*").eq("auction_id", auction_id).execute()
        if not existing_config.data:
            raise HTTPException(status_code=404, detail="Bid configuration not found")
        
        # Delete bid config
        config_id = existing_config.data[0]["id"]
        supabase.table("bid_configs").delete().eq("id", config_id).execute()
        
        return {"message": "Bid configuration deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting bid config: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/auctions/{auction_id}/bid", response_model=Bid)
async def place_bid(auction_id: int, bid: BidCreate):
    """Place a bid on an auction"""
    try:
        supabase = get_supabase_client()
        
        # Check if auction exists
        auction_response = supabase.table("auctions").select("*").eq("id", auction_id).execute()
        if not auction_response.data:
            raise HTTPException(status_code=404, detail="Auction not found")
        
        auction = auction_response.data[0]
        
        # Set user token if provided
        if bid.user_id and bid.token:
            tradera_api.set_user_token(bid.user_id, bid.token)
        
        # Place bid via Tradera API
        bid_result = tradera_api.place_bid(
            item_id=int(auction["tradera_id"]),
            bid_amount=bid.amount
        )
        
        if "error" in bid_result:
            raise HTTPException(status_code=500, detail=bid_result["error"])
        
        # Determine bid status
        status = "won" if bid_result.get("status") == "Bought" else "placed"
        
        # Store bid in database
        bid_data = {
            "auction_id": auction_id,
            "amount": bid.amount,
            "status": status,
            "tradera_response": str(bid_result)
        }
        
        bid_response = supabase.table("bids").insert(bid_data).execute()
        
        # Update auction bid count
        supabase.table("auctions").update({
            "bid_count": (auction.get("bid_count", 0) or 0) + 1
        }).eq("id", auction_id).execute()
        
        # Return bid with additional info
        result = bid_response.data[0]
        result["tradera_status"] = bid_result.get("status")
        result["next_bid"] = bid_result.get("next_bid")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error placing bid: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/bids", response_model=List[Bid])
async def get_bids():
    """Get all bids"""
    try:
        supabase = get_supabase_client()
        response = supabase.table("bids").select("*").execute()
        return response.data
    except Exception as e:
        logger.error(f"Error getting bids: {e}")
        raise HTTPException(status_code=500, detail=str(e))
