import time
from dataclasses import dataclass
from enum import Enum, auto

import arcade
from pymunk import Vec2d

from common.game_object import (
    BaseGraphicsComponent,
    BaseMovementComponent,
    Component,
    GameObject,
)
from common.utils import map_exponential


class State(Enum):
    IDLE = auto()
    DRIVING = auto()
    DYING = auto()
    DEAD = auto()


@dataclass
class KeyInput:
    key: str
    correct: bool
    time: float


class TypingComponent(Component):
    def __init__(
        self, parent: GameObject, window_seconds: int = 5, chars_per_word: int = 6
    ) -> None:
        super().__init__(parent)

        self.window_seconds = window_seconds
        self.chars_per_word = chars_per_word

        self.typing_history = []
        self.prompt = []
        self.prompt = list(
            "hello world lorem ipsum dolor sit amet consectetur adipiscing elit "
        )
        self.prompt += list(
            "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua "
        )
        self.prompt += list(
            "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat "
        )
        self.prompt += list(
            "duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur "
        )
        self.prompt += list(
            "excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum "
        )

        self.speed_wpm = 0
        self.accuracy = 0

    def update(self, delta_time: float) -> None:
        self._clear_history()
        self.speed_wpm, self.accuracy = self._get_stats()

    def handle_char(self, char: str) -> None:
        if not self.prompt:
            # TODO: renew prompt
            return

        # ignore spaces between words
        if char != " " and self.prompt and self.prompt[0] == " ":
            self.prompt.pop(0)

        self.typing_history.append(
            KeyInput(char, char == self.prompt.pop(0), time.perf_counter())
        )

    def _get_stats(self) -> tuple[float, float]:
        if not self.typing_history:
            return 0, 0

        correct_chars = sum(key.correct for key in self.typing_history)
        accuracy = correct_chars / len(self.typing_history)

        speed_cps = correct_chars / self.window_seconds
        speed_wpm = speed_cps * 60 / self.chars_per_word

        return speed_wpm, accuracy

    def _clear_history(self) -> None:
        current_time = time.perf_counter()

        self.typing_history = [
            key_input
            for key_input in self.typing_history
            if current_time - key_input.time < self.window_seconds
        ]


class MovementComponent(BaseMovementComponent):
    def update(self, delta_time: float) -> None:
        if self.parent.state in {State.DYING, State.DEAD}:
            self.acceleration -= self.velocity

        else:
            self.acceleration += Vec2d(1, 0) * self.parent.typing_speed
            self.acceleration -= self.velocity * 0.4

        self.velocity += self.acceleration * delta_time
        self.position += self.velocity * delta_time

        self.acceleration = Vec2d.zero()


class GraphicsComponent(BaseGraphicsComponent):
    def __init__(self, parent: GameObject, **kwargs) -> None:
        super().__init__(parent, **kwargs)

        main_path = "assets/auto"

        self.frames_per_sprite = 12
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
        self.position = self.parent.position
        self.current_frame += 1

        if self.parent.state == State.DYING:
            self.current_frame %= 6 * 12
            current_sprite = self.current_frame // 12

            if current_sprite == 5:
                self.parent.state = State.DEAD

            self.texture = self.death_texture[current_sprite]
            return

        elif self.parent.state == State.DEAD:
            self.texture = self.death_texture[-1]
            return

        self.current_frame %= self.sprite_count * self.frames_per_sprite
        current_sprite = self.current_frame // self.frames_per_sprite

        match self.parent.state:
            case State.IDLE:
                self.texture = self.idle_texture[current_sprite]

            case State.DRIVING:
                self.texture = self.drive_texture[current_sprite]


class Vehicle(GameObject):
    def __init__(
        self,
        initial_position: Vec2d = Vec2d.zero(),
        mass: float = 1.0,
        scale: float = 1.0,
    ) -> None:
        super().__init__()

        self.state = State.IDLE
        self.health = 100

        self.typing_component = TypingComponent(self)
        self.movement_component = MovementComponent(self, mass=mass)
        self.graphics_component = GraphicsComponent(
            self, initial_position=initial_position, scale=scale
        )

    def update(self, delta_time: float) -> None:
        if self.state == State.IDLE:
            if self.velocity.length > 0:
                self.state = State.DRIVING

        if self.state == State.DRIVING:
            if self.velocity.length > 1:
                frames_per_sprite = map_exponential(
                    self.velocity.length,
                    in_min=1,
                    in_max=200,
                    out_min=1,
                    out_max=12,
                    alpha=-2,
                )

                self.graphics_component.frames_per_sprite = int(frames_per_sprite)

            elif self.velocity.length <= 1:
                self.graphics_component.frames_per_sprite = 24
                self.state = State.IDLE

        if self.state != State.DEAD:
            if self.health <= 0:
                self.state = State.DYING

        self.typing_component.update(delta_time)
        self.movement_component.update(delta_time)
        self.graphics_component.update(delta_time)

    def handle_char(self, char: str) -> None:
        self.typing_component.handle_char(char)

    def draw(self) -> None:
        self.graphics_component.draw()

    @property
    def position(self) -> Vec2d:
        return self.movement_component.position

    @property
    def velocity(self) -> Vec2d:
        return self.movement_component.velocity

    @property
    def typing_speed(self) -> float:
        return self.typing_component.speed_wpm

    @property
    def prompt(self) -> list[str]:
        return "".join(self.typing_component.prompt)
