from typing import Any

import arcade


class Component:
    def __init__(self, parent: "GameObject") -> None:
        self.parent = parent

    def update(self, delta_time: float) -> Any:
        raise NotImplementedError


class ArcadeGraphicsComponent(arcade.Sprite, Component):
    def __init__(self, parent: "GameObject", **kwargs) -> None:
        super().__init__(**kwargs)

        self.parent = parent


class GameObject:
    def update(self, delta_time: float) -> Any:
        raise NotImplementedError
