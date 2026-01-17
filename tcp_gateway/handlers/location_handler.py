from tcp_gateway.handlers.base import MessageHandler
from tcp_gateway.dto.location_packet import LocationPacket


class LocationHandler(MessageHandler):

    def handle(self, packet: LocationPacket) -> dict:
        return {
            "device_id": packet.device_id,
            "timestamp": packet.timestamp,
            "latitude": packet.latitude,
            "longitude": packet.longitude,
            "speed_kmh": packet.speed_kmh,
            "ignition_on": packet.ignition_on,
            "gps_fixed": packet.gps_fixed,
            "gps_historical": packet.gps_historical,
        }
