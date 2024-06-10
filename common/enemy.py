from arcade import Texture
from pymunk import Vec2d

from common.game_object import (
    BaseGraphicsComponent,
    BaseMovementComponent,
    Component,
    GameObject,
)
from enum import Enum, auto
from common.sprite_cache import SpriteCache


class State(Enum):
    IDLE = auto()
    DYING = auto()
    DEAD = auto()


class TypingComponent(Component):
    def __init__(self, parent: GameObject) -> None:
        super().__init__(parent)

        self.prompt = list("verylongwordhere")

    def handle_char(self, char: str) -> None:
        if len(self.prompt) == 0:
            return

        if char == self.prompt[0]:
            self.prompt.pop(0)


class AIMovementComponent(BaseMovementComponent):
    def __init__(
        self, parent: GameObject, initial_position: Vec2d = Vec2d.zero()
    ) -> None:
        super().__init__(parent, initial_position=initial_position)

    def update(self, delta_time: float) -> None:
        if not self.parent.is_alive:
            self.acceleration += Vec2d(-0.1, -0.4) * self.mass

        self.velocity += self.acceleration
        self.position += self.velocity

        self.acceleration = Vec2d.zero()


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
            self.current_frame %= 8 * 12
            current_sprite = self.current_frame // 12

            if current_sprite == 7:
                self.parent.state = State.DEAD

            self.texture = self.death_texture[current_sprite]
            return

        elif self.parent.state == State.DEAD:
            self.texture = self.death_texture[-1]
            return

        self.current_frame %= self.sprite_count * self.frames_per_sprite

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
        self, id: int = None, initial_position: Vec2d = Vec2d.zero(), scale: float = 1.0
    ) -> None:
        super().__init__()
        self.id = id or id(self)

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
