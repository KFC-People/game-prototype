import arcade

from client.views.pause import PauseView
from common.sprites import Robot
from common.typing_engine import TypingEngine


class GameView(arcade.View):
    def __init__(self, window: arcade.Window = None):
        super().__init__(window)

        self.camera = None
        self.gui_camera = None
        self.robot = None
        self.background = None
        self.typing_engine = None
        self.speed_wpm = 0.0

        self.font_config = {
            "anchor_x": "center",
            "color": arcade.color.WHITE,
            "font_name": "monospace",
            "font_size": 64,
            "bold": True,
        }

    def on_show_view(self):
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        self.robot = Robot()
        self.robot.center_x = 64
        self.robot.center_y = 64

        self.background = arcade.load_texture(
            ":resources:images/cybercity_background/far-buildings.png"
        )

        self.typing_engine = TypingEngine()

    def on_update(self, delta_time: float):
        self.speed_wpm = self.typing_engine.update()

        self.robot.change_x = self.speed_wpm * 0.2

        self.robot.update()
        self.robot.update_animation()

        self._update_camera()

    def _update_camera(self):
        self.camera.move_to((self.robot.center_x - self.window.width // 2, 0), 0.6)

    def on_draw(self):
        self.clear()
        self.camera.use()

        offset_x = (self.robot.center_x // self.window.width - 1) * self.window.width
        repetitions = self.window.width // self.background.width

        for x in range(0, repetitions):
            arcade.draw_lrwh_rectangle_textured(
                offset_x + x * self.window.width,
                0,
                self.window.width,
                self.window.height,
                self.background,
            )

        self.robot.draw()

        self.gui_camera.use()

        arcade.draw_text(
            f"{self.speed_wpm:.1f} WPM",
            self.window.width // 2,
            self.window.height * 0.8,
            **self.font_config,
        )

    def on_key_press(self, symbol: int, *_):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(PauseView(self))

        # TODO: move this logic to the TypingEngine class
        # and add support for other language layouts
        elif " " <= (char := chr(symbol)) <= "~":
            self.typing_engine.handle_char(char)
