from typing import Any

import arcade
from pymunk import Vec2d


class Component:
    def __init__(self, parent: "GameObject") -> None:
        self.parent = parent

    def update(self, delta_time: float) -> Any:
        raise NotImplementedError

    def get_state(self) -> dict:
        return {}

    def apply_state(self, state: dict) -> None:
        pass


class BaseMovementComponent(Component):
    def __init__(
        self,
        parent: "GameObject",
        initial_position: Vec2d = Vec2d.zero(),
        mass: float = 1.0,
    ) -> None:
        super().__init__(parent)

        self.mass = mass

        self.position = initial_position
        self.velocity = Vec2d.zero()
        self.acceleration = Vec2d.zero()

    def get_state(self) -> dict:
        return {
            "position": self.position.int_tuple,
            "velocity": self.velocity.int_tuple,
        }

    def apply_state(self, state: dict) -> None:
        self.position = Vec2d(*state["position"])
        self.velocity = Vec2d(*state["velocity"])


class BaseGraphicsComponent(arcade.Sprite, Component):
    def __init__(self, parent: "GameObject", initial_position: Vec2d, **kwargs) -> None:
        super().__init__(**kwargs)

        self.parent = parent
        self.center_x, self.center_y = initial_position.int_tuple


class GameObject:
    def __init__(self) -> None:
        self.components: list[Component] = []

    def update(self, delta_time: float) -> Any:
        raise NotImplementedError

    def get_state(self) -> dict:
        state = {}

        for component in self.components:
            state.update(component.get_state())

        return state

    def apply_state(self, state: dict) -> None:
        for component in self.components:
            component.apply_state(state)
