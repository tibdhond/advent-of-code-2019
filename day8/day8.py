from tkinter import *


class Layer:
    def __init__(self):
        self.grid = [[str(0) for _ in range(25)] for _ in range(6)]

    def __str__(self):
        str_grid = [" ".join(x) for x in self.grid]
        return "%s" % ("\n".join(str_grid))


def main():
    with open("input.txt", 'r') as f:
        inpt = f.readline()
        layer = Layer()
        layers = []
        x = 0
        y = 0

        for pixel in inpt:
            layer.grid[x][y] = pixel
            y += 1
            if y == 25:
                y = 0
                x += 1
                if x == 6:
                    layers.append(layer)
                    layer = Layer()
                    x = 0
                    y = 0

    final = Layer()
    layer_id = 0
    master = Tk()
    canvas_width = 25*10
    canvas_height = 6*10
    w = Canvas(master,
               width=canvas_width,
               height=canvas_height)
    w.pack()
    for row in range(6):
        for column in range(25):

            while layers[layer_id].grid[row][column] == "2":
                layer_id += 1

            final.grid[row][column] = layers[layer_id].grid[row][column]
            if final.grid[row][column] == "0":
                w.create_rectangle(column*10, row*10, column * 10+9, row * 10+9, fill="#000000")
            else:
                w.create_rectangle(column*10, row*10, column * 10+9, row * 10+9, fill="#ffffff")

            layer_id = 0

    print(final)
    master.mainloop()


if __name__ == '__main__':
    main()
