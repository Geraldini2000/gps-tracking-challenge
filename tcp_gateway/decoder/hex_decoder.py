from typing import Union


class HexDecoderError(ValueError):
    ''' Invalid hexadecimal '''
    pass


class HexDecoder:
    @staticmethod
    def decode(payload: Union[str, bytes]) -> bytes:
        ''' Valid hexadecimal '''
        if isinstance(payload, bytes):
            try:
                payload = payload.decode("ascii")
            except UnicodeDecodeError as exc:
                raise HexDecoderError("Payload bytes must be ASCII hex.") from exc

        if not isinstance(payload, str):
            raise HexDecoderError("Payload must be a hex string or ASCII bytes.")

        payload = payload.strip().replace(" ", "")

        if len(payload) % 2 != 0:
            raise HexDecoderError("Hex payload must have even length.")

        try:
            return bytes.fromhex(payload)
        except ValueError as exc:
            raise HexDecoderError("Invalid hexadecimal payload.") from exc
