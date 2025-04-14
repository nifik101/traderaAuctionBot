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
router = APIRouter(tags=["scripts"])

# Initialize TraderaAPI
tradera_api = TraderaAPI()

# Models
class SearchScriptBase(BaseModel):
    name: str
    query: str
    category_id: Optional[int] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    sort_by: Optional[str] = "EndDateAscending"
    is_active: bool = True
    schedule: Optional[str] = "hourly"
    user_id: Optional[str] = None

class SearchScriptCreate(SearchScriptBase):
    pass

class SearchScript(SearchScriptBase):
    id: int
    created_at: str
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True

# Routes
@router.get("/api/scripts", response_model=List[SearchScript])
async def get_scripts():
    """Get all search scripts"""
    try:
        supabase = get_supabase_client()
        response = supabase.table("search_scripts").select("*").execute()
        return response.data
    except Exception as e:
        logger.error(f"Error getting scripts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/scripts/{script_id}", response_model=SearchScript)
async def get_script(script_id: int):
    """Get a specific search script by ID"""
    try:
        supabase = get_supabase_client()
        response = supabase.table("search_scripts").select("*").eq("id", script_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Script not found")
        
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting script {script_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/scripts", response_model=SearchScript)
async def create_script(script: SearchScriptCreate):
    """Create a new search script"""
    try:
        supabase = get_supabase_client()
        response = supabase.table("search_scripts").insert(script.dict()).execute()
        return response.data[0]
    except Exception as e:
        logger.error(f"Error creating script: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/api/scripts/{script_id}", response_model=SearchScript)
async def update_script(script_id: int, script: SearchScriptCreate):
    """Update an existing search script"""
    try:
        supabase = get_supabase_client()
        
        # Check if script exists
        existing = supabase.table("search_scripts").select("*").eq("id", script_id).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Script not found")
        
        # Update script
        response = supabase.table("search_scripts").update(script.dict()).eq("id", script_id).execute()
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating script {script_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/api/scripts/{script_id}")
async def delete_script(script_id: int):
    """Delete a search script"""
    try:
        supabase = get_supabase_client()
        
        # Check if script exists
        existing = supabase.table("search_scripts").select("*").eq("id", script_id).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Script not found")
        
        # Delete script
        supabase.table("search_scripts").delete().eq("id", script_id).execute()
        
        return {"message": "Script deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting script {script_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/scripts/{script_id}/run", response_model=List[dict])
async def run_script(script_id: int):
    """Run a search script and return results"""
    try:
        supabase = get_supabase_client()
        
        # Get script
        script_response = supabase.table("search_scripts").select("*").eq("id", script_id).execute()
        if not script_response.data:
            raise HTTPException(status_code=404, detail="Script not found")
        
        script = script_response.data[0]
        
        # Run search
        search_results = tradera_api.search_advanced(
            search_text=script["query"],
            category_id=script.get("category_id"),
            min_price=script.get("min_price"),
            max_price=script.get("max_price"),
            sort_order=script.get("sort_by", "EndDateAscending")
        )
        
        if "error" in search_results:
            raise HTTPException(status_code=500, detail=search_results["error"])
        
        # Process and store results
        auctions = []
        
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
            else:
                # Insert new auction
                result = supabase.table("auctions").insert(auction_data).execute()
                auction_data.update(result.data[0])
            
            auctions.append(auction_data)
        
        # Update last run time
        supabase.table("search_scripts").update({"updated_at": "now()"}).eq("id", script_id).execute()
        
        return auctions
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error running script {script_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
