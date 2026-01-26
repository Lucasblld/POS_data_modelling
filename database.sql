-- DATABASE INITIALISATION
-- This script creates tables and indexes for a retail transaction system.

-- STORES: Information about each store location.
CREATE TABLE stores(
    store_id uuid primary key, -- Unique store identifier
    store_name text not null,  -- Store name
    store_type text not null,  -- Store type: Hyper, Super, Express
    city text not null,        -- City where the store is located
    region text not null,      -- Region of the store
    created_at timestamp default now() -- Record creation timestamp
);

-- PRODUCTS: Details of products available in stores.
CREATE TABLE products(
    product_id uuid primary key, -- Unique product identifier
    product_name text not null,  -- Product name
    category text not null,      -- Product category
    brand text not null,         -- Brand name
    ean text unique,                        -- European Article Number (barcode)
    created_at timestamp default now() -- Record creation timestamp
);

-- CUSTOMERS: Customer profiles and loyalty information.
CREATE TABLE customers(
    customer_id uuid primary key, -- Unique customer identifier
    signup_date date,             -- Date of signup
    loyalty_card boolean default false -- Loyalty card status
);

-- TRANSACTIONS: Store purchase transactions.
CREATE TABLE transactions (
    transaction_id uuid primary key, -- Unique transaction identifier
    store_id uuid references stores(store_id), -- Store where transaction occurred
    customer_id uuid references customers(customer_id), -- Customer making the purchase
    transaction_timestamp timestamp not null, -- Date and time of transaction
    payment_method text,                      -- Payment method used
    total_amount numeric(10,2),               -- Total transaction amount
    created_at timestamp default now()         -- Record creation timestamp
);

-- TRANSACTION ITEMS: Items purchased in each transaction.
CREATE TABLE transaction_items (
    transaction_item_id uuid primary key, -- Unique item identifier
    transaction_id uuid references transactions(transaction_id), -- Related transaction
    product_id uuid references products(product_id),             -- Purchased product
    quantity integer not null check (quantity > 0),              -- Quantity bought
    unit_price numeric(10,2) not null check (unit_price >= 0),   -- Price per unit
    is_promo boolean default false,                              -- Was item on promotion
    promo_discount numeric(5,2),                                 -- Discount amount
    created_at timestamp default now()                           -- Record creation timestamp
);

-- Indexes for performance optimization
create index idx_transactions_timestamp on transactions(transaction_timestamp); -- Fast lookup by transaction date
create index idx_transaction_items_product on transaction_items(product_id);    -- Fast lookup by product
create index idx_transaction_items_transaction on transaction_items(transaction_id); -- Fast lookup by transaction