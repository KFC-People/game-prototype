import arcade


class OptionsView(arcade.View):
    def __init__(self, previous_view: arcade.View, window: arcade.Window | None = None):
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

        for i, text in enumerate(
            ["options menu", "", "select an option:", "press <esc> to go back"], start=2
        ):
            arcade.draw_text(
                text,
                start_x=width / 2,
                start_y=(10 - i) / 10 * height,
                **self.font_config,
            )

    def on_key_press(self, symbol: int, *_):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.previous_view)
