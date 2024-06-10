from pymunk import Vec2d

from common.enemy import Enemy
from common.vehicle import Vehicle


class Game:
    def __init__(self) -> None:
        self.vehicle = Vehicle(initial_position=Vec2d(0, 0), mass=10)

        self.enemies: list[Enemy] = []
        self.current_enemy = None

    def update(self, delta_time: float) -> None:
        self.vehicle.update(delta_time)

        if self.current_enemy is not None and self.current_enemy.is_dead:
            self.enemies.remove(self.current_enemy)
            self.current_enemy = None

        for enemy in self.enemies:
            enemy.update(delta_time)

    def on_input(self, key: int) -> None:
        if " " <= (char := chr(key)) <= "~":
            self.vehicle.handle_char(char)

            if self.current_enemy is None or not self.current_enemy.is_alive:
                for enemy in self.enemies:
                    if enemy.is_alive:
                        self.current_enemy = enemy
                        break

            if self.current_enemy:
                self.current_enemy.handle_char(char)
