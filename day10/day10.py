import math
from itertools import product


def check_direction(grid, x, y, x_inc, y_inc, count):
    start_x = x
    start_y = y
    x += x_inc
    y += y_inc
    # print(start_x, start_y)
    while 0 <= x < len(grid) and 0 <= y < len(grid[x]):
        if grid[x][y] == '#':
            grid[x][y] = str(count)
            if count == 200:
                print("200th asteroid: (%d, %d)" % (x, y))
            # print("Visible for (%d, %d): (%d, %d)" % (start_x, start_y, x, y))
            return count + 1
        y += y_inc
        x += x_inc
    return count


def main():
    with open("input.txt", 'r') as f:
        inpt = [list(line.strip()) for line in f.readlines()]
        best = 0
        best_c = (0, 0)

        x_range = []
        y_range = []
        for i in range(len(inpt)):
            x_range.append(i)
            x_range.append(-i)

        for i in range(len(inpt[0])):
            y_range.append(i)
            y_range.append(-i)

        x = 0
        while x < len(inpt):
            y = 0
            while y < len(inpt[x]):
                # print(x, y)
                if inpt[x][y] == '.':
                    y += 1
                    continue
                else:
                    inpt[x][y] = "0"

                seen = []

                for x_inc in x_range:
                    for y_inc in y_range:
                        if 0 <= x + x_inc < len(inpt) and 0 <= y + y_inc < len(inpt[x]):
                            gcd = math.gcd(x_inc, y_inc)
                            if gcd is 0 or (int(x_inc / gcd), int(y_inc / gcd)) in seen:
                                continue
                            seen.append((int(x_inc / gcd), int(y_inc / gcd)))
                            check_direction(inpt, x, y, x_inc, y_inc)

                print()
                if int(inpt[x][y]) > best:
                    best = int(inpt[x][y])
                    best_c = (x, y)
                y += 1
            x += 1

        for line in inpt:
            print(line)
        print(best, best_c)


def part2():
    with open("test.txt", 'r') as f:
        inpt = [list(line.strip()) for line in f.readlines()]
        start = (17, 14)
        # start = (3, 8)
        # start = (13, 11)
        inpt[start[0]][start[1]] = 'X'
        astroids = 0
        for row in inpt:
            for column in row:
                if column == '#':
                    astroids += 1

        print(astroids)

        list1 = [i for i in range(len(inpt))]
        list2 = [i for i in range(len(inpt[0]))]

        q1 = list(product(list1, list2))
        seen = []
        i = 0
        # print(q1)
        while i < len(q1):
            c = q1[i]
            gcd = math.gcd(c[0], c[1])
            if gcd == 0 or ((c[0] // gcd), c[1] // gcd) in seen:
                q1.pop(i)
            else:
                seen.append(((c[0] // gcd), c[1] // gcd))
                i += 1

        # print(q1)

        q1.sort(key=lambda coord: coord[1]/(coord[0] + 0.0000000001))
        # print(q1)

        count = 1
        j = 1
        while True:
            print("Rotation %d: count = %d" % (j, count))
            for config in [((-1, 1), False), ((1, 1), True), ((1, -1), False), ((-1, -1), True)]:
                q1.sort(key=lambda coord: coord[1] / (coord[0] + 0.0000000001), reverse=config[1])
                for c in q1[:-1]:
                    count = check_direction(inpt, start[0], start[1], c[0] * config[0][0], c[1] * config[0][1], count)
            # print(count)
            if count == astroids+1:
                break
            j += 1

        for line in inpt:
            print(["%s%s" % (x, "".join([" " for _ in range(3-len(x))])) for x in line])

        print(inpt[2][8])


if __name__ == '__main__':
    # main()
    part2()
