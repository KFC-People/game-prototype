import arcade
from pymunk import Vec2d

from client.views.pause import PauseView
from common.enemy import Enemy
from common.vehicle import Vehicle


class GameView(arcade.View):
    def __init__(self, window: arcade.Window = None) -> None:
        super().__init__(window)

        self.camera = None
        self.gui_camera = None

        self.vehicle = None
        self.enemies = None

        self.background_layers = []
        self.layer_positions = [0] * 5
        self.layer_speeds = [0, 0.05, 0.1, 0.15, 0.2]

    def on_show_view(self) -> None:
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        self.vehicle_screen_position = Vec2d(200, 135)
        self.vehicle = Vehicle(self.vehicle_screen_position, mass=10, scale=2)
        self.camera.move(self.vehicle_screen_position)

        self.enemies: list[Enemy] = []
        self.enemies.append(Enemy(Vec2d(500, 135), scale=2))

        self.background_layers = [
            arcade.load_texture(f"assets/backgrounds/city/{i}.png") for i in range(1, 6)
        ]

    def on_update(self, delta_time: float) -> None:
        self.vehicle.update(delta_time)
        for enemy in self.enemies:
            enemy.update(delta_time)

        camera_position = self.vehicle.position - self.vehicle_screen_position
        self.camera.move_to(camera_position, 0.1)

        for i in range(len(self.layer_positions)):
            self.layer_positions[i] -= self.layer_speeds[i] * self.vehicle.velocity.x

    def on_draw(self):
        self.clear()

        self.gui_camera.use()

        height = self.window.height
        width = self.window.width
        road_height = 100

        for i, texture in enumerate(self.background_layers):
            if i == 0:
                arcade.draw_lrwh_rectangle_textured(0, 0, width, height, texture)
                continue

            x = self.layer_positions[i] % width
            arcade.draw_lrwh_rectangle_textured(x, road_height, width, height, texture)
            arcade.draw_lrwh_rectangle_textured(
                x - width, road_height, width, height, texture
            )

        arcade.draw_rectangle_filled(
            width / 2,
            road_height / 2,
            width,
            road_height,
            arcade.color.DARK_MIDNIGHT_BLUE,
        )

        arcade.draw_text(
            self.vehicle.prompt,
            width / 2,
            38,
            arcade.color.WHITE,
            font_size=25,
            font_name="FiraCode Nerd Font",  # TODO: load font from assets
            bold=True,
        )

        for enemy in self.enemies:
            enemy.draw()
            arcade.draw_text(
                enemy.prompt,
                enemy.position.x - 25,
                enemy.position.y + 50,
                arcade.color.WHITE,
                font_size=16,
                font_name="FiraCode Nerd Font",
                bold=True,
            )

        self.camera.use()
        self.vehicle.draw()

    def on_key_press(self, symbol: int, *_) -> None:
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(PauseView(self))

        elif " " <= (char := chr(symbol)) <= "~":
            self.vehicle.handle_char(char)

            if current_enemy := self.enemies[0]:
                current_enemy.handle_char(char)
