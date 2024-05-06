import time

TYPING_WINDOW_SECONDS = 3
CHARS_PER_WORD = 5


class TypingEngine:
    def __init__(self):
        self.typing_buffer = ""
        self.typing_history = []

        self.game_start_time = time.time()

    def update(self) -> float:
        self._remove_old_chars()

        speed_cps = len(self.typing_history) / TYPING_WINDOW_SECONDS
        speed_wpm = speed_cps * 60 / CHARS_PER_WORD

        return speed_wpm

    def _remove_old_chars(self) -> None:
        current_time = time.time()

        self.typing_history = [
            time
            for time in self.typing_history
            if current_time - time < TYPING_WINDOW_SECONDS
        ]

    def handle_char(self, char: str) -> None:
        self.typing_buffer += char
        self.typing_history.append(time.time())
