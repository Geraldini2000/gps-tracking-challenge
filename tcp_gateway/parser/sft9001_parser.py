from tcp_gateway.parser.base import PacketParser
from tcp_gateway.dto.location_packet import LocationPacket


class SFT9001ParserError(ValueError):
    pass


class SFT9001Parser(PacketParser):
    HEADER = b"\x50\xF7"
    FOOTER = b"\x73\xC4"

    MSG_PING = 0x01
    MSG_LOCATION = 0x02

    def parse(self, payload: bytes):
        # Validação inicial do protocolo:
        # Todo pacote válido DEVE começar com o header fixo
        if not payload.startswith(self.HEADER):
            raise SFT9001ParserError("Invalid header")

        # Todo pacote válido DEVE terminar com o footer fixo 
        if not payload.endswith(self.FOOTER):
            raise SFT9001ParserError("Invalid footer")

        # Remove header (2 bytes) e footer (2 bytes),
        # sobrando apenas o conteúdo útil do pacote
        content = payload[2:-2]

        # - 3 bytes: device_id
        # - 1 byte : tipo da mensagem
        # - N bytes: dados (dependem do tipo)
        device_id_bytes = content[0:3]
        message_type = content[3]
        data = content[4:]

        device_id = device_id_bytes.hex().upper()

        if message_type == self.MSG_LOCATION:
            return self._parse_location(device_id, message_type, data)

        if message_type == self.MSG_PING:
            return {
                "device_id": device_id,
                "message_type": message_type,
            }

        # Caso o tipo não seja reconhecido, o pacote é rejeitado.
        raise SFT9001ParserError(f"Unsupported message type: {message_type}")

    def _parse_location(self, device_id: str, message_type: int, data: bytes) -> LocationPacket:
  
        # O payload de localização deve ter exatamente 25 bytes*****
        if len(data) != 25:
            raise SFT9001ParserError("Invalid location payload size")

        # 4 bytes - Timestamp
        timestamp = int.from_bytes(data[0:4], "big")
        # 2 bytes - Direção
        direction_raw = int.from_bytes(data[4:6], "big")
        direction = direction_raw / 100

        # 4 bytes - Hodômetro
        odometer = int.from_bytes(data[6:10], "big")
        # 4 bytes - Horímetro
        hourmeter = int.from_bytes(data[10:14], "big")
        # 2 bytes - Composição de flags
        composition = int.from_bytes(data[14:16], "big")

        # Interpretação dos bits mais significativos, conforme protocolo:
        gps_fixed = bool(composition & (1 << 15))
        gps_historical = bool(composition & (1 << 14))
        ignition_on = bool(composition & (1 << 13))
        lat_negative = bool(composition & (1 << 12))
        lon_negative = bool(composition & (1 << 11))

        # 1 byte - Velocidade
        speed = data[16]

        # 4 bytes - Latitude
        latitude = int.from_bytes(data[17:21], "big") / 1_000_000
        longitude = int.from_bytes(data[21:25], "big") / 1_000_000

        # Interpretação dos sinais de latitude e longitude
        if lat_negative:
            latitude *= -1

        if lon_negative:
            longitude *= -1

        return LocationPacket(
            device_id=device_id,
            message_type=message_type,
            timestamp=timestamp,
            direction=direction,
            odometer_m=odometer,
            hourmeter_min=hourmeter,
            gps_fixed=gps_fixed,
            gps_historical=gps_historical,
            ignition_on=ignition_on,
            latitude=latitude,
            longitude=longitude,
            speed_kmh=speed,
        )
