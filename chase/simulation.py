from model.animals import Sheep, Wolf, Flock


class SimulationOptions:

    def __init__(
            self,
            max_rounds_number: int = 50,
            flock_size: int = 15,
            init_pos_limit: float = 10.0,
            sheep_move_dist: float = 0.5,
            wolfe_move_dist: float = 1.0,
            wait_after_round: bool = False
    ):
        self.max_rounds_number: int = max_rounds_number
        self.flock_size: int = flock_size
        self.init_pos_limit: float = init_pos_limit
        self.sheep_move_dist: float = sheep_move_dist
        self.wolfe_move_dist: float = wolfe_move_dist
        self.wait_after_round: bool = wait_after_round


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
        self.round_number: int = 0
        self.max_rounds_number: int = options.max_rounds_number

    def simulate(self):

        self.log()
        while (self.round_number < self.max_rounds_number
               and not self.flock.are_all_eaten()):

            closest_sheep: Sheep = self.wolf.find_closest_sheep(self.flock.remaining)
            reached: bool = self.wolf.move(closest_sheep.position)

            if reached:
                self.flock.eliminate_sheep(closest_sheep)

            self.flock.move()

            self.log()
            self.round_number += 1

    def log(self) -> None:
        message: str = \
            f"""
Round_{self.round_number}: Initial = {len(self.flock.all)}, Remaining = {len(self.flock.remaining)}
    Wolf: {self.wolf.position}
    Sheep:
"""
        for sheep in self.flock.remaining:
            message += f"\t\t{sheep}\n"

        print(message)

