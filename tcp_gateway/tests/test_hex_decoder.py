import pytest

from tcp_gateway.decoder.hex_decoder import HexDecoder, HexDecoderError


def test_decode_valid_hex_string():
    result = HexDecoder.decode("50F773C4")
    assert result == b"\x50\xF7\x73\xC4"


def test_decode_valid_hex_with_spaces():
    result = HexDecoder.decode("50 F7 73 C4")
    assert result == b"\x50\xF7\x73\xC4"


def test_decode_valid_hex_bytes():
    result = HexDecoder.decode(b"50F773C4")
    assert result == b"\x50\xF7\x73\xC4"


def test_decode_invalid_length():
    with pytest.raises(HexDecoderError):
        HexDecoder.decode("50F773C")


def test_decode_invalid_characters():
    with pytest.raises(HexDecoderError):
        HexDecoder.decode("ZZZZ")


def test_decode_non_ascii_bytes():
    with pytest.raises(HexDecoderError):
        HexDecoder.decode(b"\xff\xff")
