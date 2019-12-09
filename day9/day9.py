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


def inp(array, index, params, base):
    value = input("Give input\n")
    array[get_value(array, index+1, params[-1], base[0])] = value
    return index + 2


def outp(array, index, params, base):
    # print("Output at index: %d" % index)
    print(array[get_value(array, index+1, params[-1], base[0])])
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


def execute(fmap):
    with open("input.txt") as f:
        inp = f.read().split(",")
        code = str(inp[0])
        code = code.zfill(5)
        index = 0
        base = [0]
        while code[-2:] != "99" and index < len(inp):
            index = fmap.get(code[-2:])(inp, index, code[:-2], base)
            code = inp[index]
            code = code.zfill(5)
    return inp[0]


def main():
    fmap = {"01": add, "02": mul, "03": inp, "04": outp, "05": jump_if_true, "06": jump_if_false,
            "07": less_than, "08": equals, "09": change_base}

    execute(fmap)


if __name__ == '__main__':
    main()
