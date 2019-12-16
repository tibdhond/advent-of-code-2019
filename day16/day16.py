def part1():
    with open("input.txt", 'r') as f:
        inpt = [int(x) for x in f.readline()]
        pattern = [0, 1, 0, -1]

        for i in range(100):
            new_inp = []
            el = 0
            while len(new_inp) < len(inpt):
                # print("next el: %d " % el)
                multiplier = 1
                total = 0
                for number in inpt:
                    # print(multiplier//(el+1))
                    total += number * pattern[multiplier//(el+1)]
                    multiplier = (multiplier + 1) % (len(pattern) * (el+1))

                new_inp += [int(str(abs(total))[-1])]
                el += 1
            inpt = [x for x in new_inp]
        print(inpt)
        print("".join([str(x) for x in inpt[:8]]))


def part2():
    with open("input.txt", 'r') as f:
        inpt = [int(x) for x in f.readline()]
        message_index = int("".join([str(x) for x in inpt[:7]]))
        inpt = inpt * 10000
        inpt = inpt[message_index:]

        for i in range(100):
            print("Phase %d" % i)
            new_input = [sum(inpt)]
            el = 1
            while el < len(inpt):
                new_input.append(new_input[-1]-inpt[el-1])
                el += 1
            inpt = [int(str(x)[-1]) for x in new_input]

        print(int("".join([str(x) for x in inpt[:8]])))


def main():
    # part1()
    part2()


if __name__ == '__main__':
    main()
