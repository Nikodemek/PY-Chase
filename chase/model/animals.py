from __future__ import annotations
from enum import Enum
import random
from model.point import Point


class Direction(Enum):
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3

    @staticmethod
    def random() -> Direction:
        return Direction(random.randint(0, 4))


class Animal:

    dir_to_point = {
        Direction.EAST: Point(1, 0),
        Direction.SOUTH: Point(0, -1),
        Direction.WEST: Point(-1, 0),
        Direction.NORTH: Point(0, 1)
    }

    def __init__(self, position: Point, move_dist: float):
        self.position = position
        self.move_dist = move_dist


class Sheep(Animal):

    def __init__(self, number: int, move_dist: float, position: Point = None, init_pos_limit: float = 1.0, alive: bool = True):
        super().__init__(position or Point.random(init_pos_limit), move_dist)
        self.number = number
        self.alive = alive

    def move(self, direction: Direction = None):
        direction = direction or Direction.random()
        self.position += Animal.dir_to_point[direction] * self.move_dist

    def __repr__(self):
        state: str = self.position if self.alive else "eaten"
        return f"Sheep_{self.number}: {state}"


class Wolf(Animal):

    def __init__(self, move_dist: float, position: Point = None):
        super().__init__(position or Point(0.0, 0.0), move_dist)

    def move(self, target: Point):
        vector: Point = self.position.calculate_vector(target)
        self.position += vector * self.move_dist

    def __repr__(self):
        return f"Wolf: {self.position}"