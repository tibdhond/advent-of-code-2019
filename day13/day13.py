import itertools
from PIL import Image
import random as r

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
    print("Requesting input")
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


def paint_empty(x, y, canvas):
    for i in range(x, x+3):
        for j in range(y, y+3):
            canvas.putpixel((i, j), (0, 0, 0))


def paint_wall(x, y, canvas):
    for i in range(x, x+3):
        for j in range(y, y+3):
            canvas.putpixel((i, j), (255, 255, 255))


def paint_block(x, y, canvas):
    red = r.randint(0, 255)
    green = r.randint(0, 255)
    blue = r.randint(0, 255)
    for i in range(x, x+3):
        for j in range(y, y+3):
            canvas.putpixel((i, j), (red, green, blue))
    canvas.putpixel((x+1, y+1), 0)


def paint_paddle(x, y, canvas):
    for j in range(x, x+3):
        canvas.putpixel((j, y), (255, 255, 255))


def paint_ball(x, y, canvas):
    canvas.putpixel((x+1, y+1), (255, 255, 255))


def main():
    frames = []
    global stdin
    global stdout
    fmap = {"01": add, "02": mul, "03": read, "04": write, "05": jump_if_true, "06": jump_if_false,
            "07": less_than, "08": equals, "09": change_base}
    paint_map = {"0": paint_empty, "1": paint_wall, "2": paint_block, "3": paint_paddle, "4": paint_ball}

    width = 126
    height = 72
    canvas = Image.new("RGB", (width, height))

    index = 0
    base = [0]

    max_x = 0
    max_y = 0
    blocks = 0
    score = 0
    ball_location = 0
    paddle_location = 0

    with open("input.txt") as f:
        inp = f.read().split(",")
        inp[0] = "2"
        while str(inp[index])[-2:] != "99":
            index = execute(fmap, inp, index, base)

            while len(stdout) > 0:
                y = int(stdout.pop(0))*3
                max_y = max(max_y, y+2)
                x = int(stdout.pop(0))*3
                max_x = max(max_x, x+2)
                id = stdout.pop(0)
                if y < 0 and x == 0:
                    score = int(id)
                else:
                    if id == "2":
                        blocks += 1
                    if id == "3":
                        paddle_location = y
                    if id == "4":
                        ball_location = y
                    paint_map[id](y, x, canvas)

                    frames.append(canvas.copy())
            joystick = 0
            if ball_location < paddle_location:
                joystick = -1
            elif ball_location > paddle_location:
                joystick = 1
            stdin.append(joystick)

        frames[0].save('breakout.gif', format='GIF', append_images=frames[1:], save_all=True, duration=10, loop=0)
        print(blocks)
        print(score)


if __name__ == '__main__':
    main()
