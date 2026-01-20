from typing import Protocol, List
from ...domain.entities import UserDeviceEntity


class DeviceRepository(Protocol):
    def find_by_user_id(self, user_id: int) -> List[UserDeviceEntity]:
        ...


class GetUserDevicesUseCase:

    def __init__(self, device_repository: DeviceRepository):
        self.device_repository = device_repository

    def execute(self, user_id: int) -> List[UserDeviceEntity]:
        return self.device_repository.find_by_user_id(user_id)
