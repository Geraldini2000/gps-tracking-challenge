from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UserDeviceEntity:
    device_id: str
    user_id: int
    device_name: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if not self.device_id or len(self.device_id.strip()) == 0:
            raise ValueError("device_id não pode ser vazio")
        
        if not self.user_id or self.user_id <= 0:
            raise ValueError("user_id deve ser um número positivo")

    def update_name(self, new_name: str) -> None:
        if new_name and len(new_name.strip()) > 0:
            self.device_name = new_name.strip()

    def belongs_to_user(self, user_id: int) -> bool:

        return self.user_id == user_id
