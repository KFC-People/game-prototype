import arcade


class ServerListView(arcade.View):
    def __init__(self, window: arcade.Window | None = None) -> None:
        super().__init__(window)
        self.font_config = {
            "anchor_x": "center",
            "color": arcade.color.GREEN,
            "font_name": "monospace",
            "font_size": 24,
        }

    def on_show_view(self) -> None:
        arcade.set_background_color(arcade.color.SMOKY_BLACK)
        self.servers = self.get_servers()

    def get_servers(self) -> list[tuple[str, int]]:
        return [("127.0.0.1", 1234)]

    def on_draw(self) -> None:
        self.clear()

        width, height = self.window.get_size()

        for i, (ip, port) in enumerate(self.servers, start=2):
            arcade.draw_text(
                f"{i - 2} - {ip}:{port}",
                start_x=width / 2,
                start_y=(10 - i) / 10 * height,
                **self.font_config,
            )

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if 0 <= (i := symbol - 48) < len(self.servers):
            ip, port = self.servers[i]
            self.window.game_view.connect(ip, port)
            self.window.show_view(self.window.game_view)

        else:
            print("out of range")
