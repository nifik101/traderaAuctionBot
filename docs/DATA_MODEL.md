# 🧬 DATA_MODEL.md – Datamodeller och strukturer

**Syfte:**  
Här dokumenteras alla databastabeller, modeller och scheman i systemet. Claude och utvecklare använder detta för att hålla koll på fält, relationer och datatyper.

> 🧠 **Instruktion till Claude:**  
Varje gång du skapar eller ändrar en datamodell, **uppdatera detta dokument** automatiskt. Lägg till datatyper och validering.

---

## 📌 Exempelmodell

### Modell: `User`

| Fält       | Typ        | Validering / Notering           |
|------------|------------|----------------------------------|
| `id`       | Integer    | Primärnyckel, autoinkrement     |
| `email`    | String     | Unik, krävs, e-postvalidering   |
| `name`     | String     | Obligatorisk                    |
| `created_at` | DateTime | Genereras automatiskt           |

---

## 🧱 Aktuella modeller

*(Lägg till här under projektets gång)*

# Tradera Assistant Data Model

This document describes the database schema used by the Tradera Assistant application, as defined in `backend/db.py`.

## Tables

### `users`

Stores user information, linked to Clerk authentication.

| Column          | Type                          | Constraints                   | Default                     | Description                                |
|-----------------|-------------------------------|-------------------------------|-----------------------------|--------------------------------------------|
| `id`            | `SERIAL`                      | `PRIMARY KEY`                 | Auto-incrementing           | Internal database user ID.                 |
| `clerk_user_id` | `TEXT`                        | `UNIQUE NOT NULL`             |                             | User ID from Clerk authentication system.  |
| `email`         | `TEXT`                        |                               |                             | User's email address.                      |
| `name`          | `TEXT`                        |                               |                             | User's name.                               |
| `preferences`   | `JSONB`                       |                               | `'{}'::jsonb`               | User-specific preferences (e.g., UI).    |
| `created_at`    | `TIMESTAMP WITH TIME ZONE`    |                               | `NOW()`                     | Timestamp when the user was created.       |
| `updated_at`    | `TIMESTAMP WITH TIME ZONE`    |                               | `NOW()`                     | Timestamp when the user was last updated.  |

### `search_scripts`

Stores user-defined search configurations to be run periodically.

| Column              | Type                          | Constraints                     | Default                     | Description                                     |
|---------------------|-------------------------------|---------------------------------|-----------------------------|-------------------------------------------------|
| `id`                | `SERIAL`                      | `PRIMARY KEY`                   | Auto-incrementing           | Internal script ID.                             |
| `name`              | `TEXT`                        | `NOT NULL`                      |                             | User-defined name for the script.               |
| `user_id`           | `INTEGER`                     | `REFERENCES users(id) ON DELETE CASCADE` |                             | Foreign key linking to the `users` table.        |
| `search_parameters` | `JSONB`                       | `NOT NULL`                      |                             | Search criteria (keywords, category, price etc).|
| `is_active`         | `BOOLEAN`                     |                                 | `TRUE`                      | Whether the script is currently active.         |
| `schedule`          | `TEXT`                        | `NOT NULL`                      |                             | Cron string defining the run schedule.          |
| `created_at`        | `TIMESTAMP WITH TIME ZONE`    |                                 | `NOW()`                     | Timestamp when the script was created.          |
| `updated_at`        | `TIMESTAMP WITH TIME ZONE`    |                                 | `NOW()`                     | Timestamp when the script was last updated.     |
| `last_run_at`       | `TIMESTAMP WITH TIME ZONE`    |                                 |                             | Timestamp when the script was last executed.    |

### `auctions`

Stores information about auctions found by search scripts or manual searches.

| Column          | Type                          | Constraints                     | Default                     | Description                                      |
|-----------------|-------------------------------|---------------------------------|-----------------------------|--------------------------------------------------|
| `id`            | `SERIAL`                      | `PRIMARY KEY`                   | Auto-incrementing           | Internal auction ID.                             |
| `tradera_id`    | `TEXT`                        | `UNIQUE NOT NULL`             |                             | Auction ID from Tradera.                         |
| `title`         | `TEXT`                        | `NOT NULL`                      |                             | Auction title.                                   |
| `description`   | `TEXT`                        |                                 |                             | Auction description.                             |
| `category_id`   | `INTEGER`                     |                                 |                             | Tradera category ID.                             |
| `seller_id`     | `TEXT`                        |                                 |                             | Tradera seller ID.                               |
| `seller_name`   | `TEXT`                        |                                 |                             | Tradera seller name.                             |
| `current_price` | `DECIMAL(10, 2)`              | `NOT NULL`                      |                             | Current highest bid or fixed price.              |
| `buy_now_price` | `DECIMAL(10, 2)`              |                                 |                             | Buy Now price, if available.                     |
| `shipping_cost` | `DECIMAL(10, 2)`              |                                 |                             | Shipping cost, if available.                     |
| `image_urls`    | `JSONB`                       |                                 | `'[]'::jsonb`               | List of image URLs for the auction.              |
| `start_time`    | `TIMESTAMP WITH TIME ZONE`    | `NOT NULL`                      |                             | Auction start time.                              |
| `end_time`      | `TIMESTAMP WITH TIME ZONE`    | `NOT NULL`                      |                             | Auction end time.                                |
| `url`           | `TEXT`                        | `NOT NULL`                      |                             | URL to the auction page on Tradera.              |
| `bid_count`     | `INTEGER`                     |                                 | `0`                         | Number of bids placed.                           |
| `status`        | `TEXT`                        |                                 | `'active'`                  | Status of the auction (e.g., active, ended).     |
| `script_id`     | `INTEGER`                     | `REFERENCES search_scripts(id) ON DELETE SET NULL` |                             | Optional foreign key linking to the script that found this auction. |
| `created_at`    | `TIMESTAMP WITH TIME ZONE`    |                                 | `NOW()`                     | Timestamp when the auction was added to DB.      |
| `updated_at`    | `TIMESTAMP WITH TIME ZONE`    |                                 | `NOW()`                     | Timestamp when the auction was last updated in DB. |

