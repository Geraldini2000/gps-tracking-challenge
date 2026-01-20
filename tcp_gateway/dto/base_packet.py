from dataclasses import dataclass


@dataclass(frozen=True)
class BasePacket:
    device_id: str
    message_type: int
