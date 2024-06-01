import arcade

from client.views.main_menu import MainMenuView


class SplashView(arcade.View):
    def __init__(self, window: arcade.Window | None = None):
        super().__init__(window)

        self.font_config = {
            "anchor_x": "center",
            "color": arcade.color.GREEN,
            "font_name": "monospace",
            "font_size": 24,
        }

        self.title_text = "press <i> to continue"
        self.text_index = 0
        self.frame_count = 0

        self.cursor_visible = True
        self.cursor_blink_rate = 30

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_update(self, *_) -> None:
        self.frame_count += 1

        if self.frame_count % 3 == 0 and self.text_index < len(self.title_text):
            self.text_index += 1

        if self.frame_count % self.cursor_blink_rate == 0:
            self.cursor_visible = not self.cursor_visible

    def on_draw(self):
        self.clear()

        width, height = self.window.get_size()
        start_x, start_y = width / 2, height / 2

        arcade.draw_text(
            "> typetypetype", start_x=start_x, start_y=start_y + 25, **self.font_config
        )

        arcade.draw_text(
            "  "
            + self.title_text[: self.text_index]
            + (" █" if self.cursor_visible else "  "),
            start_x=start_x,
            start_y=start_y - 25,
            **self.font_config,
        )

    def on_key_press(self, symbol: int, *_):
        if symbol == arcade.key.I:
            self.window.show_view(MainMenuView())
