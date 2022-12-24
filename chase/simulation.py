from enum import Enum
from animals import Sheep, Wolf, Flock
from scrivener import Scrivener


class LogLevel(Enum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class SimulationState(Enum):
    INIT = 0
    RUNNING = 1
    END = 2


class SimulationOptions:

    def __init__(
            self,
            max_rounds_number: int = 50,
            flock_size: int = 15,
            init_pos_limit: float = 10.0,
            sheep_move_dist: float = 0.5,
            wolf_move_dist: float = 1.0,
            wait_after_round: bool = False,
            scrivener: Scrivener = None
    ):
        self.max_rounds_number: int = max_rounds_number
        self.flock_size: int = flock_size
        self.init_pos_limit: float = init_pos_limit
        self.sheep_move_dist: float = sheep_move_dist
        self.wolfe_move_dist: float = wolf_move_dist
        self.wait_after_round: bool = wait_after_round
        self.scrivener: Scrivener = scrivener


class Simulation:

    def __init__(self, options: SimulationOptions):
        sheep: list[Sheep] = [
            Sheep(
                number=number,
                move_dist=options.sheep_move_dist,
                init_pos_limit=options.init_pos_limit,
                alive=True)
            for number
            in range(options.flock_size)
        ]
        self.flock: Flock = Flock(sheep)
        self.wolf: Wolf = Wolf(options.wolfe_move_dist)
        self.round_number: int = 1
        self.max_rounds_number: int = options.max_rounds_number
        self.wait_after_round: bool = options.wait_after_round

        self.closest_sheep: Sheep = None
        self.reached: bool = False

        self.scrivener: Scrivener = options.scrivener
        self.simulation_state = SimulationState.INIT

    def simulate(self):
        self.simulation_state = SimulationState.INIT

        self.scrivener.console_log(self)
        while (self.round_number <= self.max_rounds_number
               and not self.flock.are_all_eaten()):
            self.simulation_state = SimulationState.RUNNING

            self.flock.move()

            self.closest_sheep = self.wolf.find_closest_sheep(self.flock.remaining)
            self.reached: bool = self.wolf.move(self.closest_sheep.position)

            if self.reached:
                self.flock.eliminate_sheep(self.closest_sheep)

            self.scrivener.console_log(self)
            self.scrivener.add_pos_entry(self.round_number, self.wolf.position, self.flock.all)
            self.scrivener.add_alive_entry(self.round_number, len(self.flock.remaining))
            self.round_number += 1
            if self.wait_after_round:
                input("Press Enter to continue...")

        self.simulation_state = SimulationState.END

        self.scrivener.console_log(self)
        self.scrivener.dispose()
