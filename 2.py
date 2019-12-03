def add(array, loc1, loc2, out):
    array[out] = int(array[loc1]) + int(array[loc2])


def mul(array, loc1, loc2, out):
    array[out] = int(array[loc1]) * int(array[loc2])


fmap = {1: add, 2: mul}


def execute(noun, verb):
    with open("2.input") as f:
        inp = f.read().split(",")
        code = int(inp[0])
        inp[1] = noun
        inp[2] = verb
        index = 0
        while code != 99 and index < len(inp):
            fmap.get(code)(inp, int(inp[index+1]), int(inp[index+2]), int(inp[index+3]))
            index += 4
            code = int(inp[index])
    return inp[0]

outp = 0
verb = 1
noun = 1
while verb < 99:
    noun = 1
    while noun < 99:
        outp = execute(noun, verb)
        if outp == 19690720:
            break
        noun += 1
    if outp == 19690720:
        break
    verb += 1

print(100 * noun + verb)
