import math
import struct
from socket import socket as _socket


def map_exponential(
    value: float,
    in_min: float,
    in_max: float,
    out_min: float,
    out_max: float,
    alpha: float = 1,
) -> float:
    x_normal = (value - in_min) / (in_max - in_min)
    y_normal = math.exp(x_normal * alpha)

    return y_normal * (out_max - out_min) + out_min


def receive_bytes(socket: _socket, packet_length: int) -> bytes:
    data = b""

    while len(data) < packet_length:
        block = socket.recv(packet_length - len(data))

        if not block:
            return None

        data += block

    return data


def parse_header(header: bytes) -> int:
    return struct.unpack("!I", header)[0]


def format_header(data: bytes) -> bytes:
    return struct.pack("!I", len(data))


def receive_message(socket: _socket) -> bytes:
    header = receive_bytes(socket, 4)

    if not header:
        return None

    length = parse_header(header)
    return receive_bytes(socket, length)


def send_message(socket: _socket, data: bytes) -> None:
    header = format_header(data)
    socket.sendall(header + data)
