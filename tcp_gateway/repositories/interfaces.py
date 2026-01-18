from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class LocationRepository(ABC):
    @abstractmethod
    def save_last_location(self, device_id: str, data: Dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_last_location(self, device_id: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError
