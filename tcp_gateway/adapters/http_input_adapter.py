from tcp_gateway.decoder.hex_decoder import HexDecoder
from tcp_gateway.parser.sft9001_parser import SFT9001Parser
from tcp_gateway.factory.message_handler_factory import MessageHandlerFactory


class HttpInputAdapterError(ValueError):
    pass


class HttpInputAdapter:

    def __init__(self):
        self._decoder = HexDecoder()
        self._parser = SFT9001Parser()

    def process(self, hex_payload: str) -> dict:
        if not hex_payload:
            raise HttpInputAdapterError("Payload is required")

        try:
            raw_bytes = self._decoder.decode(hex_payload)
        except Exception as exc:
            raise HttpInputAdapterError("Invalid hex payload") from exc

        packet = self._parser.parse(raw_bytes)

        handler = MessageHandlerFactory.create(packet.message_type)
        return handler.handle(packet)

