import arcade

from common.game_object import Component, GameObject


class TypingComponent(Component):
    def __init__(self, parent: GameObject) -> None:
        super().__init__(parent)

        self.prompt = []
        self.health = len(self.prompt)

    def handle_char(self, char: str) -> None:
        if char == self.prompt[0]:
            self.prompt.pop(0)
            self.health -= 1

        else:
            self.health += 1

        if not self.prompt:
            # renew prompt
            return


class MovementComponent(Component):
    def update(self, delta_time: float) -> None:
        pass


class GraphicsComponent(Component):
    def __init__(self, parent: GameObject) -> None:
        super().__init__(parent)

        main_path = "assets/enemy"

        self.frames_per_sprite = 4
        self.sprite_count = 4

        spritesheet_args = (96, 96, 4, self.sprite_count)

        self.idle_texture = arcade.load_spritesheet(
            f"{main_path}/Idle.png", *spritesheet_args
        )

        self.forward_texture = arcade.load_spritesheet(
            f"{main_path}/Forward.png", *spritesheet_args
        )
        self.backward_texture = arcade.load_spritesheet(
            f"{main_path}/Backward.png", *spritesheet_args
        )

        self.death_texture = arcade.load_spritesheet(
            f"{main_path}/Death.png", *spritesheet_args
        )

        self.current_frame = 0

    def update(self, delta_time: float) -> None:
        self.current_frame += 1
        self.current_frame %= self.sprite_count * self.frames_per_sprite

        self.parent.texture = self.idle_texture[
            self.current_frame // self.frames_per_sprite
        ]


class Enemy(GameObject):
    def __init__(self):
        super().__init__()

        self.typing_component = TypingComponent(self)
        self.movement_component = MovementComponent(self)
        self.graphics_component = GraphicsComponent(self)

    def update(self, delta_time: float) -> None:
        self.movement_component.update(delta_time)
        self.graphics_component.update(delta_time)
