# Tradera Assistant

A fullstack web application designed to automate the process of monitoring, selecting, and bidding on Tradera auctions.

## Overview

Tradera Assistant helps users identify potentially undervalued items (especially those ending at night) and place last-second bids to maximize chances of winning auctions at favorable prices.

### Key Features

- **Automated Auction Search & Monitoring**: Configure search criteria and schedule automatic searches
- **Dashboard Interface**: Manage search scripts, review auctions, and configure bidding
- **Automated Bidding System**: Place last-second bids automatically (configurable, e.g., 5 seconds before auction end)
- **Statistics & Reporting**: Track auction participation, success rate, and expenditures

## Tech Stack

### Frontend
- React with TypeScript
- Vite as build tool
- pnpm for package management
- Clerk for authentication
- Supabase Client for auth interaction
- Axios for API calls
- React Router for navigation
- Deployment Target: Vercel (or similar)

### Backend
- FastAPI with Python 3.11+ (developed with 3.11/3.13)
- Uvicorn as ASGI server
- uv for package/environment management
- Supabase Python Client for database interaction
- Deployment Target: Koyeb (or similar)

### Database & Auth Provider
- Supabase (PostgreSQL) for database
- Clerk for authentication provider

## Getting Started

### Prerequisites
- Node.js (latest LTS recommended)
- Python 3.11 or higher
- pnpm (`npm install -g pnpm`)
- uv (`pip install uv` or `brew install uv`)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/nifik101/traderaAuctionBot.git
    cd traderaAuctionBot
    ```

2.  **Set up environment variables:**
    - Copy the example file:
      ```bash
      cp .env.example .env
      ```
    - Edit the `.env` file in the project root with your actual credentials for Supabase, Clerk, and potentially Tradera API.

3.  **Install frontend dependencies:**
    ```bash
    cd frontend
    pnpm install
    cd ..
    ```

4.  **Install backend dependencies:**
    ```bash
    cd backend
    # uv will automatically create and use a .venv if one doesn't exist
    uv pip install -r requirements.txt
    cd ..
    ```

### Running the Development Servers

*Make sure you have completed the installation steps and configured your `.env` file.* You need two separate terminals.

1.  **Start the Backend Server:**
    ```bash
    cd backend
    # Activate the virtual environment created by uv
    source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
    
    # Start the FastAPI server with uvicorn
    uvicorn main:app --reload --port 8000
    ```
    The backend API should now be running on `http://localhost:8000`.

2.  **Start the Frontend Server:**
    ```bash
    cd frontend
    pnpm dev
    ```
    The frontend development server should now be running on `http://localhost:5173` (or another port if 5173 is busy).

3.  **Access the Application:** Open your browser and navigate to the frontend URL (usually `http://localhost:5173`).

## Troubleshooting

- **Backend: `Address already in use` (Port 8000):**
    - This usually means a previous backend process is still running.
    - Find the process ID (PID) using the port: `lsof -ti :8000` (macOS/Linux)
    - Stop the process: `kill <PID>` (replace `<PID>` with the actual ID).
    - On macOS/Linux, you can combine these: `lsof -ti :8000 | xargs kill -9`
- **Backend: `ModuleNotFoundError`:**
    - Ensure you have activated the backend virtual environment (`source backend/.venv/bin/activate`) *before* running `uvicorn`.
- **Frontend/Backend Connection Issues:**
    - Verify the `VITE_API_URL` in `frontend/.env` (if created, otherwise defaults in `frontend/src/api/index.js`) matches the backend URL (usually `http://localhost:8000`).
    - Check the `FRONTEND_URL` in the root `.env` file matches the frontend URL (usually `http://localhost:5173`) for CORS configuration in the backend.

## Documentation

For detailed documentation, please refer to the following:

- [Product Requirements Document](./docs/tradera_assistant_prd.md)
- [API Specification](./docs/API_SPEC.md)
- [Data Model](./docs/DATA_MODEL.md)
- [Error Guide](./docs/ERROR_GUIDE.md)
- [Changelog](./docs/CHANGELOG.md)

## License

This project is proprietary and confidential.
