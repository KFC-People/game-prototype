from collections import namedtuple
from threading import Thread
from typing import NoReturn

from common.utils import receive_message, send_message


class Connection(namedtuple("Connection", ["socket"])):
    def fork(self) -> Thread:
        thread = Thread(target=self.run)
        thread.start()
        return thread

    def run(self) -> NoReturn:
        try:
            while True:
                message = self.receive()
                self.on_message(message)
                print(message)

        finally:
            pass
            # self.socket.close()

    def receive(self) -> bytes:
        return receive_message(self.socket)

    def on_message(self, message: bytes) -> None:
        raise NotImplementedError

    def send(self, data: bytes) -> None:
        send_message(self.socket, data)
