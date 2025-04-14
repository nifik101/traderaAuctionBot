from supabase import create_client
import os
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_ANON_KEY")
supabase = create_client(supabase_url, supabase_key)

# Function to get Supabase client
def get_supabase_client():
    """Return the initialized Supabase client"""
    return supabase

# Database helper functions
async def create_tables():
    """
    Create the necessary tables in Supabase if they don't exist.
    This function is used for initial setup and should be run once.
    """
    # Define SQL for creating tables
    create_tables_sql = """
    -- Users table (linked to Clerk)
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        clerk_user_id TEXT UNIQUE NOT NULL,
        email TEXT,
        name TEXT,
        preferences JSONB DEFAULT '{}'::jsonb,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    -- Search scripts table
    CREATE TABLE IF NOT EXISTS search_scripts (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        search_parameters JSONB NOT NULL,
        is_active BOOLEAN DEFAULT TRUE,
        schedule TEXT NOT NULL, -- cron format
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        last_run_at TIMESTAMP WITH TIME ZONE
    );

    -- Auctions table
    CREATE TABLE IF NOT EXISTS auctions (
        id SERIAL PRIMARY KEY,
        tradera_id TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        category_id INTEGER,
        seller_id TEXT,
        seller_name TEXT,
        current_price DECIMAL(10, 2) NOT NULL,
        buy_now_price DECIMAL(10, 2),
        shipping_cost DECIMAL(10, 2),
        image_urls JSONB DEFAULT '[]'::jsonb,
        start_time TIMESTAMP WITH TIME ZONE NOT NULL,
        end_time TIMESTAMP WITH TIME ZONE NOT NULL,
        url TEXT NOT NULL,
        bid_count INTEGER DEFAULT 0,
        status TEXT DEFAULT 'active',
        script_id INTEGER REFERENCES search_scripts(id) ON DELETE SET NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    -- Bid configurations table
    CREATE TABLE IF NOT EXISTS bid_configs (
        id SERIAL PRIMARY KEY,
        auction_id INTEGER REFERENCES auctions(id) ON DELETE CASCADE,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        max_bid_amount DECIMAL(10, 2) NOT NULL,
        bid_seconds_before_end INTEGER DEFAULT 5,
        is_active BOOLEAN DEFAULT TRUE,
        status TEXT DEFAULT 'pending',
        error_message TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    -- Bids table
    CREATE TABLE IF NOT EXISTS bids (
        id SERIAL PRIMARY KEY,
        auction_id INTEGER REFERENCES auctions(id) ON DELETE CASCADE,
        bid_config_id INTEGER REFERENCES bid_configs(id) ON DELETE CASCADE,
        amount DECIMAL(10, 2) NOT NULL,
        status TEXT DEFAULT 'scheduled',
        placed_at TIMESTAMP WITH TIME ZONE,
        response_status TEXT,
        response_message TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    -- Create indexes for performance
    CREATE INDEX IF NOT EXISTS idx_auctions_end_time ON auctions(end_time);
    CREATE INDEX IF NOT EXISTS idx_auctions_status ON auctions(status);
    CREATE INDEX IF NOT EXISTS idx_search_scripts_user_id ON search_scripts(user_id);
    CREATE INDEX IF NOT EXISTS idx_bid_configs_auction_id ON bid_configs(auction_id);
    CREATE INDEX IF NOT EXISTS idx_bids_auction_id ON bids(auction_id);
    """
    
    # Execute the SQL
    try:
        # Note: In a real implementation, we would use a migration tool
        # or execute this directly in the Supabase SQL editor
        # For this example, we'll just print the SQL that would be executed
        print("SQL for creating tables would be executed here:")
        print(create_tables_sql)
        return {"status": "success", "message": "Tables would be created"}
    except Exception as e:
        print(f"Error creating tables: {str(e)}")
        return {"status": "error", "message": str(e)}

