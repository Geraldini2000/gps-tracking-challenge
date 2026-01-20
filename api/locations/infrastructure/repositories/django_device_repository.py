from typing import List, Optional
from ...domain.entities import UserDeviceEntity
from ...models import UserDevice


class DjangoDeviceRepository:


    def save(self, device: UserDeviceEntity) -> UserDeviceEntity:
        django_device, created = UserDevice.objects.get_or_create(
            device_id=device.device_id,
            defaults={
                'user_id': device.user_id,
                'device_name': device.device_name
            }
        )
        
        if not created and django_device.user_id != device.user_id:
            raise ValueError("Dispositivo já pertence a outro usuário")

        return self._to_entity(django_device)

    def find_by_device_id(self, device_id: str) -> Optional[UserDeviceEntity]:
        try:
            django_device = UserDevice.objects.get(device_id=device_id)
            return self._to_entity(django_device)
        except UserDevice.DoesNotExist:
            return None

    def find_by_user_id(self, user_id: int) -> List[UserDeviceEntity]:
        django_devices = UserDevice.objects.filter(user_id=user_id)
        return [self._to_entity(d) for d in django_devices]

    def exists_by_device_id(self, device_id: str) -> bool:
        return UserDevice.objects.filter(device_id=device_id).exists()

    @staticmethod
    def _to_entity(django_device: UserDevice) -> UserDeviceEntity:
        return UserDeviceEntity(
            id=django_device.id,
            device_id=django_device.device_id,
            user_id=django_device.user_id,
            device_name=django_device.device_name,
            created_at=django_device.created_at,
            updated_at=django_device.updated_at
        )
