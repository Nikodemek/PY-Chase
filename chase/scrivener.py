import csv
import json
import logging
import os
from os import path
from typing import IO
from animals import Sheep
from point import Point
from simulation import LogLevel, SimulationState, Simulation


class Scrivener:

    def __init__(
            self,
            base_directory: str = None,
            log_level: LogLevel = LogLevel.INFO,
            log_filename: str = "chase.log",
            pos_filename: str = "pos.json",
            alive_filename: str = "alive.csv"
    ):
        files_dir_path = path.join(os.getcwd(), base_directory)

        log_filepath = path.join(files_dir_path, log_filename)
        pos_filepath = path.join(files_dir_path, pos_filename)
        alive_filepath = path.join(files_dir_path, alive_filename)

        logging.basicConfig(
            filename=log_filepath,
            level=log_level.name
        )
        self.logger = logging.getLogger("chase")

        self.pos_list: list[{}] = []
        self.alive_list: list[()] = []

        self.pos_file: IO = open(pos_filepath, "w")
        self.alive_file: IO = open(alive_filepath, "w")

        self.alive_writer = csv.writer(self.alive_file)
        self.alive_writer.writerow(("Round Number", "Number of Sheep"))

    def log_debug(self, log: str):
        self.logger.debug(log)

    def log_info(self, log: str):
        self.logger.info(log)

    def log_warning(self, log: str):
        self.logger.warning(log)

    def log_error(self, log: str):
        self.logger.error(log)

    def log_critical(self, log: str):
        self.logger.critical(log)

    def add_pos_entry(self, round_number: int, wolf_position: Point, all_sheep: list[Sheep]):
        self.pos_list.append(
            {
                'round_no': round_number,
                'wolf_pos': (wolf_position.x, wolf_position.y),
                'sheep_pos': [(sheep.position.x, sheep.position.y) if sheep.alive else None for sheep in all_sheep]
            }
        )
        self.save_pos()

    def add_alive_entry(self, round_number: int, remaining_sheep_count: int):
        self.alive_list.append((round_number, remaining_sheep_count))
        self.save_alive()

    def save_pos(self):
        data: str = json.dumps(self.pos_list, indent=4)
        self.pos_file.write(data)

    def save_alive(self):
        self.alive_writer.writerow(self.alive_list[-1])

    def console_log(self, sim: Simulation):
        message: str = None
        
        remaining: list[Sheep] = sim.flock.remaining
        all: list[Sheep] = sim.flock.all

        match sim.simulation_state:
            case SimulationState.INIT:
                message = f'Initial state: Sheep: {len(all)}\n' + \
                    f'\tWolf: {sim.wolf.position}\n' + \
                    f'\tSheep:\n'
                for sheep in remaining:
                    message += f'\t\t{sheep}\n'
            case SimulationState.RUNNING:
                message = f'Round_{sim.round_number}: Initial = {len(all)}, Remaining = {len(remaining)}\n' + \
                    f'\tWolf: {sim.wolf.position}\n' + \
                    f'\tSheep:\n'
                for sheep in remaining:
                    message += f'\t\t{sheep}\n'

                message += f'\tChased: {sim.closest_sheep}\n'
            case SimulationState.END:
                message = ""

        print(message)

    def dispose(self):
        self.pos_file.close()
        self.alive_file.close()
