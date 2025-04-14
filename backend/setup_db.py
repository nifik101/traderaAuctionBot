import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Supabase credentials
supabase_url = os.getenv("SUPABASE_URL")
supabase_service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

print(f"Supabase URL: {supabase_url}")
print(f"Service Key available: {'Yes' if supabase_service_key else 'No'}")

if not supabase_url or not supabase_service_key:
    print("Error: Supabase credentials not found in environment variables")
    exit(1)

# Set up headers for Supabase REST API
headers = {
    "apikey": supabase_service_key,
    "Authorization": f"Bearer {supabase_service_key}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

# Function to execute SQL via REST API
def execute_sql(sql):
    url = f"{supabase_url}/rest/v1/rpc/exec_sql"
    payload = {
        "sql": sql
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        print(f"SQL executed successfully: {sql[:50]}...")
        return True
    else:
        print(f"Error executing SQL: {response.status_code}")
        print(response.text)
        return False

# Create tables directly using the REST API
try:
    # Create tables
    tables_sql = """
    -- Users table
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
        query TEXT NOT NULL,
        category_id INTEGER,
        min_price DECIMAL(10, 2),
        max_price DECIMAL(10, 2),
        sort_by TEXT DEFAULT 'EndDateAscending',
        is_active BOOLEAN DEFAULT TRUE,
        schedule TEXT DEFAULT 'hourly',
        user_id TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    -- Auctions table
    CREATE TABLE IF NOT EXISTS auctions (
        id SERIAL PRIMARY KEY,
        tradera_id TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        current_price DECIMAL(10, 2) NOT NULL,
        end_time TIMESTAMP WITH TIME ZONE NOT NULL,
        image_url TEXT,
        seller_id TEXT,
        seller_rating DECIMAL(5, 2),
        category TEXT,
        bid_count INTEGER DEFAULT 0,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    -- Bid configurations table
    CREATE TABLE IF NOT EXISTS bid_configs (
        id SERIAL PRIMARY KEY,
        auction_id INTEGER REFERENCES auctions(id) ON DELETE CASCADE,
        max_bid_amount DECIMAL(10, 2) NOT NULL,
        bid_seconds_before_end INTEGER DEFAULT 10,
        is_active BOOLEAN DEFAULT TRUE,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    -- Bids table
    CREATE TABLE IF NOT EXISTS bids (
        id SERIAL PRIMARY KEY,
        auction_id INTEGER REFERENCES auctions(id) ON DELETE CASCADE,
        amount DECIMAL(10, 2) NOT NULL,
        status TEXT DEFAULT 'pending',
        tradera_response TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """
    
    # Split and execute table creation statements
    for statement in tables_sql.split(';'):
        statement = statement.strip()
        if statement:
            execute_sql(statement)
    
    # Create indexes
    indexes_sql = """
    CREATE INDEX IF NOT EXISTS idx_auctions_end_time ON auctions(end_time);
    CREATE INDEX IF NOT EXISTS idx_search_scripts_is_active ON search_scripts(is_active);
    CREATE INDEX IF NOT EXISTS idx_bid_configs_auction_id ON bid_configs(auction_id);
    CREATE INDEX IF NOT EXISTS idx_bids_auction_id ON bids(auction_id);
    """
    
    # Split and execute index creation statements
    for statement in indexes_sql.split(';'):
        statement = statement.strip()
        if statement:
            execute_sql(statement)
    
    # Enable RLS
    rls_sql = """
    ALTER TABLE users ENABLE ROW LEVEL SECURITY;
    ALTER TABLE search_scripts ENABLE ROW LEVEL SECURITY;
    ALTER TABLE auctions ENABLE ROW LEVEL SECURITY;
    ALTER TABLE bid_configs ENABLE ROW LEVEL SECURITY;
    ALTER TABLE bids ENABLE ROW LEVEL SECURITY;
    """
    
    # Split and execute RLS statements
    for statement in rls_sql.split(';'):
        statement = statement.strip()
        if statement:
            execute_sql(statement)
    
    # Create policies
    policies_sql = """
    DROP POLICY IF EXISTS "Anyone can view auctions" ON auctions;
    CREATE POLICY "Anyone can view auctions" ON auctions FOR SELECT USING (true);
    
    DROP POLICY IF EXISTS "Anyone can view search scripts" ON search_scripts;
    CREATE POLICY "Anyone can view search scripts" ON search_scripts FOR SELECT USING (true);
    
    DROP POLICY IF EXISTS "Authenticated users can create search scripts" ON search_scripts;
    CREATE POLICY "Authenticated users can create search scripts" ON search_scripts FOR INSERT WITH CHECK (true);
    
    DROP POLICY IF EXISTS "Anyone can view bid configs" ON bid_configs;
    CREATE POLICY "Anyone can view bid configs" ON bid_configs FOR SELECT USING (true);
    
    DROP POLICY IF EXISTS "Anyone can view bids" ON bids;
    CREATE POLICY "Anyone can view bids" ON bids FOR SELECT USING (true);
    """
    
    # Split and execute policy statements
    for statement in policies_sql.split(';'):
        statement = statement.strip()
        if statement:
            execute_sql(statement)
    
    print("Database schema setup completed successfully")
    
except Exception as e:
    print(f"Error setting up database schema: {str(e)}")
    print("Database schema setup failed")
