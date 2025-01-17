import random
from enum import Enum, auto

from arcade import Texture
from pymunk import Vec2d
from random_word import RandomWords

from common.game_object import (
    BaseGraphicsComponent,
    BaseMovementComponent,
    Component,
    GameObject,
)
from common.sprite_cache import SpriteCache

word_generator = RandomWords()


class State(Enum):
    ACTIVE = auto()
    IDLE = auto()
    DYING = auto()
    DEAD = auto()


class TypingComponent(Component):
    def __init__(self, parent: GameObject) -> None:
        super().__init__(parent)

        self.prompt = list(word_generator.get_random_word().lower())

    def handle_char(self, char: str) -> None:
        if len(self.prompt) == 0:
            return

        if char == self.prompt[0]:
            self.prompt.pop(0)

    def get_state(self) -> dict:
        return {"prompt": self.prompt}

    def apply_state(self, state: dict) -> None:
        self.prompt = state.get("prompt", self.prompt)


class AIMovementComponent(BaseMovementComponent):
    def __init__(
        self, parent: GameObject, initial_position: Vec2d = Vec2d.zero()
    ) -> None:
        super().__init__(parent, initial_position=initial_position)

    def update(self, delta_time: float) -> None:
        if not self.parent.is_alive:
            self.acceleration += Vec2d(-0.1, -0.4) * self.mass

        if self.parent.state == State.ACTIVE:
            self.check_speed()
            self.check_borders()
            self.acceleration += Vec2d(random.randint(-5, 5), random.randint(-5, 5))

        self.velocity += self.acceleration
        self.position += self.velocity

        self.acceleration = Vec2d.zero()

    def check_speed(self) -> None:
        if self.velocity.length > 10:
            self.velocity = self.velocity.normalized() * 10

    def check_borders(self) -> None:
        if self.position.x < 0:
            self.position = Vec2d(0, self.position.y)
            self.velocity = Vec2d(-1 * self.velocity.x, self.velocity.y)

        if self.position.y < 0:
            self.position = Vec2d(self.position.x, 0)
            self.velocity = Vec2d(self.velocity.x, -1 * self.velocity.y)

        if self.position.x > 1300:
            self.position = Vec2d(1300, self.position.y)
            self.velocity = Vec2d(-1 * self.velocity.x, self.velocity.y)

        if self.position.y > 700:
            self.position = Vec2d(self.position.x, 700)
            self.velocity = Vec2d(self.velocity.x, -1 * self.velocity.y)


class GraphicsComponent(BaseGraphicsComponent):
    def __init__(self, parent: GameObject, **kwargs) -> None:
        super().__init__(parent, **kwargs)

        main_path = "assets/enemy/drone1"

        self.frames_per_sprite = 6
        self.sprite_count = 4

        spritesheet_args = (48, 48, 4, self.sprite_count)

        self.idle_texture_path = f"{main_path}/Idle.png"
        self.forward_texture_path = f"{main_path}/Forward.png"
        self.backward_texture_path = f"{main_path}/Back.png"
        self.death_texture_path = f"{main_path}/Death.png"

        SpriteCache.load_spritesheet(
            self.idle_texture_path, flip=True, *spritesheet_args
        )
        SpriteCache.load_spritesheet(
            self.forward_texture_path, flip=True, *spritesheet_args
        )
        SpriteCache.load_spritesheet(
            self.backward_texture_path, flip=True, *spritesheet_args
        )
        SpriteCache.load_spritesheet(
            self.death_texture_path,
            flip=True,
            sprite_width=48,
            sprite_height=48,
            columns=8,
            count=8,
        )

        self.current_frame = 0

    def update(self, delta_time: float) -> None:
        self.position = self.parent.position
        self.current_frame += 1

        if self.parent.state == State.DYING:
            self.current_frame %= 8 * self.frames_per_sprite
            current_sprite = self.current_frame // self.frames_per_sprite

            if current_sprite == 7:
                self.parent.state = State.DEAD

            self.texture = self.death_texture[current_sprite]
            return

        elif self.parent.state == State.DEAD:
            self.texture = self.death_texture[-1]
            return

        self.current_frame %= self.sprite_count * self.frames_per_sprite

        match self.parent.state:
            case State.ACTIVE:
                self.texture = self.forward_texture[
                    self.current_frame // self.frames_per_sprite
                ]

            case State.IDLE:
                self.texture = self.backward_texture[
                    self.current_frame // self.frames_per_sprite
                ]

    @property
    def idle_texture(self) -> list[Texture]:
        return SpriteCache.get_sprite(self.idle_texture_path, flip=True)

    @property
    def forward_texture(self) -> list[Texture]:
        return SpriteCache.get_sprite(self.forward_texture_path, flip=True)

    @property
    def backward_texture(self) -> list[Texture]:
        return SpriteCache.get_sprite(self.backward_texture_path, flip=True)

    @property
    def death_texture(self) -> list[Texture]:
        return SpriteCache.get_sprite(self.death_texture_path, flip=True)


class Enemy(GameObject):
    def __init__(
        self, id: int, initial_position: Vec2d = Vec2d.zero(), scale: float = 1.0
    ) -> None:
        super().__init__()
        self.id = id

        self.typing_component = TypingComponent(self)
        self.ai_movement_component = AIMovementComponent(
            self, initial_position=initial_position
        )
        self.graphics_component = GraphicsComponent(
            self, initial_position=initial_position, scale=scale
        )

        self.components = [
            self.typing_component,
            self.ai_movement_component,
            self.graphics_component,
        ]

        self.state = State.IDLE

    def update(self, delta_time: float) -> None:
        if self.state != State.DEAD:
            if len(self.prompt) == 0:
                self.state = State.DYING

        self.ai_movement_component.update(delta_time)
        self.graphics_component.update(delta_time)

    def handle_char(self, char: str) -> None:
        self.typing_component.handle_char(char)

    def draw(self) -> None:
        self.graphics_component.draw()

    def select(self) -> None:
        self.state = State.ACTIVE

    def _get_state(self) -> dict:
        return {"state": self.state.value}

    def _apply_state(self, state: dict) -> None:
        self.state = State(state.get("state")) or self.state

    @property
    def position(self) -> Vec2d:
        return self.ai_movement_component.position

    @property
    def prompt(self) -> list[str]:
        return "".join(self.typing_component.prompt)

    @property
    def is_alive(self) -> bool:
        return self.state not in {State.DYING, State.DEAD}

    @property
    def is_dead(self) -> bool:
        return self.state == State.DEAD
