import arcade

from client.views.options import OptionsView
from client.views.server_list import ServerListView


class MainMenuView(arcade.View):
    def __init__(self, window: arcade.Window | None = None) -> None:
        super().__init__(window)

        self.font_config = {
            "anchor_x": "center",
            "color": arcade.color.GREEN,
            "font_name": "monospace",
            "font_size": 24,
        }

    def on_show_view(self) -> None:
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self) -> None:
        self.clear()

        width, height = self.window.get_size()

        for i, text in enumerate(
            [
                "select an option:",
                "press <i> to open servers list",
                "press <o> to open the options menu",
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

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.Q:
            arcade.close_window()

        elif symbol == arcade.key.I:
            self.window.show_view(ServerListView())

        elif symbol == arcade.key.O:
            self.window.show_view(OptionsView(self))
