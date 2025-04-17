# Code Cleanup Identification Report (Task #9)

This report identifies potential areas for code cleanup based on reviews performed in Task #4 (Backend) and Task #5 (Frontend). No code has been removed; this serves as a list of candidates for future refactoring.

## 1. Unused Code and Imports (Subtask 9.1)

- **Frontend Dependencies (`frontend/package.json`):**
    - `@hookform/resolvers`, `react-hook-form`, `zod`: These libraries seem unused in `ScriptManagement.jsx`. **Verification needed:** Check if they are used in `Dashboard.jsx`, `AuctionListing.jsx`, or `Statistics.jsx` before removal.
- **Backend Dependencies (`backend/requirements.txt`):**
    - `pytest`, `pytest-mock`: Potentially unused if no tests exist or are run in the `tests/` directory. **Verification needed:** Check test suite status.
- **Internal Imports:**
    - A systematic check using static analysis tools (e.g., `vulture` for Python, ESLint rules for JS) is recommended to identify unused imports within specific files across both frontend and backend.

## 2. Duplicated Functionality (Subtask 9.2)

- **Backend Pydantic Models:**
    - **Location:** `backend/routes/scripts.py`, `backend/routes/auctions.py`, `backend/routes/bidding.py` define local models (`Script`, `Auction`, `BidConfig`, `Bid`, etc.).
    - **Issue:** These models duplicate the central models defined in `backend/models.py`.
    - **Recommendation:** Remove local models and refactor routes to use the central models from `backend/models.py` exclusively (after ensuring central models are correct and consistent with the DB schema).
- **Backend Auction Search & Save Logic:**
    - **Location:** `routes/scripts.py` (in `run_script`) and `routes/auctions.py` (in `search_auctions`).
    - **Issue:** Logic for calling `tradera_api.search_advanced()` and then iterating results to check/update/insert into the `auctions` database table is duplicated.
    - **Recommendation:** Extract this common logic into a shared function, potentially in `backend/db.py` or a new `backend/services/auction_service.py`.

## 3. Anti-patterns and Irrelevant Code (Subtask 9.3)

- **Backend Import Hack (`routes/*.py`):**
    - **Issue:** Usage of `sys.path.append` to import `tradera_api.py` from the parent directory.
    - **Recommendation:** Refactor backend structure into a proper Python package or use relative imports (e.g., `from ..tradera_api import TraderaAPI`) to resolve imports correctly without modifying `sys.path`.
- **Backend Mock Authentication (`models.py`):**
    - **Issue:** The `get_current_user` function is a mock implementation and returns a hardcoded user, providing no actual authentication.
    - **Recommendation:** Replace with a proper implementation that validates the Clerk JWT token received via the `Authorization` header.
- **Backend Inconsistent Pydantic Models (`routes/*.py`):**
    - **Issue:** The local Pydantic models (mentioned in section 2) are often inconsistent with `models.py` and the DB schema (e.g., `image_url` vs `image_urls`, `str` vs `datetime`, `float` vs `DECIMAL`).
    - **Recommendation:** Consolidate to use central, consistent models from `models.py`.
- **Backend `create_tables` Function (`db.py`):**
    - **Issue:** Contains SQL for table creation but is noted as not suitable for production; suggests using migrations.
    - **Status:** Keep for reference/initial setup, but acknowledge it's not part of the runtime application logic.
- **Frontend Missing API Call (`ScriptManagement.jsx`):**
    - **Issue:** The `handleToggleScript` function calls `scripts.toggle(id)`, but no corresponding `/api/scripts/{id}/toggle` endpoint exists in the backend.
    - **Recommendation:** Either remove the toggle functionality from the frontend or implement the corresponding endpoint in the backend. 