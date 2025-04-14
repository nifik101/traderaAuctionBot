# Tradera Assistant Backend API

This is the backend API for the Tradera Assistant application, which helps users automate searching, monitoring, and bidding on Tradera auctions.

## Features

- Search for auctions based on user-defined criteria
- Store auction data in Supabase database
- Manage search scripts for automated auction discovery
- Configure and execute last-second bidding
- Track auction statistics and bidding history

## Tech Stack

- FastAPI (Python 3.13)
- Supabase for database
- Clerk for authentication
- Tradera API integration

## Development

### Prerequisites

- Python 3.10+
- pip
- Supabase account
- Tradera API credentials

### Setup

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file with the following variables:
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_ANON_KEY=your_supabase_anon_key
   SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
   TRADERA_APP_ID=your_tradera_app_id
   TRADERA_APP_KEY=your_tradera_app_key
   FRONTEND_URL=your_frontend_url
   NODE_ENV=development
   PORT=8000
   ```
5. Run the development server:
   ```
   uvicorn main:app --reload
   ```

### API Documentation

When the server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Deployment

This application is configured for deployment to Koyeb. See the `deployment_guide.md` file for detailed instructions.

## Project Structure

- `main.py`: FastAPI application entry point
- `db.py`: Database connection and helper functions
- `tradera_api.py`: Tradera API integration
- `routes/`: API route handlers
  - `scripts.py`: Search script management
  - `auctions.py`: Auction data management
  - `bidding.py`: Bidding configuration and execution
- `models.py`: Pydantic models for request/response validation
- `tests/`: Unit and integration tests
- `schema.sql`: Database schema definition
- `setup_db.py`: Script to set up the database schema
- `Dockerfile`: Container definition for deployment
- `koyeb.yaml`: Koyeb deployment configuration
- `requirements.txt`: Python dependencies

## License

MIT
