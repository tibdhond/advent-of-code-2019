import math


def check_direction(grid, x, y, x_inc, y_inc):
    start_x = x
    start_y = y
    x += x_inc
    y += y_inc
    # print(start_x, start_y)
    while 0 <= x < len(grid) and 0 <= y < len(grid[x]):
        if grid[x][y] != '.':
            grid[start_x][start_y] = str(int(grid[start_x][start_y]) + 1)
            print("Visible for (%d, %d): (%d, %d)" % (start_x, start_y, x, y))
            break
        y += y_inc
        x += x_inc


def main():
    with open("input.txt", 'r') as f:
        inpt = [list(line.strip()) for line in f.readlines()]
        best = 0

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
                best = max(best, int(inpt[x][y]))
                y += 1
            x += 1

        for line in inpt:
            print(line)
        print(best)


if __name__ == '__main__':
    main()
