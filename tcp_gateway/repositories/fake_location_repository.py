from typing import Dict, Any
from tcp_gateway.repositories.interfaces import LocationRepository


class FakeLocationRepository(LocationRepository):
    """Repositório fake para testes - não conecta ao banco real"""
    
    def __init__(self):
        self.saved_locations = {}
    
    def save_last_location(self, device_id: str, data: Dict[str, Any]) -> None:
        self.saved_locations[device_id] = data
    
    def get_last_location(self, device_id: str) -> Dict[str, Any]:
        return self.saved_locations.get(device_id, {})
