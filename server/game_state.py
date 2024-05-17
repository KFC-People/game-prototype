from dataclasses import dataclass, field


@dataclass(slots=True)
class Input:
    key: str
    correct: bool
    time: float


@dataclass(slots=True)
class PlayerState:
    text: str = ""
    history: list[Input] = field(default_factory=list)

    @property
    def speed_cps(self) -> float:
        return sum(
            key_input.correct for key_input in self.history
        )  # TODO: divide by TYPING_WINDOW_SECONDS

    @property
    def speed_wpm(self) -> float:
        return self.speed_cps * 60 / 5


@dataclass(slots=True)
class GunnerState(PlayerState):
    current_target_id: int = None


@dataclass(slots=True)
class EnemyState:
    id: int
    text: str


@dataclass(slots=True)
class GameState:
    health: int = 100

    driver: PlayerState = field(default_factory=PlayerState)
    gunner: GunnerState = field(default_factory=GunnerState)
    healer: PlayerState = field(default_factory=PlayerState)

    enemies: list[EnemyState] = field(default_factory=list)
