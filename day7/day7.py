from itertools import permutations

stdin = []


def add(array, index, params):
    value1 = array[int(array[index+1])] if params[-1] == "0" else array[index+1]
    value2 = array[int(array[index+2])] if params[-2] == "0" else array[index+2]
    array[int(array[index+3])] = str(int(value1) + int(value2))
    return index + 4


def mul(array, index, params):
    value1 = array[int(array[index+1])] if params[-1] == "0" else array[index+1]
    value2 = array[int(array[index+2])] if params[-2] == "0" else array[index+2]
    array[int(array[index+3])] = str(int(value1) * int(value2))
    return index + 4


def inp(array, index, _):
    global stdin
    # print("input: %s" % stdin)
    value = stdin.pop(0)
    array[int(array[index+1])] = value
    return index + 2


def outp(array, index, params):
    global stdin
    stdin.append(array[int(array[index+1])]) if params[-1] == "0" else print(array[index+1])
    # print("output: %s" % stdin)
    return index + 2


def jump_if_true(array, index, params):
    value1 = array[int(array[index+1])] if params[-1] == "0" else array[index+1]
    value2 = array[int(array[index+2])] if params[-2] == "0" else array[index+2]
    if int(value1) != 0:
        return int(value2)
    else:
        return index + 3


def jump_if_false(array, index, params):
    value1 = array[int(array[index+1])] if params[-1] == "0" else array[index+1]
    value2 = array[int(array[index+2])] if params[-2] == "0" else array[index+2]
    if int(value1) == 0:
        return int(value2)
    else:
        return index + 3


def less_than(array, index, params):
    value1 = array[int(array[index+1])] if params[-1] == "0" else array[index+1]
    value2 = array[int(array[index+2])] if params[-2] == "0" else array[index+2]

    if int(value1) < int(value2):
        array[int(array[index+3])] = 1
    else:
        array[int(array[index+3])] = 0
    return index + 4


def equals(array, index, params):
    value1 = array[int(array[index+1])] if params[-1] == "0" else array[index+1]
    value2 = array[int(array[index+2])] if params[-2] == "0" else array[index+2]

    if int(value1) == int(value2):
        array[int(array[index+3])] = 1
    else:
        array[int(array[index+3])] = 0

    return index + 4


def execute(fmap):
    with open("input.txt") as f:
        inp = f.read().split(",")
        code = str(inp[0])
        code = code.zfill(5)
        index = 0
        while code[-2:] != "99" and index < len(inp):
            index = fmap.get(code[-2:])(inp, index, code[:-2])
            code = inp[index]
            code = code.zfill(5)
    return inp[0]


def main():
    global stdin
    fmap = {"01": add, "02": mul, "03": inp, "04": outp, "05": jump_if_true, "06": jump_if_false,
            "07": less_than, "08": equals}

    best = 0

    all_phases = permutations("01234", 5)
    for phases in all_phases:
        stdin.append(0)
        for phase in phases:
            stdin.insert(0, phase)
            print("main: %s" % stdin)
            execute(fmap)
        print("main: %s" % stdin)
        best = max(int(stdin[0]), best)

        stdin = []

    print(best)


if __name__ == '__main__':
    main()
