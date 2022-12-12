from model.animals import Sheep, Wolf


class SimulationOptions:

    def __init__(
            self,
            max__rounds_number: int = 50,
            flock_size: int = 15,
            init_pos_limit: float = 10.0,
            sheep_move_dist: float = 0.5,
            wolfe_move_dist = 1.0
    ):
        self.max__rounds_number = max__rounds_number
        self.flock_size = flock_size
        self.init_pos_limit = init_pos_limit
        self.sheep_move_dist = sheep_move_dist
        self.wolfe_move_dist = wolfe_move_dist


class Simulation:

    def __init__(self, options: SimulationOptions):
        self.options = options
        self.flock = [Sheep(number) for number in range(options.flock_size)]
        self.wolf = Wolf()
        self.round_number = 0

    def simulate(self):
        pass















