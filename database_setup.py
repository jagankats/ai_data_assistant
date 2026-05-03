import csv
from decimal import Decimal
from pathlib import Path

import psycopg2
from psycopg2 import sql

from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

DATA_FILE = Path(__file__).with_name("sap_sales_sample.csv")
SFDC_DATA_FILE = Path(__file__).with_name("sfdc_marketing_leads.csv")


def create_database():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname='postgres',
        user=DB_USER,
        password=DB_PASSWORD
    )
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(DB_NAME)))
        print(f"Database '{DB_NAME}' created.")
    else:
        print(f"Database '{DB_NAME}' already exists.")
    cursor.close()
    conn.close()


def create_tables():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales_orders (
            id SERIAL PRIMARY KEY,
            order_id TEXT NOT NULL,
            order_date DATE NOT NULL,
            customer_name TEXT NOT NULL,
            segment TEXT NOT NULL,
            country TEXT NOT NULL,
            region TEXT NOT NULL,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            sub_category TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            sales NUMERIC NOT NULL,
            discount NUMERIC NOT NULL,
            profit NUMERIC NOT NULL
        );
    """)

    cursor.execute("COMMENT ON COLUMN sales_orders.order_id IS 'External order identifier';")
    cursor.execute("COMMENT ON COLUMN sales_orders.order_date IS 'Date when the order was placed';")
    cursor.execute("COMMENT ON COLUMN sales_orders.customer_name IS 'Name of the customer who placed the order';")
    cursor.execute("COMMENT ON COLUMN sales_orders.segment IS 'Customer segment such as Consumer, Corporate, or Small Business';")
    cursor.execute("COMMENT ON COLUMN sales_orders.country IS 'Country where the order was shipped';")
    cursor.execute("COMMENT ON COLUMN sales_orders.region IS 'Sales region for the order';")
    cursor.execute("COMMENT ON COLUMN sales_orders.product_name IS 'Name of the product sold';")
    cursor.execute("COMMENT ON COLUMN sales_orders.category IS 'High-level product category';")
    cursor.execute("COMMENT ON COLUMN sales_orders.sub_category IS 'Sub-category of the product';")
    cursor.execute("COMMENT ON COLUMN sales_orders.quantity IS 'Number of units sold';")
    cursor.execute("COMMENT ON COLUMN sales_orders.sales IS 'Total sales amount for the order line';")
    cursor.execute("COMMENT ON COLUMN sales_orders.discount IS 'Discount applied to the order line';")
    cursor.execute("COMMENT ON COLUMN sales_orders.profit IS 'Profit earned from the order line';")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sfdc_leads (
            id SERIAL PRIMARY KEY,
            lead_id TEXT NOT NULL UNIQUE,
            created_date DATE NOT NULL,
            lead_source TEXT NOT NULL,
            lead_status TEXT NOT NULL,
            campaign_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            company TEXT,
            industry TEXT,
            score INTEGER,
            converted BOOLEAN NOT NULL
        );
    """)

    cursor.execute("COMMENT ON COLUMN sfdc_leads.lead_id IS 'Unique identifier for the lead in Salesforce';")
    cursor.execute("COMMENT ON COLUMN sfdc_leads.created_date IS 'Date when the lead was created';")
    cursor.execute("COMMENT ON COLUMN sfdc_leads.lead_source IS 'Source of the lead (Website, Social Media, Email, etc.)';")
    cursor.execute("COMMENT ON COLUMN sfdc_leads.lead_status IS 'Current status of the lead (Qualified, Contacted, Nurturing)';")
    cursor.execute("COMMENT ON COLUMN sfdc_leads.campaign_name IS 'Marketing campaign that generated this lead';")
    cursor.execute("COMMENT ON COLUMN sfdc_leads.email IS 'Email address of the lead';")
    cursor.execute("COMMENT ON COLUMN sfdc_leads.phone IS 'Phone number of the lead';")
    cursor.execute("COMMENT ON COLUMN sfdc_leads.company IS 'Company name of the lead';")
    cursor.execute("COMMENT ON COLUMN sfdc_leads.industry IS 'Industry sector of the lead company';")
    cursor.execute("COMMENT ON COLUMN sfdc_leads.score IS 'Lead scoring value indicating quality';")
    cursor.execute("COMMENT ON COLUMN sfdc_leads.converted IS 'Whether this lead has been converted to a customer';")

    conn.commit()
    cursor.close()
    conn.close()
    print("Tables created successfully.")

def insert_sample_data():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Cannot find dataset file: {DATA_FILE}")

    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sales_orders;")
    if cursor.fetchone()[0] > 0:
        print("Sample data already loaded. Skipping insertion.")
        cursor.close()
        conn.close()
        return

    with open(DATA_FILE, newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        rows = [
            (
                row['order_id'],
                row['order_date'],
                row['customer_name'],
                row['segment'],
                row['country'],
                row['region'],
                row['product_name'],
                row['category'],
                row['sub_category'],
                int(row['quantity']),
                Decimal(row['sales']),
                Decimal(row['discount']),
                Decimal(row['profit'])
            )
            for row in reader
        ]

    cursor.executemany(
        "INSERT INTO sales_orders (order_id, order_date, customer_name, segment, country, region, product_name, category, sub_category, quantity, sales, discount, profit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        rows
    )

def insert_sfdc_data():
    if not SFDC_DATA_FILE.exists():
        raise FileNotFoundError(f"Cannot find SFDC dataset file: {SFDC_DATA_FILE}")

    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sfdc_leads;")
    if cursor.fetchone()[0] > 0:
        print("SFDC marketing data already loaded. Skipping insertion.")
        cursor.close()
        conn.close()
        return

    with open(SFDC_DATA_FILE, newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        rows = [
            (
                row['lead_id'],
                row['created_date'],
                row['lead_source'],
                row['lead_status'],
                row['campaign_name'],
                row['email'],
                row['phone'],
                row['company'],
                row['industry'],
                int(row['score']) if row['score'] else None,
                bool(int(row['converted']))
            )
            for row in reader
        ]

    cursor.executemany(
        "INSERT INTO sfdc_leads (lead_id, created_date, lead_source, lead_status, campaign_name, email, phone, company, industry, score, converted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        rows
    )

    conn.commit()
    cursor.close()
    conn.close()
    print("SFDC marketing leads data inserted successfully.")

if __name__ == "__main__":
    create_database()
    create_tables()
    insert_sample_data()
    insert_sfdc_data()