### `bid_configs`

Stores user configurations for automatic bidding on specific auctions.

| Column                   | Type                          | Constraints                               | Default         | Description                                       |
|--------------------------|-------------------------------|-------------------------------------------|-----------------|---------------------------------------------------|
| `id`                     | `SERIAL`                      | `PRIMARY KEY`                             | Auto-incrementing | Internal bid configuration ID.                    |
| `auction_id`             | `INTEGER`                     | `REFERENCES auctions(id) ON DELETE CASCADE` |                 | Foreign key linking to the `auctions` table.       |
| `user_id`                | `INTEGER`                     | `REFERENCES users(id) ON DELETE CASCADE`  |                 | Foreign key linking to the `users` table.         |
| `max_bid_amount`         | `DECIMAL(10, 2)`              | `NOT NULL`                                |                 | Maximum amount the user is willing to bid.        |
| `bid_seconds_before_end` | `INTEGER`                     |                                           | `5`             | How many seconds before auction end to place bid. |
| `is_active`              | `BOOLEAN`                     |                                           | `TRUE`          | Whether this auto-bid configuration is active.    |
| `status`                 | `TEXT`                        |                                           | `'pending'`     | Status of the bid config (e.g., pending, active). |
| `error_message`          | `TEXT`                        |                                           |                 | Stores error message if auto-bid fails.           |
| `created_at`             | `TIMESTAMP WITH TIME ZONE`    |                                           | `NOW()`         | Timestamp when the config was created.            |
| `updated_at`             | `TIMESTAMP WITH TIME ZONE`    |                                           | `NOW()`         | Timestamp when the config was last updated.       |

### `bids`

Stores records of bids placed (or attempted) by the system.

| Column             | Type                          | Constraints                               | Default           | Description                                            |
|--------------------|-------------------------------|-------------------------------------------|-------------------|--------------------------------------------------------|
| `id`               | `SERIAL`                      | `PRIMARY KEY`                             | Auto-incrementing | Internal bid record ID.                                |
| `auction_id`       | `INTEGER`                     | `REFERENCES auctions(id) ON DELETE CASCADE` |                   | Foreign key linking to the `auctions` table.            |
| `bid_config_id`    | `INTEGER`                     | `REFERENCES bid_configs(id) ON DELETE CASCADE` |                | Foreign key linking to the specific `bid_configs` entry. |
| `amount`           | `DECIMAL(10, 2)`              | `NOT NULL`                                |                   | The amount that was bid.                               |
| `status`           | `TEXT`                        |                                           | `'scheduled'`     | Status of the bid (e.g., scheduled, placed, failed).   |
| `placed_at`        | `TIMESTAMP WITH TIME ZONE`    |                                           |                   | Timestamp when the bid was actually placed.            |
| `response_status`  | `TEXT`                        |                                           |                   | Status received from Tradera API after placing bid.    |
| `response_message` | `TEXT`                        |                                           |                   | Message received from Tradera API after placing bid.   |
| `created_at`       | `TIMESTAMP WITH TIME ZONE`    |                                           | `NOW()`           | Timestamp when the bid record was created.             |
| `updated_at`       | `TIMESTAMP WITH TIME ZONE`    |                                           | `NOW()`           | Timestamp when the bid record was last updated.        |

## Relationships

- `users` (1) -> (N) `search_scripts` (`user_id`)
- `users` (1) -> (N) `bid_configs` (`user_id`)
- `search_scripts` (1) -> (N) `auctions` (`script_id`, nullable, ON DELETE SET NULL)
- `auctions` (1) -> (N) `bid_configs` (`auction_id`)
- `auctions` (1) -> (N) `bids` (`auction_id`)
- `bid_configs` (1) -> (N) `bids` (`bid_config_id`)

## Indexes

- `idx_auctions_end_time` ON `auctions(end_time)`
- `idx_auctions_status` ON `auctions(status)`
- `idx_search_scripts_user_id` ON `search_scripts(user_id)`
- `idx_bid_configs_auction_id` ON `bid_configs(auction_id)`
- `idx_bids_auction_id` ON `bids(auction_id)`

## Application Models (`models.py`)

Pydantic models defined in `backend/models.py` are used in the application layer (e.g., API request/response validation). These generally mirror the database schema but may have slight differences in data types (e.g., `float` in Pydantic vs `DECIMAL` in DB, `datetime` vs `TIMESTAMP WITH TIME ZONE`) or structure (e.g., `search_parameters` is a nested Pydantic model vs JSONB in DB).

## Entity-Relationship Diagram (ERD)

**(Subtask 7.4)** - An ERD should be created to visualize these tables and relationships.
