import asyncio
import logging

from tcp_gateway.decoder.hex_decoder import HexDecoder, HexDecoderError
from tcp_gateway.parser.sft9001_parser import SFT9001Parser, SFT9001ParserError
from tcp_gateway.factory.message_handler_factory import MessageHandlerFactory
from tcp_gateway.protocol.ping_ack import build_ping_ack

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TcpGatewayServer:

    def __init__(self, host: str = "0.0.0.0", port: int = 9000):
        self.host = host
        self.port = port
        self.parser = SFT9001Parser()

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        peer = writer.get_extra_info("peername")
        logger.info("Client connected: %s", peer)

        try:
            while True:
                raw = await reader.read(1024)
                if not raw:
                    break

                try:
                    payload = HexDecoder.decode(raw)
                except HexDecoderError:
                    logger.warning("Failed to decode hex from %s", peer)
                    payload = raw

                try:
                    packet = self.parser.parse(payload)
                except SFT9001ParserError as exc:
                    logger.warning("Invalid packet from %s: %s", peer, exc)
                    continue

                handler = MessageHandlerFactory.create(packet["message_type"] if isinstance(packet, dict) else packet.message_type)
                result = handler.handle(packet)

                if isinstance(result, dict) and result.get("type") == "PING":
                    ack = build_ping_ack()
                    writer.write(ack)
                    await writer.drain()

                if not (isinstance(result, dict) and result.get("type") == "PING"):
                    logger.info("Processed packet: %s", result)

        except asyncio.CancelledError:
            logger.info("Connection cancelled: %s", peer)
        finally:
            try:
                writer.close()
            except Exception:
                pass

            logger.info("Client disconnected: %s", peer)


    async def start(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        logger.info("TCP Gateway listening on %s:%s", self.host, self.port)

        async with server:
            await server.serve_forever()


def main():
    gateway = TcpGatewayServer()
    asyncio.run(gateway.start())


if __name__ == "__main__":
    main()
