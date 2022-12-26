from __future__ import annotations
from enum import Enum
import random

from .logger_provider import get_logger
from .point import Point


class Direction(Enum):
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3

    @staticmethod
    def random() -> Direction:
        return Direction(random.randint(0, 3))


class Animal:

    dir_to_point = {
        Direction.EAST: Point(1, 0),
        Direction.SOUTH: Point(0, -1),
        Direction.WEST: Point(-1, 0),
        Direction.NORTH: Point(0, 1)
    }

    def __init__(self, position: Point, move_dist: float):
        self.log = get_logger(__name__)

        self.position = position
        self.move_dist = move_dist


class Sheep(Animal):

    def __init__(
            self,
            number: int,
            move_dist: float,
            position: Point = None,
            init_pos_limit: float = 1.0,
            alive: bool = True
    ):
        super().__init__(position or Point.random(init_pos_limit), move_dist)
        self.number = number
        self.alive = alive

    def move(self, direction: Direction = None):
        direction = direction or Direction.random()
        self.position += Animal.dir_to_point[direction] * self.move_dist
        self.log.debug(f"Calculated new sheep position: {self.position}")

    def __repr__(self):
        state: str = self.position if self.alive else "eaten"
        return f"Sheep_{self.number}: {state}"


class Flock:

    def __init__(self, sheep: list[Sheep]):
        self.log = get_logger(__name__)

        self.all: list[Sheep] = sheep.copy()
        self.remaining: list[Sheep] = [s for s in sheep if s.alive]

    def move(self):
        for sheep in self.remaining:
            sheep.move()
        self.log.info(f"Moved all remaining sheep")

    def eliminate_sheep(self, sheep: Sheep):
        sheep.alive = False
        self.remaining.remove(sheep)
        self.log.info(f"Eliminated sheep {sheep}")

    def are_all_eaten(self) -> bool:
        return len(self.remaining) < 1


class Wolf(Animal):

    def __init__(self, move_dist: float, position: Point = None):
        super().__init__(position or Point(0.0, 0.0), move_dist)

    def find_closest_sheep(self, remaining_sheep: list[Sheep]) -> Sheep:
        length: int = len(remaining_sheep)

        if length < 1:
            self.log.error(f"Flock length is {length} (less than 1)!")
            raise ValueError(f"Flock length is {length} (less than 1)!")

        closest_sheep: Sheep = remaining_sheep[0]
        closest_magnitude: float = self.position.magnitude(closest_sheep.position)

        for sheep in remaining_sheep[1:]:
            magnitude = self.position.magnitude(sheep.position)
            self.log.debug(f"Calculated magnitude between {self.position} and {sheep.position}. Got {magnitude}")

            if magnitude < closest_magnitude:
                closest_sheep = sheep
                closest_magnitude = magnitude
                self.log.debug(f"Found closer sheep: {closest_sheep}")

        return closest_sheep

    def move(self, target: Point) -> bool:
        distance: float = self.position.distance(target)
        self.log.debug(f"Calculated distance between wolf and target: |{self.position}, {target}| = {distance}")

        if distance <= self.move_dist:
            self.position = target
            return True
        else:
            vector: Point = self.position.calculate_vector(target)
            self.log.debug(f"Calculated movement vector: {vector}")
            self.position += vector * self.move_dist
            self.log.debug(f"Calculated new wolf position: {self.position}")
            return False

    def __repr__(self):
        return f"Wolf: {self.position}"
