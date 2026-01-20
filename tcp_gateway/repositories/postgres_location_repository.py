import psycopg2
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

from tcp_gateway.repositories.interfaces import LocationRepository

load_dotenv()

class PostgresLocationRepository(LocationRepository):

    def __init__(
        self,
        host=None,
        port=None,
        dbname=None,
        user=None,
        password=None,
    ):
        self._conn_params = {
            "host": host or os.getenv('POSTGRES_HOST'),
            "port": port or os.getenv('POSTGRES_PORT'),
            "dbname": dbname or os.getenv('POSTGRES_DB'),
            "user": user or os.getenv('POSTGRES_USER'),
            "password": password or os.getenv('POSTGRES_PASSWORD'),
        }

    def _connect(self):
        return psycopg2.connect(**self._conn_params)

    def save_last_location(self, device_id: str, data: Dict[str, Any]) -> None:
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO last_location (
            device_id, timestamp, latitude, longitude,
            speed_kmh, ignition_on, gps_fixed, gps_historical
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (device_id) DO UPDATE SET
            timestamp = EXCLUDED.timestamp,
            latitude = EXCLUDED.latitude,
            longitude = EXCLUDED.longitude,
            speed_kmh = EXCLUDED.speed_kmh,
            ignition_on = EXCLUDED.ignition_on,
            gps_fixed = EXCLUDED.gps_fixed,
            gps_historical = EXCLUDED.gps_historical
        """, (
            device_id,
            data["timestamp"],
            data["latitude"],
            data["longitude"],
            data["speed_kmh"],
            data["ignition_on"],
            data["gps_fixed"],
            data["gps_historical"],
        ))

        conn.commit()
        cursor.close()
        conn.close()

    def get_last_location(self, device_id: str) -> Optional[Dict[str, Any]]:
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT device_id, timestamp, latitude, longitude,
               speed_kmh, ignition_on, gps_fixed, gps_historical
        FROM last_location
        WHERE device_id = %s
        """, (device_id,))

        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if not row:
            return None

        return {
            "device_id": row[0],
            "timestamp": row[1],
            "latitude": row[2],
            "longitude": row[3],
            "speed_kmh": row[4],
            "ignition_on": row[5],
            "gps_fixed": row[6],
            "gps_historical": row[7],
        }
