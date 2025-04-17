# 📘 API_SPEC.md – API-specifikation

**Syfte:**  
Detta dokument innehåller en översikt över samtliga API-endpoints i projektet. Det hjälper både utvecklare och Claude att förstå strukturen, vad som krävs för varje endpoint, och vad som returneras.

> 🧠 **Instruktion till Claude:**  
Varje gång du skapar, ändrar eller raderar en endpoint, **uppdatera detta dokument** automatiskt. Beskriv även headers, URL, metoder och payload.

---

## 📌 Exempelstruktur

### [GET] `/api/users/{id}`

- **Beskrivning:** Hämtar användarinformation baserat på ID.
- **Request:**
    - URL-parametrar: `id` (int)
    - Headers: `Authorization: Bearer <token>`
- **Response:**  
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "Ada Lovelace"
}

Statuskoder: 200 OK, 404 Not Found, 401 Unauthorized
```

# Tradera Assistant API Specification (v0.1.2 - As Implemented)

This document describes the API endpoints as currently implemented based on the code review (Task #4).

**Base URL:** `/` (Hosted base URL depends on deployment)

## Authentication

**Method:** Bearer Token (JWT from Clerk) - **CURRENTLY NOT ENFORCED/VALIDATED**

- The frontend *attempts* to send a JWT token obtained from Clerk via the `Authorization: Bearer <token>` header (handled by axios interceptor in `frontend/src/api/index.js`).
- The backend currently **DOES NOT** validate this token. The `get_current_user` dependency in `backend/models.py` is a mock and is **NOT USED** by any endpoints.
- **All endpoints listed below are currently unprotected.**

**(Subtask 6.1)** - No specific authentication endpoints (like login, refresh) were found in the backend code. Authentication flow is expected to be handled by Clerk externally.

## API Endpoints

### Root

**(Subtask 6.2)**

#### `GET /`

- **Description:** Root endpoint to check if API is running.
- **Authentication:** None (Public)
- **Response (200 OK):**
  ```json
  {
    "message": "Tradera Assistant API is running",
    "version": "string",
    "status": "online"
  }
  ```

#### `GET /health`

- **Description:** Health check endpoint for monitoring.
- **Authentication:** None (Public)
- **Response (200 OK):**
  ```json
  {
    "status": "healthy",
    "version": "string"
  }
  ```

### Scripts (`/api/scripts`)

**(Subtasks 6.2 & 6.3)**

*Note: These endpoints currently lack user association/authorization.*

#### `GET /api/scripts`

- **Description:** Get all search scripts stored in the database.
- **Authentication:** **None (CRITICAL ISSUE)**
- **Response (200 OK):** `List[Script]` (Uses local model definition in `routes/scripts.py`, inconsistent with `models.py`)
  ```json
  [
    {
      "id": 0,
      "name": "string",
      "query": "string",
      "category_id": 0,
      "min_price": 0,
      "max_price": 0,
      "sort_by": "string",
      "is_active": true,
      "schedule": "string",
      "user_id": "string", 
      "created_at": "string (datetime)",
      "updated_at": "string (datetime)" 
    }
  ]
  ```
- **Error Response (500):** Internal Server Error

#### `GET /api/scripts/{script_id}`

- **Description:** Get a specific search script by its database ID.
- **Authentication:** **None (CRITICAL ISSUE)**
- **Path Parameters:**
    - `script_id` (integer): The ID of the script to retrieve.
- **Response (200 OK):** `Script` (Uses local model definition)
  ```json
  {
    "id": 0,
    // ... (same fields as above)
  }
  ```
- **Error Response (404):** `{"detail": "Script not found"}`
- **Error Response (500):** Internal Server Error

#### `POST /api/scripts`

- **Description:** Create a new search script.
- **Authentication:** **None (CRITICAL ISSUE)**
- **Request Body:** `ScriptCreate` (Uses local model definition)
  ```json
  {
    "name": "string",
    "query": "string",
    "category_id": 0,
    "min_price": 0,
    "max_price": 0,
    "sort_by": "string",
    "is_active": true,
    "schedule": "string",
    "user_id": "string" // Not currently used/validated
  }
  ```
- **Response (200 OK):** `Script` (The created script object from DB)
- **Error Response (500):** Internal Server Error

#### `PUT /api/scripts/{script_id}`

- **Description:** Update an existing search script.
- **Authentication:** **None (CRITICAL ISSUE)**
- **Path Parameters:**
    - `script_id` (integer): The ID of the script to update.
- **Request Body:** `ScriptCreate` (Uses local model definition)
- **Response (200 OK):** `Script` (The updated script object from DB)
- **Error Response (404):** `{"detail": "Script not found"}`
- **Error Response (500):** Internal Server Error

#### `DELETE /api/scripts/{script_id}`

- **Description:** Delete a search script.
- **Authentication:** **None (CRITICAL ISSUE)**
- **Path Parameters:**
    - `script_id` (integer): The ID of the script to delete.
- **Response (200 OK):**
  ```json
  {
    "message": "Script deleted successfully"
  }
  ```
- **Error Response (404):** `{"detail": "Script not found"}`
- **Error Response (500):** Internal Server Error

#### `POST /api/scripts/{script_id}/run`

- **Description:** Run a specific search script immediately, search Tradera, store/update results in the `auctions` table, and return the found/updated auctions.
- **Authentication:** **None (CRITICAL ISSUE)**
- **Path Parameters:**
    - `script_id` (integer): The ID of the script to run.
- **Response (200 OK):** `List[dict]` (Represents auctions found/updated, uses inconsistent fields compared to DB/models)
  ```json
  [
    {
      "title": "string",
      "description": "string",
      "tradera_id": "string",
      "current_price": 0.0,
      "end_time": "string (datetime)",
      "image_url": "string", // Note: inconsistent with DB schema ('image_urls')
      "seller_id": "string",
      "seller_rating": 0.0,
      "category": "string", // Note: inconsistent with DB schema ('category_id')
      "bid_count": 0,
      "id": 0, // DB id
      "created_at": "string (datetime)", // Only present on update
      "updated_at": "string (datetime)" // Only present on update
    }
    // ...
  ]
  ```
- **Error Response (404):** `{"detail": "Script not found"}`
- **Error Response (500):** Internal Server Error (can be from DB or Tradera API search)

### Auctions (`/api/auctions`, `/api/search`)

**(Subtasks 6.2 & 6.3)**

*Note: These endpoints currently lack user association/authorization.*

#### `GET /api/auctions`

- **Description:** Get all auctions stored in the database.
- **Authentication:** **None (CRITICAL ISSUE)**
- **Response (200 OK):** `List[Auction]` (Uses local model definition in `routes/auctions.py`, inconsistent with `models.py`)
  ```json
  [
    {
      "id": 0,
      "title": "string",
      "description": "string",
      "tradera_id": "string",
      "current_price": 0.0,
      "end_time": "string (datetime)", // Note: inconsistent type vs models.py (datetime)
      "image_url": "string", // Note: inconsistent with DB schema ('image_urls')
      "seller_id": "string",
      "seller_rating": 0.0,
      "category": "string", // Note: inconsistent with DB schema ('category_id')
      "bid_count": 0,
      "created_at": "string (datetime)",
      "updated_at": "string (datetime)" 
    }
  ]
  ```
- **Error Response (500):** Internal Server Error

#### `GET /api/auctions/{auction_id}`

- **Description:** Get a specific auction by its database ID.
- **Authentication:** **None (CRITICAL ISSUE)**
- **Path Parameters:**
    - `auction_id` (integer): The ID of the auction to retrieve.
- **Response (200 OK):** `Auction` (Uses local model definition)
  ```json
  {
    "id": 0,
    // ... (same fields as above)
  }
  ```
- **Error Response (404):** `{"detail": "Auction not found"}`
- **Error Response (500):** Internal Server Error

#### `POST /api/search`

- **Description:** Perform a one-off search on Tradera, store/update results in the `auctions` table, and return the found/updated auctions.
- **Authentication:** **None (CRITICAL ISSUE)**
- **Request Body:** `SearchParams` (Uses local model definition)
  ```json
  {
    "query": "string",
    "category_id": 0,
    "min_price": 0,
    "max_price": 0,
    "sort_by": "string",
    "limit": 20
  }
  ```
- **Response (200 OK):** `List[Auction]` (Represents auctions found/updated, uses inconsistent fields compared to DB/models - same as `/api/scripts/{script_id}/run`)
- **Error Response (500):** Internal Server Error (can be from DB or Tradera API search)

#### `DELETE /api/auctions/{auction_id}`

- **Description:** Delete an auction from the database.
- **Authentication:** **None (CRITICAL ISSUE)**
- **Path Parameters:**
    - `auction_id` (integer): The ID of the auction to delete.
- **Response (200 OK):**
  ```json
  {
    "message": "Auction deleted successfully"
  }
  ```
- **Error Response (404):** `{"detail": "Auction not found"}` (Note: Implementation might not correctly check for 404 on delete)
- **Error Response (500):** Internal Server Error

### Bidding (`/api/bid-configs`, `/api/bids`, `/api/auctions/{auction_id}/...`)

**(Subtasks 6.2 & 6.3)**

*Note: These endpoints currently lack user association/authorization. `place_bid` accepts token insecurely.*

#### `GET /api/bid-configs`

- **Description:** Get all bid configurations stored in the database.
- **Authentication:** **None (CRITICAL ISSUE)**
- **Response (200 OK):** `List[BidConfig]` (Uses local model definition in `routes/bidding.py`, inconsistent with `models.py`)
  ```json
  [
    {
      "id": 0,
      "auction_id": 0,
      "max_bid_amount": 0.0,
      "bid_seconds_before_end": 0,
      "is_active": true,
      "status": "string",
      "created_at": "string (datetime)",
      "updated_at": "string (datetime)"
    }
  ]
  ```
- **Error Response (500):** Internal Server Error

#### `POST /api/auctions/{auction_id}/bid-config`

- **Description:** Create a new bid configuration for a specific auction.
- **Authentication:** **None (CRITICAL ISSUE)**
- **Path Parameters:**
    - `auction_id` (integer): The ID of the auction to configure bidding for.
- **Request Body:** `BidConfigCreate` (Uses local model definition)
  ```json
  {
    "auction_id": 0, // Redundant, taken from path param
    "max_bid_amount": 0.0,
    "bid_seconds_before_end": 0,
    "is_active": true
  }
  ```
- **Response (200 OK):** `BidConfig` (The created config object from DB)
- **Error Response (404):** `{"detail": "Auction not found"}`
- **Error Response (400):** `{"detail": "Bid configuration already exists for this auction"}`
- **Error Response (500):** Internal Server Error

#### `PUT /api/auctions/{auction_id}/bid-config`

- **Description:** Update an existing bid configuration for a specific auction.
- **Authentication:** **None (CRITICAL ISSUE)**
- **Path Parameters:**
    - `auction_id` (integer): The ID of the auction whose config to update.
- **Request Body:** `BidConfigCreate` (Uses local model definition)
- **Response (200 OK):** `BidConfig` (The updated config object from DB)
- **Error Response (404):** `{"detail": "Bid configuration not found"}`
- **Error Response (500):** Internal Server Error

#### `DELETE /api/auctions/{auction_id}/bid-config`

- **Description:** Delete a bid configuration for a specific auction.
- **Authentication:** **None (CRITICAL ISSUE)**
- **Path Parameters:**
    - `auction_id` (integer): The ID of the auction whose config to delete.
- **Response (200 OK):**
  ```json
  {
    "message": "Bid configuration deleted successfully"
  }
  ```
- **Error Response (404):** `{"detail": "Bid configuration not found"}`
- **Error Response (500):** Internal Server Error

#### `POST /api/auctions/{auction_id}/bid`

- **Description:** Place a bid on a specific auction via the Tradera API.
- **Authentication:** **None (CRITICAL ISSUE + Insecure Token Handling)**
- **Path Parameters:**
    - `auction_id` (integer): The ID of the auction in the database.
- **Request Body:** `BidCreate` (Uses local model definition)
  ```json
  {
    "auction_id": 0, // Redundant
    "amount": 0.0,
    "user_id": 0, // Insecurely provided
    "token": "string" // Insecurely provided
  }
  ```
- **Response (200 OK):** `Bid` (Uses local model definition, includes extra Tradera info)
  ```json
  {
    "id": 0,
    "auction_id": 0,
    "amount": 0.0,
    "user_id": 0,
    "token": null, // Not returned
    "status": "string", // e.g., "won", "placed"
    "created_at": "string (datetime)",
    "tradera_response": "string", // Raw response from API
    "tradera_status": "string", // Status from Tradera (e.g., "Bought")
    "next_bid": 0.0 // Next required bid amount from Tradera
  }
  ```
- **Error Response (404):** `{"detail": "Auction not found"}`
- **Error Response (500):** Internal Server Error (can be from DB or Tradera API bid placement)

#### `GET /api/bids`

- **Description:** Get all bids stored in the database.
- **Authentication:** **None (CRITICAL ISSUE)**
- **Response (200 OK):** `List[Bid]` (Uses local model definition)
  ```json
  [
    {
      "id": 0,
      "auction_id": 0,
      "amount": 0.0,
      "user_id": 0,
      "token": null,
      "status": "string",
      "created_at": "string (datetime)",
      "tradera_response": "string",
      "tradera_status": "string",
      "next_bid": 0.0
    }
  ]
  ```
- **Error Response (500):** Internal Server Error

## Error Handling Standards

**(Subtask 6.4)**

- **Standard Success:** `200 OK` with JSON body as described above.
- **Standard Client Errors:**
    - `404 Not Found`: Used when a specific resource (script, auction, bid config) is not found by ID. Response body: `{"detail": "<Resource> not found"}`.
    - `400 Bad Request`: Used when trying to create a duplicate bid configuration. Response body: `{"detail": "Bid configuration already exists for this auction"}`.
    - Validation errors (e.g., incorrect request body format) are likely handled by FastAPI's default Pydantic validation, returning a `422 Unprocessable Entity` error with details about the validation failure (not explicitly documented here).
- **Authentication Errors:**
    - Currently, no `401 Unauthorized` or `403 Forbidden` errors are expected from the backend as authentication is not implemented.
    - The frontend interceptor *will* trigger a redirect to `/sign-in` if it receives a `401` from *any* source (potentially including Clerk itself during token refresh, though unlikely from this backend).
- **Server Errors:**
    - `500 Internal Server Error`: Used for general exceptions caught in the `try...except` blocks in route handlers (e.g., database errors, Tradera API errors, unexpected Python exceptions). Response body usually includes the raw error message: `{"detail": "<error message>"}`.