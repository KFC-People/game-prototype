from queue import Queue
from threading import Thread

from server.game_state import GameState
from server.network_manager import NetworkManager
from server.physics import Physics


class Server:
    def __init__(self):
        self.game_state = GameState()
        self.event_queue = Queue()

        self.network_manager = NetworkManager(self.game_state, self.event_queue)
        self.networking_thread = Thread(target=self.network_manager.listen)

        self.physics = Physics(self.game_state, self.event_queue, self.network_manager)
        self.physics_thread = Thread(target=self.physics.start)

    def start(self):
        self.networking_thread.start()
