import itertools
from PIL import Image

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
    value1 = array[get_value(array, index+1, params[-1], base[0])]
    value2 = array[get_value(array, index+2, params[-2], base[0])]
    array[get_value(array, index+3, params[-3], base[0])] = str(int(value1) + int(value2))
    return index + 4


def mul(array, index, params, base):
    value1 = array[get_value(array, index+1, params[-1], base[0])]
    value2 = array[get_value(array, index+2, params[-2], base[0])]
    array[get_value(array, index+3, params[-3], base[0])] = str(int(value1) * int(value2))
    return index + 4


def read(array, index, params, base):
    global stdin
    if len(stdin) == 0:
        return -1
    value = stdin.pop(0)
    array[get_value(array, index+1, params[-1], base[0])] = value
    return index + 2


def write(array, index, params, base):
    global stdout
    # print("Output at index: %d" % index)
    stdout.append(array[get_value(array, index+1, params[-1], base[0])])
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
        array[get_value(array, index+3, params[-3], base[0])] = 1
    else:
        array[get_value(array, index+3, params[-3], base[0])] = 0
    return index + 4


def equals(array, index, params, base):
    value1 = array[get_value(array, index + 1, params[-1], base[0])]
    value2 = array[get_value(array, index + 2, params[-2], base[0])]

    if int(value1) == int(value2):
        array[get_value(array, index+3, params[-3], base[0])] = 1
    else:
        array[get_value(array, index+3, params[-3], base[0])] = 0

    return index + 4


def change_base(array, index, params, base):
    value = array[get_value(array, index+1, params[-1], base[0])]
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


def main():
    global stdin
    global stdout
    fmap = {"01": add, "02": mul, "03": read, "04": write, "05": jump_if_true, "06": jump_if_false,
            "07": less_than, "08": equals, "09": change_base}

    direction_map = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    location_map = {(0, 0): 2}

    width = 100
    height = 100
    canvas = Image.new("1", (width, height))

    index = 0
    base = [0]

    location = (0, 0)
    direction = 0

    stdin.append(location_map[location] & 1)

    with open("input.txt") as f:
        inp = f.read().split(",")
        while str(inp[index])[-2:] != "99":
            index = execute(fmap, inp, index, base)

            print(stdout)
            color = int(stdout.pop(0))
            if color != 1 and color != 0:
                raise ValueError("Wrong color value: %d" % color)
            print("Color: %d" % color)
            print("Location color: %d, New color: %d, Location &: %d, Color &: %d"
                  % (location_map[location], color, location_map[location] & 1, color & 1))
            if location_map[location] & 1 != color & 1:
                location_map[location] += 1
                canvas.putpixel((height//2+location[0], width//2-location[1]), location_map[location] & 1)

            rotation = int(stdout.pop(0))

            direction = (direction + 1) % 4 if rotation == 1 else (direction - 1) % 4
            location = (location[0] + direction_map[direction][0], location[1] + direction_map[direction][1])

            print(direction)
            print(rotation)
            print(location)

            if location not in location_map:
                location_map[location] = 2

            print(location_map[location] & 1 == 1)
            print()

            stdin.append(location_map[location] & 1)

        print(location_map)
        print(len(location_map))
        print([(k, len(list(v))) for k, v in itertools.groupby(sorted(location_map.values()))])

        canvas.save("result.png")


if __name__ == '__main__':
    main()
