import sqlite3
from pathlib import Path

DB_PATH = Path("data/location.db")
DB_PATH.parent.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS last_location (
    device_id TEXT PRIMARY KEY,
    timestamp INTEGER,
    latitude REAL,
    longitude REAL,
    speed_kmh INTEGER,
    ignition_on INTEGER,
    gps_fixed INTEGER,
    gps_historical INTEGER
)
""")

conn.commit()
conn.close()

print("Database initialized.")
