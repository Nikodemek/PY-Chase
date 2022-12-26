from .initializer import parse_arguments
from .simulation import Simulation, SimulationOptions


def main():

    options: SimulationOptions = parse_arguments()

    simulation: Simulation = Simulation(options)
    simulation.simulate()


if __name__ == '__main__':
    main()
