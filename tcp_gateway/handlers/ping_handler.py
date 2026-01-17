from tcp_gateway.handlers.base import MessageHandler


class PingHandler(MessageHandler):

    def handle(self, packet: dict) -> dict:
        return {
            "device_id": packet["device_id"],
            "type": "PING",
        }
