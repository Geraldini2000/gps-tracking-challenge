from typing import Dict, Any, Optional
from threading import Lock

from tcp_gateway.repositories.interfaces import LocationRepository


class InMemoryLocationRepository(LocationRepository):

    def __init__(self):
        self._storage: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()

    def save_last_location(self, device_id: str, data: Dict[str, Any]) -> None:
        with self._lock:
            self._storage[device_id] = data

    def get_last_location(self, device_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            return self._storage.get(device_id)
