from common.connection import Connection


class Player:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection
        self.last_input = {}
