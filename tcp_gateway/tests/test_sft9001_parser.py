import pytest
from tcp_gateway.parser.sft9001_parser import SFT9001Parser


def test_parse_valid_location_packet():
    raw_hex = (
        "50F7"
        "0A3F73"
        "02"
        "5EFCF950"
        "156F"
        "017D7840"
        "00008CA0"
        "F800"
        "3C"
        "013026A1"
        "029E72BD"
        "73C4"
    )

    payload = bytes.fromhex(raw_hex)
    parser = SFT9001Parser()

    packet = parser.parse(payload)

    assert packet.device_id == "0A3F73"
    assert packet.message_type == 2
    assert packet.gps_fixed is True
    assert packet.gps_historical is True
    assert packet.ignition_on is True
    assert packet.speed_kmh == 60
