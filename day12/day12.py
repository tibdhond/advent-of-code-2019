import re
import math
import matplotlib.pyplot as plt


# def step(moons, state):
def step(moons):
    for i in range(len(moons)):
        for j in range(i+1, len(moons)):
            moon1 = moons[i]
            moon2 = moons[j]

            for k in range(3):
                distance = moon1[0][k] - moon2[0][k]
                if distance > 0:
                    moon1[1][k] -= 1
                    moon2[1][k] += 1
                elif distance < 0:
                    moon1[1][k] += 1
                    moon2[1][k] -= 1

    for moon in moons:
        moon[0] = [x + y for x, y in zip(moon[0], moon[1])]

    # state.append([moons[0][0][0], moons[0][0][1], moons[0][0][2]])


def part1():
    with open("input.txt", 'r') as f:
        inpt = f.readlines()
        moons = [[[int(x) for x in re.sub("[xyz<>=]", "", line.strip()).split(",")], [0, 0, 0]] for line in inpt]

        # print("Step 0: %s" % moons)
        # states = [[moons[0][0][0], moons[0][0][1], moons[0][0][2]]]
        for i in range(1000):
            # step(moons, states)
            step(moons)
            # print("Step %d: %s" % (i+1, moons))

        print(sum([sum([abs(x) for x in moon[0]]) * sum([abs(x) for x in moon[1]]) for moon in moons]))

        # plt.plot(states)
        # plt.show()


def step_alt(moons):
    for i in range(len(moons)):
        for j in range(i+1, len(moons)):
            moon1 = moons[i]
            moon2 = moons[j]

            distance = moon1[0] - moon2[0]
            if distance > 0:
                moon1[1] -= 1
                moon2[1] += 1
            elif distance < 0:
                moon1[1] += 1
                moon2[1] -= 1

    for moon in moons:
        moon[0] += moon[1]

    # print(tuple(moons))


def part2():
    with open("input.txt", 'r') as f:
        inpt = f.readlines()
        moons = [[[int(x) for x in re.sub("[xyz<>=]", "", line.strip()).split(",")], [0, 0, 0]] for line in inpt]

        x_state = [[list(x) for x in zip(moon[0], moon[1])][0] for moon in moons]
        x_states = {(tuple([tuple(x) for x in x_state])): 0}
        y_state = [[list(x) for x in zip(moon[0], moon[1])][1] for moon in moons]
        y_states = {(tuple([tuple(y) for y in y_state])): 0}
        z_state = [[list(x) for x in zip(moon[0], moon[1])][2] for moon in moons]
        z_states = {(tuple([tuple(z) for z in z_state])): 0}

        x_period = 0
        y_period = 0
        z_period = 0

        i = 1
        while not x_period or not y_period or not z_period:
            if x_period == 0:
                step_alt(x_state)
                x_tuple_form = (tuple([tuple(x) for x in x_state]))
                if x_tuple_form not in x_states:
                    x_states[x_tuple_form] = i
                else:
                    print("x offset: % d, x period: %d" % (x_states[x_tuple_form], i - x_states[x_tuple_form]))
                    x_period = i

            if y_period == 0:
                step_alt(y_state)
                y_tuple_form = (tuple([tuple(y) for y in y_state]))
                if y_tuple_form not in y_states:
                    y_states[y_tuple_form] = i
                else:
                    print("y offset: % d, y period: %d" % (y_states[y_tuple_form], i - y_states[y_tuple_form]))
                    y_period = i

            if z_period == 0:
                step_alt(z_state)
                z_tuple_form = (tuple([tuple(z) for z in z_state]))
                if z_tuple_form not in z_states:
                    z_states[z_tuple_form] = i
                else:
                    print("z offset: % d, z period: %d" % (z_states[z_tuple_form], i - z_states[z_tuple_form]))
                    z_period = i
            i += 1
        print(lcm(lcm(x_period, y_period), z_period))


def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()
