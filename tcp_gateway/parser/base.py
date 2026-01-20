from abc import ABC, abstractmethod


class PacketParser(ABC):
    @abstractmethod
    def parse(self, payload: bytes):
        raise NotImplementedError
