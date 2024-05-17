import socket


def run():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address = ("127.0.0.1", 3000)

    s.sendto(b"username", address)
