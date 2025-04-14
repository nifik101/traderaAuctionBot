-- Supabase SQL Schema for Tradera Assistant

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

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_auctions_end_time ON auctions(end_time);
CREATE INDEX IF NOT EXISTS idx_search_scripts_is_active ON search_scripts(is_active);
CREATE INDEX IF NOT EXISTS idx_bid_configs_auction_id ON bid_configs(auction_id);
CREATE INDEX IF NOT EXISTS idx_bids_auction_id ON bids(auction_id);

-- Enable Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE search_scripts ENABLE ROW LEVEL SECURITY;
ALTER TABLE auctions ENABLE ROW LEVEL SECURITY;
ALTER TABLE bid_configs ENABLE ROW LEVEL SECURITY;
ALTER TABLE bids ENABLE ROW LEVEL SECURITY;

-- Create policies for authenticated users
CREATE POLICY "Users can view their own data" ON users
    FOR SELECT USING (auth.uid() = clerk_user_id);

CREATE POLICY "Anyone can view auctions" ON auctions
    FOR SELECT USING (true);

CREATE POLICY "Anyone can view search scripts" ON search_scripts
    FOR SELECT USING (true);

CREATE POLICY "Authenticated users can create search scripts" ON search_scripts
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Users can update their own search scripts" ON search_scripts
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own search scripts" ON search_scripts
    FOR DELETE USING (auth.uid() = user_id);

CREATE POLICY "Anyone can view bid configs" ON bid_configs
    FOR SELECT USING (true);

CREATE POLICY "Authenticated users can create bid configs" ON bid_configs
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Anyone can view bids" ON bids
    FOR SELECT USING (true);

CREATE POLICY "Authenticated users can create bids" ON bids
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');
