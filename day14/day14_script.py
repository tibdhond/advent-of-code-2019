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

        chemical = requirements["FUEL"]
        result = get_requirements(requirements, leftovers, chemical, 1, "FUEL")
        print(leftovers)
        print([(key, value) for key, value in leftovers.items() if value > 0])
        for key, value in leftovers.items():
            if value >= int(requirements[key]["amount"]):
                print(key, value)

        return result


def get_requirements(requirements, leftovers, chemical, needed, name):
    ore = 0
    multiplier = 1
    new_leftovers = leftovers[name] - needed
    needed = max(0, needed - leftovers[name])
    leftovers[name] = max(0, new_leftovers)
    if needed > 0:
        while int(chemical["amount"]) * multiplier < needed:
            multiplier += 1

        leftovers[name] += int(chemical["amount"]) * multiplier - needed

        for requirement in chemical["requirement"]:
            if requirement[1] == "ORE":
                ore += int(requirement[0]) * multiplier
            else:
                next_chem = requirements[requirement[1]]
                ore += get_requirements(requirements, leftovers, next_chem,
                                        int(requirement[0]) * multiplier, requirement[1])
    else:
        print("No extra %s needed: %d" % (name, needed))
    return ore


def main():
    print(part1("input.txt"))


if __name__ == '__main__':
    main()
