from collections import namedtuple
from threading import Thread
from typing import NoReturn

from common.utils import receive_message, send_message


class Connection(namedtuple("Connection", ["socket", "address"])):
    def send(self, data: bytes) -> None:
        send_message(self.socket, data)

    def run(self) -> NoReturn:
        try:
            while True:
                message = receive_message(self.socket)
                print(message)

        finally:
            self.socket.close()

    def fork(self) -> Thread:
        thread = Thread(target=self.run)
        thread.start()
        return thread
