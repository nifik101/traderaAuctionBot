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
router = APIRouter(tags=["auctions"])

# Initialize TraderaAPI
tradera_api = TraderaAPI()

# Models
class AuctionBase(BaseModel):
    title: str
    description: Optional[str] = None
    tradera_id: str
    current_price: float
    end_time: str
    image_url: Optional[str] = None
    seller_id: Optional[str] = None
    seller_rating: Optional[float] = None
    category: Optional[str] = None
    bid_count: Optional[int] = 0

class AuctionCreate(AuctionBase):
    pass

class Auction(AuctionBase):
    id: int
    created_at: str
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True

class SearchParams(BaseModel):
    query: str
    category_id: Optional[int] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    sort_by: Optional[str] = "EndDateAscending"
    limit: Optional[int] = 20

# Routes
@router.get("/api/auctions", response_model=List[Auction])
async def get_auctions():
    """Get all auctions from the database"""
    try:
        supabase = get_supabase_client()
        response = supabase.table("auctions").select("*").execute()
        return response.data
    except Exception as e:
        logger.error(f"Error getting auctions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/auctions/{auction_id}", response_model=Auction)
async def get_auction(auction_id: int):
    """Get a specific auction by ID"""
    try:
        supabase = get_supabase_client()
        response = supabase.table("auctions").select("*").eq("id", auction_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Auction not found")
        
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting auction {auction_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/search", response_model=List[Auction])
async def search_auctions(search_params: SearchParams):
    """Search for auctions on Tradera and store results in database"""
    try:
        # Search Tradera API
        search_results = tradera_api.search_advanced(
            search_text=search_params.query,
            category_id=search_params.category_id,
            min_price=search_params.min_price,
            max_price=search_params.max_price,
            sort_order=search_params.sort_by,
            items_per_page=search_params.limit
        )
        
        if "error" in search_results:
            raise HTTPException(status_code=500, detail=search_results["error"])
        
        # Process and store results
        auctions = []
        supabase = get_supabase_client()
        
        for item in search_results.get("items", []):
            # Check if auction already exists
            existing = supabase.table("auctions").select("*").eq("tradera_id", item["id"]).execute()
            
            auction_data = {
                "title": item["title"],
                "description": item.get("description", ""),
                "tradera_id": item["id"],
                "current_price": float(item["current_price"]),
                "end_time": item["end_time"],
                "image_url": item.get("image_url", ""),
                "seller_id": item.get("seller_id", ""),
                "seller_rating": float(item.get("seller_rating", 0)),
                "category": item.get("category_name", ""),
                "bid_count": int(item.get("bid_count", 0))
            }
            
            if existing.data:
                # Update existing auction
                auction_id = existing.data[0]["id"]
                supabase.table("auctions").update(auction_data).eq("id", auction_id).execute()
                auction_data["id"] = auction_id
                auction_data["created_at"] = existing.data[0]["created_at"]
                auction_data["updated_at"] = "now()"
            else:
                # Insert new auction
                result = supabase.table("auctions").insert(auction_data).execute()
                auction_data.update(result.data[0])
            
            auctions.append(auction_data)
        
        return auctions
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching auctions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/api/auctions/{auction_id}")
async def delete_auction(auction_id: int):
    """Delete an auction from the database"""
    try:
        supabase = get_supabase_client()
        response = supabase.table("auctions").delete().eq("id", auction_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Auction not found")
        
        return {"message": "Auction deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting auction {auction_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
