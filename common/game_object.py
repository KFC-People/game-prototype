from typing import Any

import arcade


class Component:
    def __init__(self, parent: "GameObject") -> None:
        self.parent = parent

    def update(self, delta_time: float) -> Any:
        raise NotImplementedError


class GameObject(arcade.Sprite):
    def __init__(self) -> None:
        super().__init__()

    def update(self, delta_time: float) -> Any:
        raise NotImplementedError
