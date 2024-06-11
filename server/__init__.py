from server.game_lobby import GameLobby


def run(update_rate: float = 1 / 10) -> None:
    GameLobby(host="127.0.0.1", port=1234, update_rate=update_rate).run()
