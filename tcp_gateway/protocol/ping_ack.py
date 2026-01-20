def build_ping_ack() -> bytes:
    header = b"\x50\xF7"
    msg_type = b"\x01"
    data = b"PING"
    footer = b"\x73\xC4"
    return header + msg_type + data + footer