# User functions
async def get_or_create_user(clerk_user_id: str, email: str, name: str) -> Dict[str, Any]:
    """Get a user by Clerk ID or create if not exists"""
    user = supabase.table("users").select("*").eq("clerk_user_id", clerk_user_id).execute()
    
    if user.data and len(user.data) > 0:
        return user.data[0]
    
    # Create new user
    new_user = {
        "clerk_user_id": clerk_user_id,
        "email": email,
        "name": name
    }
    
    result = supabase.table("users").insert(new_user).execute()
    if result.data and len(result.data) > 0:
        return result.data[0]
    
    raise Exception("Failed to create user")

# Search script functions
async def create_search_script(user_id: int, name: str, search_parameters: Dict, schedule: str) -> Dict[str, Any]:
    """Create a new search script"""
    script = {
        "user_id": user_id,
        "name": name,
        "search_parameters": json.dumps(search_parameters),
        "schedule": schedule,
        "is_active": True
    }
    
    result = supabase.table("search_scripts").insert(script).execute()
    if result.data and len(result.data) > 0:
        return result.data[0]
    
    raise Exception("Failed to create search script")

async def get_search_scripts(user_id: int) -> List[Dict[str, Any]]:
    """Get all search scripts for a user"""
    result = supabase.table("search_scripts").select("*").eq("user_id", user_id).execute()
    return result.data if result.data else []

async def update_search_script(script_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
    """Update a search script"""
    if "search_parameters" in data and not isinstance(data["search_parameters"], str):
        data["search_parameters"] = json.dumps(data["search_parameters"])
    
    data["updated_at"] = datetime.now().isoformat()
    
    result = supabase.table("search_scripts").update(data).eq("id", script_id).execute()
    if result.data and len(result.data) > 0:
        return result.data[0]
    
    raise Exception("Failed to update search script")

# Auction functions
async def create_auction(auction_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new auction record"""
    if "image_urls" in auction_data and not isinstance(auction_data["image_urls"], str):
        auction_data["image_urls"] = json.dumps(auction_data["image_urls"])
    
    result = supabase.table("auctions").insert(auction_data).execute()
    if result.data and len(result.data) > 0:
        return result.data[0]
    
    raise Exception("Failed to create auction")

async def get_auctions(filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Get auctions with optional filters"""
    query = supabase.table("auctions").select("*")
    
    if filters:
        for key, value in filters.items():
            if key == "status" and isinstance(value, list):
                query = query.in_(key, value)
            elif key == "end_time_lt":
                query = query.lt("end_time", value)
            elif key == "end_time_gt":
                query = query.gt("end_time", value)
            else:
                query = query.eq(key, value)
    
    result = query.execute()
    return result.data if result.data else []

# Bid configuration functions
async def create_bid_config(bid_config_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new bid configuration"""
    result = supabase.table("bid_configs").insert(bid_config_data).execute()
    if result.data and len(result.data) > 0:
        return result.data[0]
    
    raise Exception("Failed to create bid configuration")

async def get_bid_configs(user_id: int) -> List[Dict[str, Any]]:
    """Get all bid configurations for a user"""
    result = supabase.table("bid_configs").select("*, auctions(*)").eq("user_id", user_id).execute()
    return result.data if result.data else []

# Bid functions
async def create_bid(bid_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new bid record"""
    result = supabase.table("bids").insert(bid_data).execute()
    if result.data and len(result.data) > 0:
        return result.data[0]
    
    raise Exception("Failed to create bid")

async def get_bids(auction_id: int) -> List[Dict[str, Any]]:
    """Get all bids for an auction"""
    result = supabase.table("bids").select("*").eq("auction_id", auction_id).execute()
    return result.data if result.data else []

# Statistics functions
async def get_user_statistics(user_id: int) -> Dict[str, Any]:
    """Get statistics for a user"""
    # This would be a more complex query in a real implementation
    # For now, we'll return a placeholder
    return {
        "total_auctions_found": 0,
        "auctions_with_bids": 0,
        "auctions_won": 0,
        "auctions_lost": 0,
        "total_spent": 0
    }
