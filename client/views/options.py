import arcade


class OptionsView(arcade.View):
    def __init__(self, previous_view: arcade.View, window: arcade.Window = None):
        super().__init__(window)

        self.font_config = {
            "anchor_x": "center",
            "color": arcade.color.GREEN,
            "font_name": "monospace",
            "font_size": 24,
        }

        self.previous_view = previous_view

    def on_show_view(self):
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

    def on_update(self, delta_time: float):
        pass

    def on_draw(self):
        self.clear()

        width, height = self.window.get_size()

        arcade.draw_text(
            "options menu",
            start_x=width / 2,
            start_y=height * 0.9,
            **self.font_config,
        )

        arcade.draw_text(
            "press <esc> to go back",
            start_x=width / 2,
            start_y=height * 0.1,
            **self.font_config,
        )

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.previous_view)
