from abc import ABC, abstractmethod
from typing import Any


class MessageHandler(ABC):
    @abstractmethod
    def handle(self, packet: Any) -> Any:
        raise NotImplementedError
