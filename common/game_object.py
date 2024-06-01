from typing import Any

import arcade
from pymunk import Vec2d


class Component:
    def __init__(self, parent: "GameObject") -> None:
        self.parent = parent

    def update(self, delta_time: float) -> Any:
        raise NotImplementedError


class BaseMovementComponent(Component):
    def __init__(
        self,
        parent: "GameObject",
        initial_position: Vec2d = Vec2d.zero(),
        mass: float = 1,
    ) -> None:
        super().__init__(parent)

        self.mass = mass

        self.position = initial_position
        self.velocity = Vec2d.zero()
        self.acceleration = Vec2d.zero()


class BaseGraphicsComponent(arcade.Sprite, Component):
    def __init__(self, parent: "GameObject", initial_position: Vec2d, **kwargs) -> None:
        super().__init__(**kwargs)

        self.parent = parent
        self.center_x, self.center_y = initial_position.int_tuple


class GameObject:
    def update(self, delta_time: float) -> Any:
        raise NotImplementedError
