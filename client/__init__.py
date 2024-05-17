import arcade

from client.views import GameView, SplashView

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "fuckfuckfuck client"


def run_game(update_rate: float = 1 / 60):
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.set_update_rate(update_rate)

    window.game_view = GameView()
    splash_view = SplashView()

    window.show_view(splash_view)
    arcade.run()
