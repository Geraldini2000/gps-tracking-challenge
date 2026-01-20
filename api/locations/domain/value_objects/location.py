from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Location:
    device_id: str
    timestamp: int
    latitude: float
    longitude: float
    speed_kmh: int
    ignition_on: bool
    gps_fixed: bool
    gps_historical: bool

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if not -90 <= self.latitude <= 90:
            raise ValueError("Latitude deve estar entre -90 e 90")
        
        if not -180 <= self.longitude <= 180:
            raise ValueError("Longitude deve estar entre -180 e 180")
        
        if self.speed_kmh < 0:
            raise ValueError("Velocidade não pode ser negativa")
        
        if self.timestamp <= 0:
            raise ValueError("Timestamp deve ser positivo")

    def is_moving(self) -> bool:
        return self.speed_kmh > 0 and self.ignition_on

    def is_valid_gps(self) -> bool:
        return self.gps_fixed and not self.gps_historical
