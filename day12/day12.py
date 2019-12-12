import re


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


def main():
    with open("input.txt", 'r') as f:
        inpt = f.readlines()
        moons = []
        for line in inpt:
            moons.append([[int(x) for x in re.sub("[xyz<>=]", "", line.strip()).split(",")], [0, 0, 0]])

        print("Step 0: %s" % moons)
        for i in range(1000):
            step(moons)
            print("Step %d: %s" % (i+1, moons))

        print(sum([sum([abs(x) for x in moon[0]]) * sum([abs(x) for x in moon[1]]) for moon in moons]))


if __name__ == '__main__':
    main()
