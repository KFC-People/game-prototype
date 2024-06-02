import arcade

from client.views import GameView, SplashView


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "typetypetype client"


def run_game(update_rate: float = 1 / 60) -> None:
    window = arcade.Window(
        width=SCREEN_WIDTH,
        height=SCREEN_HEIGHT,
        title=SCREEN_TITLE,
        update_rate=update_rate,
    )

    window.game_view = GameView()
    splash_view = SplashView()

    window.show_view(splash_view)
    arcade.run()
