import json
import queue
import socket

from server.game_state import GameState


class PacketType:
    GET_FREE_ROLES = "get_free_roles"
    CONNECT = "connect"
    INPUT = "input"


class NetworkManager:
    def __init__(self, game_state: GameState, event_queue: queue.Queue):
        self.game_state = game_state
        self.event_queue = event_queue

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((socket.gethostname(), 1234))

        self.packet_handlers = {
            # PacketType.GET_FREE_ROLES: self.get_free_roles,
            PacketType.CONNECT: self.handle_connect,
            PacketType.INPUT: self.handle_input,
        }

    def listen(self):
        while True:
            data, address = self.socket.recvfrom(1470)
            self.handle_packet(json.loads(data.decode("utf-8")), address)

    def handle_packet(self, data: dict, address: tuple):
        self.packet_handlers[data["action"]](data, address)

    def handle_connect(self, data: dict, address: tuple):
        pass

    def handle_input(self, data: dict, *_):
        self.queue.put(data)
