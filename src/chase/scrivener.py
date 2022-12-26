import csv
import json
import os
from os import path
from typing import IO

from .animals import Sheep
from .logger_provider import LogLevel, configure_logger, get_logger
from .point import Point


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

        configure_logger(log_filepath, log_level)
        self.log = get_logger(__name__)

        self.pos_list: list[{}] = []
        self.alive_list: list[()] = []

        self.pos_file: IO = open(pos_filepath, "w")
        self.alive_file: IO = open(alive_filepath, "w", newline='')

        self.alive_writer = csv.writer(self.alive_file)
        self.alive_writer.writerow(("Round Number", "Number of Sheep"))

    def add_pos_entry(self, round_number: int, wolf_position: Point, all_sheep: list[Sheep]):
        self.pos_list.append(
            {
                'round_no': round_number,
                'wolf_pos': (wolf_position.x, wolf_position.y),
                'sheep_pos': [(sheep.position.x, sheep.position.y) if sheep.alive else None for sheep in all_sheep]
            }
        )
        self.log.debug("Added position entry")

        self.save_pos()

    def add_alive_entry(self, round_number: int, remaining_sheep_count: int):
        self.alive_list.append((round_number, remaining_sheep_count))
        self.log.debug("Added alive entry")

        self.save_alive()

    def save_pos(self):
        data: str = json.dumps(self.pos_list, indent=4)
        self.pos_file.truncate(0)
        self.pos_file.seek(0)
        self.pos_file.write(data)
        self.log.debug("Saved position entry")

    def save_alive(self):
        self.alive_writer.writerow(self.alive_list[-1])
        self.log.debug("Saved alive entry")

    def dispose(self):
        self.pos_file.close()
        self.alive_file.close()
        self.log.debug("Closed position and alive files")
