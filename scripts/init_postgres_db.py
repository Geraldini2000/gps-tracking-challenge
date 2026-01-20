import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS last_location (
    device_id TEXT PRIMARY KEY,
    timestamp BIGINT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    speed_kmh INTEGER,
    ignition_on BOOLEAN,
    gps_fixed BOOLEAN,
    gps_historical BOOLEAN
)
""")

conn.commit()
cursor.close()
conn.close()

print("Postgres database initialized.")
