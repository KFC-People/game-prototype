import arcade
from pymunk import Vec2d

from client.views.pause import PauseView
from common.vehicle import Vehicle


class GameView(arcade.View):
    def __init__(self, window: arcade.Window = None) -> None:
        super().__init__(window)

        self.camera = None
        self.gui_camera = None

        self.vehicle = None

        self.background_layers = []
        self.layer_positions = [0] * 5
        self.layer_speeds = [0, 0.5, 0.75, 1, 1.5]

    def on_show_view(self) -> None:
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        self.vehicle = Vehicle(
            initial_position=Vec2d(128, 150),
            mass=10,
            scale=2,
        )

        self.background_layers = [
            arcade.load_texture(f"assets/backgrounds/city/{i}.png") for i in range(1, 6)
        ]

    def on_update(self, delta_time: float) -> None:
        self.vehicle.update(delta_time)

        for i in range(len(self.layer_positions)):
            self.layer_positions[i] -= self.layer_speeds[i] * self.vehicle.velocity.x

    def on_draw(self):
        self.clear()
        self.camera.use()

        height = self.window.height
        width = self.window.width

        for i, texture in enumerate(self.background_layers):
            if i == 0:
                arcade.draw_lrwh_rectangle_textured(0, 0, width, height, texture)
                continue

            x = self.layer_positions[i] % width
            arcade.draw_lrwh_rectangle_textured(x, 0, width, height, texture)
            arcade.draw_lrwh_rectangle_textured(x - width, 0, width, height, texture)

        road_height = 100
        arcade.draw_rectangle_filled(
            width / 2,
            road_height / 2,
            width,
            road_height,
            arcade.color.LIGHT_GRAY,
        )

        self.vehicle.draw()

        self.gui_camera.use()

        arcade.draw_text(
            self.vehicle.prompt,
            width / 2,
            50,
            arcade.color.BLACK,
            font_size=25,
            font_name="FiraCode Nerd Font",  # TODO: load font from assets
            bold=True,
        )

    def on_key_press(self, symbol: int, *_) -> None:
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(PauseView(self))

        elif " " <= (char := chr(symbol)) <= "~":
            self.vehicle.handle_char(char)
