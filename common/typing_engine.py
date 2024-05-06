import time
from dataclasses import dataclass

import lorem

TYPING_WINDOW_SECONDS = 3
CHARS_PER_WORD = 5


@dataclass
class KeyInput:
    key: str
    correct: bool
    time: float


class TypingEngine:
    def __init__(self):
        self.speed_cps = 0.0
        self.speed_wpm = 0.0

        self.typing_history = []
        self.prompt = self.generate_prompt()

    def generate_prompt(
        self,
    ) -> list[str]:
        return list(lorem.get_paragraph(1).lower())

    def update(self) -> float:
        if len(self.prompt) < self.speed_cps * TYPING_WINDOW_SECONDS:
            self.prompt.extend(self.generate_prompt())

        self._remove_old_chars()

        correct_symbols = sum(key_input.correct for key_input in self.typing_history)
        self.speed_cps = correct_symbols / TYPING_WINDOW_SECONDS
        self.speed_wpm = self.speed_cps * 60 / CHARS_PER_WORD

        return self.speed_wpm

    def _remove_old_chars(self) -> None:
        current_time = time.time()

        self.typing_history = [
            key_input
            for key_input in self.typing_history
            if current_time - key_input.time < TYPING_WINDOW_SECONDS
        ]

    def handle_char(self, char: str) -> None:
        self.typing_history.append(
            KeyInput(char, char == self.prompt.pop(0), time.time())
        )
