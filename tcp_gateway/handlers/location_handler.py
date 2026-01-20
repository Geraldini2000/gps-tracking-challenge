from tcp_gateway.handlers.base import MessageHandler
from tcp_gateway.dto.location_packet import LocationPacket
from tcp_gateway.repositories.interfaces import LocationRepository


class LocationHandler(MessageHandler):

    def __init__(self, repository: LocationRepository):
        self._repository = repository

    def handle(self, packet: LocationPacket) -> dict:
        data = {
            "device_id": packet.device_id,
            "timestamp": packet.timestamp,
            "latitude": packet.latitude,
            "longitude": packet.longitude,
            "speed_kmh": packet.speed_kmh,
            "ignition_on": packet.ignition_on,
            "gps_fixed": packet.gps_fixed,
            "gps_historical": packet.gps_historical,
        }

        self._repository.save_last_location(packet.device_id, data)
        return data
