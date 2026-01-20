from typing import List
from ..entities import UserDeviceEntity


class DeviceAuthorizationService:

    @staticmethod
    def can_access_device(user_id: int, device: UserDeviceEntity) -> bool:
        return device.belongs_to_user(user_id)

    @staticmethod
    def filter_user_devices(user_id: int, devices: List[UserDeviceEntity]) -> List[UserDeviceEntity]:
        return [device for device in devices if device.belongs_to_user(user_id)]
