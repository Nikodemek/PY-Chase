from chase.initializer import parse_arguments
from simulation import Simulation, SimulationOptions, LogLevel


def main():

    options: SimulationOptions = parse_arguments()

    print(vars(options))
    return

    simulation: Simulation = Simulation(options)

    print("Simulation starting")
    simulation.simulate()


if __name__ == '__main__':
    main()

