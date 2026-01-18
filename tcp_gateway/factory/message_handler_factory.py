from tcp_gateway.handlers.ping_handler import PingHandler
from tcp_gateway.handlers.location_handler import LocationHandler
from tcp_gateway.handlers.base import MessageHandler
from tcp_gateway.repositories.in_memory_location_repository import InMemoryLocationRepository


class MessageHandlerFactory:

    _repository = InMemoryLocationRepository()

    _handlers = {
        0x01: PingHandler,
        0x02: LocationHandler,
    }

    @classmethod
    def create(cls, message_type: int) -> MessageHandler:
        handler_class = cls._handlers.get(message_type)

        if not handler_class:
            raise ValueError(f"No handler for message type {message_type}")

        if message_type == 0x02:
            return handler_class(cls._repository)

        return handler_class()
