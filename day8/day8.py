from tkinter import *
from PIL import Image


class Layer:
    def __init__(self, width, height):
        self.grid = [[str(0) for _ in range(width)] for _ in range(height)]

    def __str__(self):
        str_grid = [" ".join(x) for x in self.grid]
        return "%s" % ("\n".join(str_grid))


def main():
    with open("input2.txt", 'r') as f:
        inpt = f.readline()
        width, height = [int(x) for x in inpt.strip().split('x')]
        inpt = f.readline()
        layer = Layer(width, height)
        layers = []
        x = 0
        y = 0

        for pixel in inpt:
            layer.grid[x][y] = pixel
            y += 1
            if y == width:
                y = 0
                x += 1
                if x == height:
                    layers.append(layer)
                    layer = Layer(width, height)
                    x = 0
                    y = 0

    final = Layer(width, height)
    layer_id = 0
    scale = 1
    canvas_width = width*scale
    canvas_height = height*scale
    canvas = Image.new("1", (canvas_width, canvas_height))
    for row in range(height):
        for column in range(width):

            while layers[layer_id].grid[row][column] == "2":
                layer_id += 1

            final.grid[row][column] = layers[layer_id].grid[row][column]
            canvas.putpixel((column, row), int(final.grid[row][column]))

            layer_id = 0

    print(final)
    canvas.save("result.png")


if __name__ == '__main__':
    main()
