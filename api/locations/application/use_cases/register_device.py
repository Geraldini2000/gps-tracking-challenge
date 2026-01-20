from typing import Protocol
from ...domain.entities import UserDeviceEntity


class DeviceRepository(Protocol):
    def save(self, device: UserDeviceEntity) -> UserDeviceEntity:
        ...

    def exists_by_device_id(self, device_id: str) -> bool:
        ...


class RegisterDeviceUseCase:
    def __init__(self, device_repository: DeviceRepository):
        self.device_repository = device_repository

    def execute(self, user_id: int, device_id: str, device_name: str = None) -> UserDeviceEntity:

        if self.device_repository.exists_by_device_id(device_id):
            raise ValueError(f"Dispositivo {device_id} já está registrado")

   
        device = UserDeviceEntity(
            device_id=device_id,
            user_id=user_id,
            device_name=device_name or f"Device {device_id}"
        )

        return self.device_repository.save(device)
