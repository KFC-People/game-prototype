import socket
import time
from typing import NoReturn

from common.game import Game
from server.connection import Connection


class GameLobby:
    def __init__(
        self,
        host: str,
        port: int,
        backlog: int = 3,
        is_blocking: bool = True,
        update_rate: float = 1 / 60,
    ) -> None:
        self.update_rate = update_rate

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.backlog = backlog

        self.socket.setblocking(is_blocking)
        self.socket.bind((host, port))
        self.socket.listen(backlog)

        self.players = []
        self.game = Game()

    def run(self) -> NoReturn:
        while True:
            self.wait_for_players()
            self.game_loop()

    def wait_for_players(self) -> None:
        while len(self.players) < self.backlog:
            connection = Connection(*self.socket.accept())
            connection.fork()

            self.add_player(connection)

    def add_player(self, connection: Connection) -> None:
        connection.send(b"welcome")
        self.players.append(connection)

    def game_loop(self) -> None:
        current_time = time.perf_counter()
        accumulator = 0

        while len(self.players) == self.backlog:
            new_time = time.perf_counter()
            frame_time = new_time - current_time
            current_time = new_time

            accumulator += frame_time

            while accumulator >= self.update_rate:
                self.game.update(self.update_rate)
                accumulator -= self.update_rate
