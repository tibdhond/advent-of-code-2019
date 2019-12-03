import math
import operator


def main():
    grid = {}
    shortest = math.inf
    instrmap = {"L": (-1, 0), "R": (1, 0), "U": (0, -1), "D": (0, 1)}
    with open("input.txtg") as f:
        for building in [True, False]:
            inp = f.readline().split(",")
            coordinates = (0, 0)
            total = 0
            for instr in inp:
                direction = instrmap[instr[0]]
                steps = int(instr[1:])
                for _ in range(steps):
                    coordinates = tuple(map(operator.add, coordinates, direction))
                    total += 1
                    if not building:
                        if coordinates in grid:
                            shortest = min(shortest, grid[coordinates] + total)
                    else:
                        grid[coordinates] = min(total, grid.get(coordinates, math.inf))
    print(shortest)


if __name__ == '__main__':
    main()
