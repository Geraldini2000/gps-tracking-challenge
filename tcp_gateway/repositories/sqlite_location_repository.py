import sqlite3
from pathlib import Path
from typing import Dict, Any, Optional
import json

from tcp_gateway.repositories.interfaces import LocationRepository


class SqliteLocationRepository(LocationRepository):
    """
    Repository SQLite para persistir a última localização por device_id.
    """

    def __init__(self, db_path: Optional[str] = None):
        if db_path:
            self.db_path = Path(db_path)
        else:
            # Root do projeto = pasta que contém tcp_gateway/
            project_root = Path(__file__).resolve().parents[2]
            self.db_path = project_root / "data" / "location.db"

        self.db_path.parent.mkdir(exist_ok=True)
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)
    
    def _init_db(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS locations (
                device_id TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
    
    def save_last_location(self, device_id: str, data: Dict[str, Any]) -> None:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO locations (device_id, data, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (device_id, json.dumps(data)))
        conn.commit()
        conn.close()
    
    def get_last_location(self, device_id: str) -> Optional[Dict[str, Any]]:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT data FROM locations WHERE device_id = ?
        """, (device_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return json.loads(result[0])
        return None
