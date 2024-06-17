from server.game_lobby import GameLobby


def run(update_rate: float = 1 / 10) -> None:
    GameLobby(host="0.0.0.0", port=1234, update_rate=update_rate).run()
