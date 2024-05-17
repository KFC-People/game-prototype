from queue import Queue
import time

from server.game_state import GameState
from server.network_manager import NetworkManager


class Physics:
    def __init__(
        self, game_state: GameState, event_queue: Queue, network_manager: NetworkManager
    ):
        self.is_running = True

        self.game_state = game_state
        self.event_queue = event_queue
        self.network_manager = network_manager

    def start(self):
        fps = 60

        current_time = time.time()
        fixed_dt = 1 / fps
        accumulator = 0

        while self.is_running:
            new_time = time.time()
            frame_time = new_time - current_time
            current_time = new_time

            accumulator += frame_time

            while accumulator >= fixed_dt:
                self.update(fixed_dt)
                accumulator -= fixed_dt

    def update(self, dt):
        pass
