import random

from pymunk import Vec2d

from common.enemy import Enemy
from common.id_generator import IDGenerator
from common.vehicle import Vehicle


class PlayerType:
    DRIVER = 1
    GUNNER = 2
    HEALER = 3


PLAYER_LABELS = {
    PlayerType.DRIVER: "driver",
    PlayerType.GUNNER: "gunner",
    PlayerType.HEALER: "healer",
}


class Game:
    def __init__(self) -> None:
        self.vehicle = Vehicle(initial_position=Vec2d(0, 0), mass=10)

        self.enemies: dict[int, Enemy] = {}
        self.current_enemy: Enemy | None = None

    def update(self, delta_time: float) -> None:
        self.vehicle.update(delta_time)

        if self.current_enemy is not None and self.current_enemy.is_dead:
            del self.enemies[self.current_enemy.id]
            self.current_enemy = None

        for enemy in list(self.enemies.values()):
            enemy.update(delta_time)

    def handle_player_key(self, player_type: int, key: int) -> None:
        match player_type:
            case PlayerType.DRIVER:
                if " " <= (char := chr(key)) <= "~":
                    self.vehicle.handle_char(char)

            case PlayerType.GUNNER:
                if " " <= (char := chr(key)) <= "~":
                    if self.current_enemy is None or not self.current_enemy.is_alive:
                        for enemy in list(self.enemies.values()):
                            if enemy.is_alive:
                                self.current_enemy = enemy
                                break

                    if self.current_enemy is not None:
                        self.current_enemy.handle_char(char)

            case PlayerType.HEALER:
                pass

    def get_state(self) -> dict:
        return {
            "vehicle": self.vehicle.get_state(),
            "enemies": {
                enemy_id: enemy.get_state() for enemy_id, enemy in self.enemies.items()
            },
        }

    def apply_state(self, state: dict) -> None:
        self.vehicle.apply_state(state["vehicle"])

        for enemy_id, enemy_state in state["enemies"].items():
            enemy_id = int(enemy_id)

            if enemy_id not in self.enemies:
                self.enemies[enemy_id] = Enemy(id=enemy_id, scale=2.0)
                self.enemies[enemy_id].apply_state(enemy_state)

            enemy_state.pop("position")
            enemy_state.pop("velocity")
            self.enemies[enemy_id].apply_state(enemy_state)

    def spawn_random_enemy(self) -> None:
        _id = IDGenerator.next_id()
        position = Vec2d(random.randint(300, 700), random.randint(400, 900))

        self.enemies[_id] = Enemy(id=_id, initial_position=position)
