from scrivener import Scrivener
from simulation import LogLevel, SimulationOptions
from os import path, mkdir
import argparse
import configparser


class Arguments:

    def __init__(
            self,
            config_file: str = "",
            directory: str = ".",
            log_level: LogLevel = LogLevel.INFO,
            number_of_rounds: int = 50,
            number_of_sheep: int = 15,
            wait_after_round: bool = False
    ):
        self.config_file: str = config_file
        self.directory: str = directory
        self.number_of_rounds: int = number_of_rounds
        self.number_of_sheep: int = number_of_sheep
        self.wait_after_round: bool = wait_after_round

        self.validate_arguments()

        self.init_pos_limit: float = 10.0
        self.sheep_move_dist: float = 0.5
        self.wolf_move_dist: float = 1.0

        self.read_config_if_exists()
        self.validate_config()

        self.scrivener: Scrivener = Scrivener(
            base_directory=self.directory,
            log_level=log_level
        )

    def validate_arguments(self):
        if self.number_of_rounds < 1:
            raise ValueError(f"Number of rounds is {self.number_of_rounds} but must be larger than 0!")

        if self.number_of_sheep < 1:
            raise ValueError(f"Number of sheep is {self.number_of_sheep} but must be larger than 0!")

        if self.config_file != "" and not path.exists(self.config_file):
            raise ValueError("Config file argument was passed, but the file does not exist!")

        if not path.exists(self.directory):
            mkdir(self.directory)

    def read_config_if_exists(self):
        if self.config_file == "":
            return

        parser = configparser.SafeConfigParser()
        parser.read(self.config_file)

        try:
            self.init_pos_limit = parser.getfloat('Terrain', 'InitPosLimit')
            self.sheep_move_dist = parser.getfloat('Movement', 'SheepMoveDist')
            self.wolf_move_dist = parser.getfloat('Movement', 'WolfMoveDist')
        except Exception as e:
            raise ValueError("Error reading values of config File!", e)

    def validate_config(self):
        if self.init_pos_limit < 0:
            raise ValueError(f"Initial position limit is {self.init_pos_limit} but must not be less than 0!")

        if self.sheep_move_dist < 0:
            raise ValueError(f"Sheep move distance is {self.sheep_move_dist} but must not be less than 0!")

        if self.wolf_move_dist < 0:
            raise ValueError(f"Wolf move distance is {self.wolf_move_dist} but must not be less than 0!")

    def get_simulation_options(self) -> SimulationOptions:
        return SimulationOptions(
            max_rounds_number=self.number_of_rounds,
            flock_size=self.number_of_sheep,
            init_pos_limit=self.init_pos_limit,
            sheep_move_dist=self.sheep_move_dist,
            wolf_move_dist=self.wolf_move_dist,
            wait_after_round=self.wait_after_round,
            scrivener=self.scrivener
        )


def parse_arguments() -> SimulationOptions:
    parser = argparse.ArgumentParser(
        prog="Chase",
        description="Argument Parser for 'Chase' Simulation",
        epilog="Have a great simulation!")

    parser.add_argument("-c", "--config",
                        type=str,
                        default="",
                        dest="config_file",
                        metavar="FILE",
                        help="Name of the config file")
    parser.add_argument("-d", "--dir",
                        type=str,
                        default=".",
                        dest="directory",
                        metavar="DIR",
                        help="Path to directory where logs will be stored")
    parser.add_argument("-l", "--log",
                        type=LogLevel,
                        choices=[level for level in LogLevel],
                        default=LogLevel.INFO,
                        dest="log_level",
                        metavar="LEVEL",
                        help="Logging level")
    parser.add_argument("-r", "--rounds",
                        type=int,
                        default=50,
                        dest="number_of_rounds",
                        metavar="NUM",
                        help="Max number of rounds for simulation")
    parser.add_argument("-s", "--sheep",
                        type=int,
                        default=15,
                        dest="number_of_sheep",
                        metavar="NUM",
                        help="Initial number of sheep for simulation")
    parser.add_argument("-w", "--wait",
                        action="store_true",
                        dest="wait_after_round",
                        help="Flag indicating whether simulation will be paused after every round")

    args, leftovers = parser.parse_known_args()

    arguments = Arguments(
        config_file=args.config_file,
        directory=args.directory,
        log_level=args.log_level,
        number_of_rounds=args.number_of_rounds,
        number_of_sheep=args.number_of_sheep,
        wait_after_round=args.wait_after_round
    )

    return arguments.get_simulation_options()
