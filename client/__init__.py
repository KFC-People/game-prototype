import arcade

from client.views import MainMenuView, SplashView

SCREEN_TITLE = "typetypetype client"
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768


def run_game(update_rate: float = 1 / 60) -> None:
    window = arcade.Window(
        width=SCREEN_WIDTH,
        height=SCREEN_HEIGHT,
        title=SCREEN_TITLE,
        update_rate=update_rate,
    )

    splash_view = SplashView(MainMenuView())

    window.show_view(splash_view)
    arcade.run()
