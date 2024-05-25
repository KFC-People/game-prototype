from enum import Enum
import time
from dataclasses import dataclass

import arcade

from common.game_object import Component, GameObject


class State(Enum):
    IDLE = 1
    DRIVING = 2
    DYING = 3
    DEAD = 4


@dataclass
class KeyInput:
    key: str
    correct: bool
    time: float


class TypingComponent(Component):
    def __init__(
        self, parent: GameObject, window_seconds: int = 5, chars_per_word: int = 6
    ):
        super().__init__(parent)

        self.window_seconds = window_seconds
        self.chars_per_word = chars_per_word

        self.typing_history = []
        self.prompt = []

    def update(self, delta_time: float) -> None:
        self._clear_history()
        self.parent.speed_wpm = self._get_speed()

    def handle_char(self, char: str) -> None:
        self.typing_history.append(
            KeyInput(
                char,
                (char == self.prompt.pop(0)) if self.prompt else True,
                time.perf_counter(),
            )
        )
        self.parent.health -= 1

    def _get_speed(self) -> float:
        if not self.typing_history:
            return 0

        correct_chars = sum(key.correct for key in self.typing_history)
        speed_cps = correct_chars / self.window_seconds
        speed_wpm = speed_cps * 60 / self.chars_per_word

        return speed_wpm

    def _clear_history(self) -> None:
        current_time = time.perf_counter()

        self.typing_history = [
            key_input
            for key_input in self.typing_history
            if current_time - key_input.time < self.window_seconds
        ]


class MovementComponent(Component):
    def update(self, delta_time: float) -> None:
        if self.parent.health <= 0:
            if self.parent.state not in (
                State.DYING,
                State.DEAD,
            ):
                self.parent.state = State.DYING
                self.parent.change_x = 0

            return

        self.parent.change_x = self.parent.speed_wpm * 0.1

        if self.parent.change_x > 0:
            self.parent.state = State.DRIVING

        else:
            self.parent.state = State.IDLE


class GraphicsComponent(Component):
    def __init__(self, parent: GameObject):
        super().__init__(parent)

        main_path = "assets/auto"

        self.frames_per_sprite = 4
        self.sprite_count = 4

        spritesheet_args = (96, 96, 4, self.sprite_count)
        spritesheet_args = {
            "sprite_width": 96,
            "sprite_height": 96,
            "columns": 4,
            "count": self.sprite_count,
        }

        self.idle_texture = arcade.load_spritesheet(
            f"{main_path}/Idle.png", **spritesheet_args
        )
        self.drive_texture = arcade.load_spritesheet(
            f"{main_path}/Walk.png", **spritesheet_args
        )
        self.death_texture = arcade.load_spritesheet(
            f"{main_path}/Death.png",
            sprite_width=96,
            sprite_height=96,
            columns=6,
            count=6,
        )

        self.attack_right_texture = arcade.load_spritesheet(
            f"{main_path}/Attack3_1.png", **spritesheet_args
        )
        self.attack_up_texture = arcade.load_spritesheet(
            f"{main_path}/Attack3_2.png", **spritesheet_args
        )
        self.attack_down_texture = arcade.load_spritesheet(
            f"{main_path}/Attack3_3.png", **spritesheet_args
        )

        self.hurt_texture = arcade.load_spritesheet(
            f"{main_path}/Hurt.png",
            sprite_width=96,
            sprite_height=96,
            columns=2,
            count=2,
        )

        self.current_frame = 0

    def update(self, delta_time: float) -> None:
        self.current_frame += 1

        if self.parent.state == State.DYING:
            self.current_frame %= 6 * 12
            current_sprite = self.current_frame // 12

            if current_sprite == 5:
                self.parent.state = State.DEAD

            self.parent.texture = self.death_texture[current_sprite]
            return

        elif self.parent.state == State.DEAD:
            self.parent.texture = self.death_texture[5]
            return

        self.current_frame %= self.sprite_count * self.frames_per_sprite
        current_sprite = self.current_frame // self.frames_per_sprite

        match self.parent.state:
            case State.IDLE:
                self.parent.texture = self.idle_texture[current_sprite]

            case State.DRIVING:
                self.parent.texture = self.drive_texture[current_sprite]


class Vehicle(GameObject):
    def __init__(self):
        super().__init__()

        self.state = State.IDLE
        self.health = 100

        self.typing_component = TypingComponent(self)
        self.movement_component = MovementComponent(self)
        self.graphics_component = GraphicsComponent(self)

    def update(self, delta_time: float) -> None:
        self.typing_component.update(delta_time)
        self.movement_component.update(delta_time)
        self.graphics_component.update(delta_time)
