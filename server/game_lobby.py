import json
import socket
import time
from typing import NoReturn

from common.connection import Connection
from common.game import Game, PlayerType
from server.player import Player


class GameLobby:
    def __init__(self, host: str, port: int, update_rate: float = 1 / 10) -> None:
        self.update_rate = update_rate

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.bind((host, port))
        self.socket.listen(2)

        self.game = Game()
        self.players: dict[int, Player | None] = {
            PlayerType.DRIVER: None,
            PlayerType.GUNNER: None,
            # PlayerType.HEALER: None,
        }

    def run(self) -> NoReturn:
        while True:
            self.wait_for_players()
            self.game_loop()

    def wait_for_players(self) -> None:
        while not all(self.players.values()):
            self.broadcast({"event": "pause"})
            connection = Connection(self.socket.accept()[0])
            self.add_player(connection)

            time.sleep(0.1)

        self.broadcast({"event": "start"})

    def add_player(self, connection: Connection) -> None:
        player_type = [
            player_type
            for player_type, connection in self.players.items()
            if connection is None
        ][0]

        connection.send(json.dumps({"player_type": player_type}).encode())
        connection.on_message = lambda message: self.handle_input(player_type, message)
        connection.fork()

        self.players[player_type] = Player(connection)

    def handle_input(self, player_type: PlayerType, message: bytes) -> None:
        if not message:
            # TODO: player disconnected
            # self.players[player_type] = None
            return

        json_message = json.loads(message)

        if player_input := json_message.get("input"):
            self.game.handle_player_key(player_type, player_input)
            self.players[player_type].last_input = json_message

    def game_loop(self) -> None:
        current_time = time.time()
        accumulator = 0

        while all(self.players.values()):
            new_time = time.time()
            frame_time = new_time - current_time
            current_time = new_time

            accumulator += frame_time

            while accumulator >= self.update_rate:
                self.check_enemies()
                self.game.update(self.update_rate)
                self.broadcast({"state": self.game.get_state()})

                accumulator -= self.update_rate

    def check_enemies(self) -> None:
        for enemy in list(self.game.enemies.values()):
            if enemy.is_dead:
                del self.game.enemies[enemy.id]

        if len(self.game.enemies) < 5:
            self.game.spawn_random_enemy()

    def broadcast(self, event: dict) -> None:
        for role, player in self.players.items():
            if not player:
                continue

            try:
                message = json.dumps(
                    {
                        "timestamp": player.last_input.get("timestamp", time.time()),
                        **event,
                    }
                ).encode()

                player.connection.send(message)

            except ConnectionError:
                print("Connection with player lost")
