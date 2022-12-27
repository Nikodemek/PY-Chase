from enum import Enum

from .logger_provider import get_logger
from .animals import Sheep, Wolf, Flock
from .scrivener import Scrivener


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
        self.log = get_logger(__name__)

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
        self.round_number: int = 0
        self.max_rounds_number: int = options.max_rounds_number
        self.wait_after_round: bool = options.wait_after_round

        self.closest_sheep: Sheep or None = None
        self.reached: bool = False

        self.scrivener: Scrivener = options.scrivener
        self.simulation_state: SimulationState = SimulationState.INIT

        self.log.info("Instantiated a Simulation object")

    def simulate(self):
        self.log.info("Starting the Simulation")

        self.simulation_state = SimulationState.INIT
        self.log.debug("Setting simulation_state to INIT")

        self.scrivener.add_alive_entry(self.round_number, len(self.flock.remaining))
        self.log.debug("Adding initial alive sheep entry")

        self.console_log()
        self.log.debug("Evaluating if the Simulation should be continued")
        while self.round_number < self.max_rounds_number and not self.flock.are_all_eaten():
            self.round_number += 1
            self.log.debug("Increasing round_number")

            self.log.debug(f"Continuing the Simulation. Round number {self.round_number}")

            if self.simulation_state != SimulationState.RUNNING:
                self.simulation_state = SimulationState.RUNNING
                self.log.debug("Setting simulation_state to RUNNING")

            self.log.info("Moving all Sheep")
            self.flock.move()

            self.closest_sheep = self.wolf.find_closest_sheep(self.flock.remaining)
            self.log.info(f"Finding closest Sheep. Found {self.closest_sheep}")

            self.reached: bool = self.wolf.attack(self.closest_sheep)
            self.log.info(f"Wolf ({self.wolf}){' successfully' if self.reached else ''} attacked a sheep ({self.closest_sheep})")

            if self.reached:
                self.flock.eliminate_sheep(self.closest_sheep)
                self.log.info("Eliminating closest sheep")

            self.console_log()
            self.log.debug("Logging Simulation state to console")

            self.scrivener.add_pos_entry(self.round_number, self.wolf.position, self.flock.all)
            self.log.debug("Adding animals position entry")

            self.scrivener.add_alive_entry(self.round_number, len(self.flock.remaining))
            self.log.debug("Adding alive sheep entry")

            if self.wait_after_round:
                self.log.debug("Waiting for user's input")
                input("Press Enter to continue...")

        self.log.debug(f"Ending the Simulation")

        self.simulation_state = SimulationState.END
        self.log.debug("Setting simulation_state to END")

        self.console_log()
        self.log.debug("Logging Simulation end state to console")

        self.log.debug("Disposing of the Scrivener")
        self.scrivener.dispose()

    def console_log(self):
        message: str

        remaining: list[Sheep] = self.flock.remaining
        initial: list[Sheep] = self.flock.all
        match self.simulation_state:
            case SimulationState.INIT:
                message = f'Initial state: Sheep: {len(initial)}\n' + \
                    f'\tWolf: {self.wolf.position}\n' + \
                    f'\tSheep:\n'
                for sheep in remaining:
                    message += f'\t\t{sheep}\n'
            case SimulationState.RUNNING:
                message = f'Round {self.round_number}: Initial = {len(initial)}, Remaining = {len(remaining)}\n' + \
                    f'\tWolf: {self.wolf.position}\n' + \
                    f'\tSheep:\n'
                for sheep in remaining:
                    message += f'\t\t{sheep}\n'

                message += f'\tChased: {self.closest_sheep}\n'
            case _:
                message = ""

        print(message)
