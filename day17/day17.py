import itertools
from PIL import Image
import random as r
import operator
import traceback

stdin = []
stdout = []


def pad_array(array, to):
    while to >= len(array):
        array.append(0)


def get_value(array, index, param, base):
    param_map = {"0": int(array[index]), "1": index, "2": base + int(array[index])}
    pointer = param_map[param]
    pad_array(array, pointer)
    return pointer


def add(array, index, params, base):
    value1 = array[get_value(array, index + 1, params[-1], base[0])]
    value2 = array[get_value(array, index + 2, params[-2], base[0])]
    array[get_value(array, index + 3, params[-3], base[0])] = str(int(value1) + int(value2))
    return index + 4


def mul(array, index, params, base):
    value1 = array[get_value(array, index + 1, params[-1], base[0])]
    value2 = array[get_value(array, index + 2, params[-2], base[0])]
    array[get_value(array, index + 3, params[-3], base[0])] = str(int(value1) * int(value2))
    return index + 4


def read(array, index, params, base):
    global stdin
    # print("Requesting input")
    if len(stdin) == 0:
        return -1
    value = stdin.pop(0)
    array[get_value(array, index + 1, params[-1], base[0])] = value
    return index + 2


def write(array, index, params, base):
    global stdout
    # print("Output at index: %d" % index)
    stdout.append(str(array[get_value(array, index + 1, params[-1], base[0])]))
    return index + 2


def jump_if_true(array, index, params, base):
    value1 = array[get_value(array, index + 1, params[-1], base[0])]
    value2 = array[get_value(array, index + 2, params[-2], base[0])]
    if int(value1) != 0:
        return int(value2)
    else:
        return index + 3


def jump_if_false(array, index, params, base):
    value1 = array[get_value(array, index + 1, params[-1], base[0])]
    value2 = array[get_value(array, index + 2, params[-2], base[0])]
    if int(value1) == 0:
        return int(value2)
    else:
        return index + 3


def less_than(array, index, params, base):
    value1 = array[get_value(array, index + 1, params[-1], base[0])]
    value2 = array[get_value(array, index + 2, params[-2], base[0])]

    if int(value1) < int(value2):
        array[get_value(array, index + 3, params[-3], base[0])] = 1
    else:
        array[get_value(array, index + 3, params[-3], base[0])] = 0
    return index + 4


def equals(array, index, params, base):
    value1 = array[get_value(array, index + 1, params[-1], base[0])]
    value2 = array[get_value(array, index + 2, params[-2], base[0])]

    if int(value1) == int(value2):
        array[get_value(array, index + 3, params[-3], base[0])] = 1
    else:
        array[get_value(array, index + 3, params[-3], base[0])] = 0

    return index + 4


def change_base(array, index, params, base):
    value = array[get_value(array, index + 1, params[-1], base[0])]
    base.append(base[0] + int(value))
    base.pop(0)
    # print("New base: %d" % base[0])

    return index + 2


def execute(fmap, inp, index, base):
    code = str(inp[index])
    code = code.zfill(5)
    while code[-2:] != "99" and index < len(inp):
        result = fmap.get(code[-2:])(inp, index, code[:-2], base)
        if result == -1:
            return index
        index = result
        code = inp[index]
        code = code.zfill(5)
    return index


def paint_empty(x, y, width, height, canvas):
    x = x * 10
    y = y * 10
    for i in range(x, x + 9):
        for j in range(y, y + 9):
            canvas.putpixel((i, j), (255, 255, 255))
    return canvas


def paint_intersect(x, y, width, height, canvas):
    x = x * 10
    y = y * 10
    for i in range(x, x + 9):
        for j in range(y, y + 9):
            canvas.putpixel((i, j), (255, 0, 0))
    return canvas


def paint_location(x, y, width, height, canvas):
    x = width // 2 + x * 10
    y = height // 2 + y * 10
    for i in range(x, x + 9):
        for j in range(y, y + 9):
            if i - x == j - y or (i - x) + (j - y) == 8 \
                    or y == j or y + 8 == j\
                    or x == i or x + 8 == i:
                canvas.putpixel((i, j), (255, 255, 255))
            else:
                canvas.putpixel((i, j), (0, 0, 0))
    return canvas


def main():
    global stdin
    global stdout
    fmap = {"01": add, "02": mul, "03": read, "04": write, "05": jump_if_true, "06": jump_if_false,
            "07": less_than, "08": equals, "09": change_base}

    # Intcode stuff, don't delete
    index = 0
    base = [0]

    width = 500
    height = 500
    canvas = Image.new("RGB", (width, height))
    frames = [canvas]

    grid = [[]]

    try:
        with open("input.txt") as f:
            inp = f.read().split(",")
            y = 0
            x = 0
            repeat = False
            while not repeat and inp[index] != "99":
                execute(fmap, inp, index, base)
                while len(stdout) > 0:
                    outp = stdout.pop(0)
                    if outp != "10":
                        if outp == "35":
                            grid[y].append("#")
                            frames.append(paint_empty(x, y, width, height, frames[-1].copy()))
                        elif outp == "46":
                            grid[y].append(".")
                        x += 1
                    else:
                        if len(grid[y]) == 0:
                            print("hit")
                            grid = grid[:-1]
                            repeat = True
                            break
                        grid.append([])
                        y += 1
                        x = 0
        alignment = 0
        frames[-1].save("Layout.png")
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == "#":
                    temp = 0
                    # print(i+1, len(grid), j, len(grid[i+1]))
                    if i + 1 < len(grid) and grid[i+1][j] == "#":
                        temp += 1
                    if i - 1 > 0 and grid[i-1][j] == "#":
                        temp += 1
                    if j + 1 < len(grid[i]) and grid[i][j+1] == "#":
                        temp += 1
                    if j - 1 > 0 and grid[i][j-1] == "#":
                        temp += 1
                    if temp >= 3:
                        frames.append(paint_intersect(j, i, width, height, frames[-1]))
                        alignment += i * j
        print(alignment)

    except Exception as e:
        print("Something went wrong")
        traceback.print_exc()
    finally:
        print("Saving gif: %d frames" % len(frames))
        frames[0].save('breakout.gif', format='GIF', append_images=frames[1:], save_all=True, duration=1, loop=0)
        print("Gif saved!")


if __name__ == '__main__':
    main()
