from typing import Protocol, Optional
from ...domain.entities import UserDeviceEntity
from ...domain.value_objects import Location
from ...domain.services import DeviceAuthorizationService


class DeviceRepository(Protocol):
    def find_by_device_id(self, device_id: str) -> Optional[UserDeviceEntity]:
        ...


class LocationRepository(Protocol):
    def get_last_location(self, device_id: str) -> Optional[dict]:
        ...


class GetDeviceLocationUseCase:

    def __init__(
        self,
        device_repository: DeviceRepository,
        location_repository: LocationRepository,
        auth_service: DeviceAuthorizationService
    ):
        self.device_repository = device_repository
        self.location_repository = location_repository
        self.auth_service = auth_service

    def execute(self, user_id: int, device_id: str) -> Optional[dict]:
        device = self.device_repository.find_by_device_id(device_id)
        
        if not device:
            return None

        if not self.auth_service.can_access_device(user_id, device):
            raise PermissionError("Você não tem permissão para acessar este dispositivo")

        return self.location_repository.get_last_location(device_id)
