from dataclasses import dataclass
from .base_packet import BasePacket


@dataclass(frozen=True)
class LocationPacket(BasePacket):
    timestamp: int
    direction: float
    odometer_m: int
    hourmeter_min: int
    gps_fixed: bool
    gps_historical: bool
    ignition_on: bool
    latitude: float
    longitude: float
    speed_kmh: int
