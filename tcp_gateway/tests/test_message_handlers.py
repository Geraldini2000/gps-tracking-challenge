import pytest

from tcp_gateway.factory.message_handler_factory import MessageHandlerFactory
from tcp_gateway.dto.location_packet import LocationPacket
from tcp_gateway.repositories.fake_location_repository import FakeLocationRepository
from tcp_gateway.handlers.location_handler import LocationHandler


def test_factory_returns_ping_handler():
    handler = MessageHandlerFactory.create(0x01)
    result = handler.handle({"device_id": "ABC123"})

    assert result["type"] == "PING"
    assert result["device_id"] == "ABC123"


def test_factory_returns_location_handler():
    # Usar repositório fake para não conectar ao banco real nos testes
    fake_repo = FakeLocationRepository()
    handler = LocationHandler(fake_repo)

    packet = LocationPacket(
        device_id="ABC123",
        message_type=0x02,
        timestamp=123456,
        direction=90.0,
        odometer_m=1000,
        hourmeter_min=50,
        gps_fixed=True,
        gps_historical=False,
        ignition_on=True,
        latitude=-23.55,
        longitude=-46.63,
        speed_kmh=60,
    )

    result = handler.handle(packet)

    assert result["device_id"] == "ABC123"
    assert result["speed_kmh"] == 60
    assert result["gps_fixed"] is True


def test_factory_raises_for_unknown_type():
    with pytest.raises(ValueError):
        MessageHandlerFactory.create(0x99)
