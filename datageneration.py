import os
import sys
import random
import uuid

import psycopg2
from faker import Faker

# Set the random seed for reproducibility
SEED = 42
random.seed(SEED)
Faker.seed(SEED)

fake = Faker()

# --- Database connection ---
# Read database connection parameters from environment variables
host = os.environ["HOST"]
db = os.environ["DB"]
user = os.environ["USER"]
password = os.environ["PASSWORD"]

try:
    # Establish connection to the PostgreSQL database
    conn = psycopg2.connect(host=host, database=db, user=user, password=password)
except psycopg2.OperationalError as e:
    print(f"Database connection failed: {e}")
    sys.exit(1)

cur = conn.cursor()

# Parameters for data generation
NUM_STORES = 10
NUM_CUSTOMER = 200
NUM_PRODUCTS = 75
NUM_TRANSACTIONS = 10000
categories = ["Hyper", "Super", "Express"]
shared_cities = [fake.city() for _ in range(3)]
shared_states = [fake.state() for _ in range(3)]

# -- stores generation --
stores = []

for i in range(NUM_STORES):
    # Generate a unique store ID using UUID5
    store_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"store-{i}"))
    store_type = random.choices(categories)[0]
    # 65% chance to use a shared city/state for realism
    if random.random() < 0.35:
        city = random.choice(shared_cities)
        region = random.choice(shared_states)
    else:
        city = fake.city()
        region = fake.state()
    # Insert store record into the database
    cur.execute(
        """
        INSERT INTO stores (store_id, store_name, store_type, city, region)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (store_id) DO NOTHING
        """,
        (store_id, fake.company(), store_type, city, region),
    )
    stores.append(store_id)

# -- product generation
products = []
categories = ["Alimentaire", "Boissons", "Hygiene", "Maison", "Electronique"]

for i in range(NUM_PRODUCTS):
    # Generate a unique product ID using UUID5
    product_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"product-{i}"))
    # Insert product record into the database
    cur.execute(
        """
        INSERT INTO products (product_id, product_name, category, brand, ean)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (product_id) DO NOTHING
        """,
        (
            product_id,
            fake.word().capitalize(),
            random.choice(categories),
            fake.company(),
            fake.ean(length=13),
        ),
    )
    products.append(product_id)

# -- customer generation
customers = []
for i in range(NUM_CUSTOMER):
    # Generate a unique customer ID using UUID5
    customer_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"customer-{i}"))
    loyalty_card_random = random.choice([True, False])
    # Assign loyalty card and signup date to some customers
    if loyalty_card_random:
        signup_date = fake.date_between(start_date="-1y", end_date="today")
        loyalty_card = True
    else:
        signup_date = None
        loyalty_card = False
    # Insert customer record into the database
    cur.execute(
        """
        INSERT INTO customers (customer_id, signup_date, loyalty_card)
        VALUES (%s, %s, %s)
        ON CONFLICT (customer_id) DO NOTHING
        """,
        (customer_uuid, signup_date, loyalty_card),
    )
    customers.append(customer_uuid)

# Commit store, product, and customer records
conn.commit()

# -- transaction and transaction_item generation --
new = 0
for i in range(NUM_TRANSACTIONS):
    # Generate a unique transaction ID using UUID5
    transaction_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"transaction-{i}"))
    store_id = random.choice(stores)
    customer_id = random.choice(customers)
    transaction_timestamp = fake.date_time_between(start_date="-3M", end_date="now")
    payment_method = random.choice(["cash", "card", "check"])

    num_item = random.randint(1, 7)
    items_total = 0
    # Insert transaction record into the database
    cur.execute(
        """INSERT INTO transactions (transaction_id, store_id, customer_id, transaction_timestamp, payment_method)
        VALUES (%s,%s,%s,%s,%s)
        ON CONFLICT (transaction_id) DO NOTHING""",
        (transaction_id, store_id, customer_id, transaction_timestamp, payment_method),
    )

    for i in range(num_item):
        # Generate a unique transaction item ID using UUID5
        transaction_item_id = str(uuid.uuid4())
        product_id = random.choice(products)
        quantity = random.randint(1, 5)
        unit_price = round(random.uniform(1, 100), 2)
        is_promo = random.choices([True, False], weights=[0.2, 0.8])[0]
        promo_discount = round(unit_price * 0.2, 2) if is_promo else 0

        items_total += quantity * (unit_price - promo_discount)

        # Insert transaction item record into the database
        cur.execute(
            """INSERT INTO transaction_items (transaction_item_id,transaction_id, product_id,
             quantity, unit_price, is_promo, promo_discount)
             VALUES (%s,%s,%s,%s,%s,%s,%s)
             ON CONFLICT (transaction_item_id) DO NOTHING""",
            (
                transaction_item_id,
                transaction_id,
                product_id,
                quantity,
                unit_price,
                is_promo,
                promo_discount,
            ),
        )

    # Update the total amount for the transaction
    cur.execute(
        """UPDATE transactions SET total_amount=%s WHERE transaction_id=%s""",
        (items_total, transaction_id),
    )


# Commit all transaction and transaction item records
conn.commit()
cur.close()
conn.close()