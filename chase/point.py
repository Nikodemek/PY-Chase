from __future__ import annotations
from math import sqrt
import random
import inspect


class Point:

    def __init__(self, init_x: float, init_y: float):
        self.x = init_x
        self.y = init_y

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __radd__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

    def __rsub__(self, other: Point) -> Point:
        return Point(other.x - self.x, other.y - self.y)

    def __mul__(self, number: float) -> Point:
        return Point(self.x * number, self.y * number)

    def __rmul__(self, number: float) -> Point:
        return Point(self.x * number, self.y * number)

    def __floordiv__(self, number: int) -> Point:
        return Point(self.x // number, self.y // number)

    def __truediv__(self, number: float) -> Point:
        return Point(self.x / number, self.y / number)

    def magnitude(self, other: Point) -> float:
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2

    def distance(self, other: Point) -> float:
        mag: float = self.magnitude(other)
        return sqrt(mag)

    def calculate_vector(self, other: Point) -> Point:
        diff: Point = other - self
        max_of_diff: float = max(abs(diff.x), abs(diff.y))
        return diff / max_of_diff

    @staticmethod
    def random(max_value: float, min_value: float = None) -> Point:
        min_value = min_value or -max_value
        new_x = random.uniform(min_value, max_value)
        new_y = random.uniform(min_value, max_value)
        return Point(new_x, new_y)

    def __repr__(self):
        return f"({self.x:.3f}, {self.y:.3f})"

    def __getattribute__(self, item):
        returned = object.__getattribute__(self, item)
        if inspect.isfunction(returned) or inspect.ismethod(returned):
            print('called ', returned.__name__, returned)
        return returned
