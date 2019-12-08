import math


class Layer:
    def __init__(self):
        self.grid = [[str(0) for _ in range(25)] for _ in range(6)]
        self.zeros = 0
        self.ones = 0
        self.twos = 0

    def __str__(self):
        str_grid = [" ".join(x) for x in self.grid]
        return "Layer(%d, %d, %d)\n%s" % (self.zeros, self.ones, self.twos, "\n".join(str_grid))


def main():
    with open("input.txt", 'r') as f:
        inpt = f.readline()
        layer = Layer()
        layer_id = 0
        best_zeros = math.inf
        best_result = 0
        x = 0
        y = 0

        for pixel in inpt:
            if pixel == "0":
                layer.zeros += 1
            elif pixel == "1":
                layer.ones += 1
            elif pixel == "2":
                layer.twos += 1
            layer.grid[x][y] = pixel
            y += 1
            if y == 25:
                y = 0
                x += 1
                if x == 6:
                    if layer.zeros < best_zeros:
                        best_result = layer.ones * layer.twos
                        best_zeros = layer.zeros
                    print(layer)
                    layer = Layer()
                    layer_id += 1
                    x = 0
                    y = 0
    print(best_result)


if __name__ == '__main__':
    main()
