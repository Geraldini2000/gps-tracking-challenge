import socket
import time

HOST = "127.0.0.1"
PORT = 9000

# Pacote de Ping
PING_PACKET = bytes.fromhex("50F70A3F730150494E4773C4")

# Pacote de Localização (exemplo do protocolo)
LOCATION_PACKET = bytes.fromhex(
    "50F7"
    "0A3F73"
    "02"
    "5EFCF950"
    "156F"
    "017D7840"
    "00008CA0"
    "F800"
    "3C"
    "013026A1"
    "029E72BD"
    "73C4"
)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    print("Sending PING...")
    s.sendall(PING_PACKET)
    time.sleep(1)

    print("Sending LOCATION...")
    s.sendall(LOCATION_PACKET)
    time.sleep(1)
