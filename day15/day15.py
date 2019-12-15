import itertools
from PIL import Image
import random as r
import operator

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
    x = width // 2 + x * 10
    y = height // 2 + y * 10
    for i in range(x, x + 9):
        for j in range(y, y + 9):
            canvas.putpixel((i, j), (255, 255, 255))
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

    index = 0
    base = [0]

    width = 1000
    height = 1000
    canvas = Image.new("RGB", (width, height))
    frames = [paint_location(0, 0, width, height, canvas)]
    location = (0, 0)
    direction = 0
    last_directions = [-1]
    surroundings = {(0, 0): ["", "", "", ""]}
    direction_map = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    direction_to_code = ["1", "4", "2", "3"]

    status = 0

    try:
        with open("input.txt") as f:
            inp = f.read().split(",")
            while status != "2":
                stdin.append(direction_to_code[direction])
                execute(fmap, inp, index, base)
                status = stdout.pop(0)
                if status == "2":
                    break
                elif status == "0":
                    surroundings[location][direction] = "#"
                else:
                    surroundings[location][direction] = "."
                    canvas = paint_empty(location[1], location[0], width, height, frames[-1].copy())
                    location = tuple(map(operator.add, location, direction_map[direction]))
                    if location not in surroundings:
                        surroundings[location] = ["", "", "", ""]
                        last_directions.append((direction + 2) % 4)
                    surroundings[location][(direction + 2) % 4] = "."
                    frames.append(paint_location(location[1], location[0], width, height, canvas))
                if "" in surroundings[location]:
                    direction = (direction + 1) % 4
                    while surroundings[location][direction] != "":
                        direction = (direction + 1) % 4
                else:
                    direction = last_directions.pop(-1)
    except IndexError:
        print("Something went wrong")
        print(last_directions)
    finally:
        print("Target found! Took %d steps" % len(last_directions))
        print("Saving gif: %d frames" % len(frames))
        frames[0].save('breakout.gif', format='GIF', append_images=frames[1:], save_all=True, duration=1, loop=0)
        print("Gif saved!")


if __name__ == '__main__':
    main()
