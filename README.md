# POS Data Modelling

A sample project for simulating and modeling retail point-of-sale (POS) data. It generates synthetic data for stores, products, customers, transactions, and transaction items, and loads it into a PostgreSQL database for analytics and development purposes.

## Features

- SQL schema for a retail transaction system (`database.sql`)
- Python script to generate realistic fake data (`datageneration.py`)
- Uses [Faker](https://faker.readthedocs.io/) for data generation
- Supports PostgreSQL as the backend database

## Technologies

- Python 3.9+
- PostgreSQL
- psycopg2
- Faker

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Lucasblld/POS_data_modelling.git
   cd POS_data_modelling

2. **Create and activate a virtual environment:**
    ```bash
    python3.9 -m venv env
    source env/bin/activate

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt

4. **Set environment variables for database connection:**
    ```bash
    export HOST=localhost
    export DB=your_database_name
    export USER=your_db_user
    export PASSWORD=your_db_password

## Database Initialization

1. **Create a PostgreSQL database if not already present.**
2. **Run the schema script to create tables and indexes:**
   ```bash
    psql -U $USER -d $DB -f database.sql

## Data Generation

Run the data generation script to populate the database with synthetic data:
    ```bash
    python datageneration.py