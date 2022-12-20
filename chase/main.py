from simulation import Simulation, SimulationOptions
import argparse


def parse_arguments() -> SimulationOptions:
    parser = argparse.ArgumentParser(
        prog="Chase",
        description="Argument Parser for 'Chase' Simulation",
        epilog="Have a great simulation!")

    parser.add_argument("-c", "--config",
                        type=str,
                        default=None,
                        dest="config",
                        metavar="FILE",
                        help="Name of the config file")
    parser.add_argument("-d", "--dir",
                        type=str,
                        default=".",
                        dest="dir",
                        metavar="DIR",
                        help="Path to directory where logs will be stored")
    parser.add_argument("-l", "--log",
                        type=str,
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        default="INFO",
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

    args = parser.parse_args()

    print("config", args.config)
    print("dir", args.dir)
    print("log", args.log_level)
    print("rounds", args.number_of_rounds)
    print("sheep", args.number_of_sheep)
    print("wait", args.wait_after_round)

    return SimulationOptions(
        max_rounds_number=args.number_of_rounds,
        flock_size=args.number_of_sheep,
        wait_after_round=args.wait_after_round
    )

def main():

    parse_arguments()


    print("IM GOING")
    return

    options: SimulationOptions = SimulationOptions(
        wolfe_move_dist=5
    )
    simulation: Simulation = Simulation(options)

    print("Simulation starting")
    simulation.simulate()





if __name__ == '__main__':
    main()

