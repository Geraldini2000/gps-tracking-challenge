from tcp_gateway.handlers.ping_handler import PingHandler
from tcp_gateway.handlers.location_handler import LocationHandler
from tcp_gateway.handlers.base import MessageHandler


class MessageHandlerFactory:

    _handlers = {
        0x01: PingHandler,
        0x02: LocationHandler,
    }

    @classmethod
    def create(cls, message_type: int) -> MessageHandler:
        handler_class = cls._handlers.get(message_type)

        if not handler_class:
            raise ValueError(f"No handler for message type {message_type}")

        return handler_class()
