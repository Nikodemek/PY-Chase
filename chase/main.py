from model.point import Point
from model.animals import Sheep


def main():
    print("Simulation started")

    point = Point(1, 2.3)

    sheep = Sheep(0)
    print(sheep)

    sheep.alive = False
    print(sheep)





if __name__ == '__main__':
    main()

