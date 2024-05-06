import arcade

from client.views.options import OptionsView


class PauseView(arcade.View):
    def __init__(self, previous_view: arcade.View, window: arcade.Window = None):
        super().__init__(window)

        self.previous_view = previous_view
        self.font_config = {
            "anchor_x": "center",
            "color": arcade.color.GREEN,
            "font_name": "monospace",
            "font_size": 24,
        }

    def on_show_view(self):

        arcade.set_background_color(arcade.color.SMOKY_BLACK)

    def on_update(self, delta_time: float):
        pass

    def on_draw(self):
        self.clear()

        width, height = self.window.get_size()

        for i, text in enumerate(
            [
                "paused",
                "",
                "select an option:",
                "press <o> to open the options menu",
                "press <esc> to go back",
                "press <q> to quit the game",
            ],
            start=2,
        ):
            arcade.draw_text(
                text,
                start_x=width / 2,
                start_y=(10 - i) / 10 * height,
                **self.font_config,
            )

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.O:
            self.window.show_view(OptionsView(self))

        elif symbol == arcade.key.ESCAPE:
            self.window.show_view(self.previous_view)

        elif symbol == arcade.key.Q:
            arcade.close_window()
