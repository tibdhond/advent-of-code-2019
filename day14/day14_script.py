import math


def part1(file):
    with open(file, 'r') as f:
        requirements = {}
        leftovers = {}

        inpt = f.readline()

        while inpt:
            requirement, result = inpt.strip().split(" => ")
            requirement = [tuple(x.split(' ')) for x in requirement.split(', ')]
            result = result.split(' ')
            if result[1] in requirement:
                print(result[1])
            requirements[result[1]] = {'amount': result[0], "requirement": requirement}
            leftovers[result[1]] = 0
            inpt = f.readline()

        ore = 1000000000000
        fuel = 0
        fuel_check = ore // 10
        chemical = requirements["FUEL"]

        while ore > 0:
            result = get_requirements(requirements, leftovers, chemical, fuel_check, "FUEL")

            if fuel_check == 1 and ore - result < 0:
                break

            if ore - result > 0:
                ore -= result
                fuel += fuel_check
            else:
                fuel_check = fuel_check // 10

        return fuel


def get_requirements(requirements, leftovers, chemical, needed, name):
    ore = 0
    new_leftovers = leftovers[name] - needed
    needed = max(0, needed - leftovers[name])
    leftovers[name] = max(0, new_leftovers)
    if needed > 0:
        multiplier = int(math.ceil(needed / int(chemical["amount"])))

        leftovers[name] += int(chemical["amount"]) * multiplier - needed

        for requirement in chemical["requirement"]:
            if requirement[1] == "ORE":
                ore += int(requirement[0]) * multiplier
            else:
                next_chem = requirements[requirement[1]]
                ore += get_requirements(requirements, leftovers, next_chem,
                                        int(requirement[0]) * multiplier, requirement[1])
    return ore


def main():
    print(part1("test3.txt"))


if __name__ == '__main__':
    main()
