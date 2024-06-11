import threading


class IDGenerator:
    _counter = 0
    _lock = threading.Lock()

    @classmethod
    def next_id(cls) -> int:
        with cls._lock:
            cls._counter += 1
            return cls._counter
