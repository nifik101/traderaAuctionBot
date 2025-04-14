# Tradera Assistant

A fullstack web application designed to automate the process of monitoring, selecting, and bidding on Tradera auctions.

## Overview

Tradera Assistant helps users identify potentially undervalued items (especially those ending at night) and place last-second bids to maximize chances of winning auctions at favorable prices.

### Key Features

- **Automated Auction Search & Monitoring**: Configure search criteria and schedule automatic searches
- **Dashboard Interface**: Manage search scripts, review auctions, and configure bidding
- **Automated Bidding System**: Place last-second bids automatically (3-6 seconds before auction end)
- **Statistics & Reporting**: Track auction participation, success rate, and expenditures

## Tech Stack

### Frontend
- React with TypeScript
- Vite as build tool
- pnpm for package management
- Hosted on Vercel

### Backend
- FastAPI with Python 3.13
- Uvicorn as ASGI server
- uv for package management
- Hosted on Koyeb

### Database & Auth
- Supabase (PostgreSQL)
- Clerk for authentication

## Getting Started

### Prerequisites
- Node.js (latest LTS)
- Python 3.13
- pnpm
- uv

### Installation

1. Clone the repository
```bash
git clone https://github.com/nifik101/traderaAuctionBot.git
cd traderaAuctionBot
```

2. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your actual credentials
```

3. Install frontend dependencies
```bash
cd frontend
pnpm install
```

4. Install backend dependencies
```bash
cd backend
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

5. Start development servers
```bash
# Frontend
cd frontend
pnpm dev

# Backend
cd backend
uvicorn main:app --reload
```

## Documentation

For detailed documentation, please refer to the following:

- [Product Requirements Document](./docs/tradera_assistant_prd.md)
- [API Specification](./docs/API_SPEC.md)
- [Data Model](./docs/DATA_MODEL.md)
- [Error Guide](./docs/ERROR_GUIDE.md)
- [Changelog](./docs/CHANGELOG.md)

## License

This project is proprietary and confidential.
