class Satellite:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.orbits = []
        self.id_orbits = 0

    def __repr__(self):
        return "Satellite(%s, %s, %s, %d)" % (self.name, self.parent.name if self.parent else None,
                                              [sat.name for sat in self.orbits], self.id_orbits)


def main():
    satellite_map = {"COM": Satellite("COM")}
    with open("input.txt", 'r') as f:
        lines = f.readlines()
        for line in lines:
            satellites = line.strip().split(")")
            if satellites[0] in satellite_map:
                parent = satellite_map[satellites[0]]
            else:
                parent = Satellite(satellites[0])
                satellite_map[parent.name] = parent

            if satellites[1] in satellite_map:
                sat = satellite_map[satellites[1]]
            else:
                sat = Satellite(satellites[1])
                satellite_map[sat.name] = sat

            sat.parent = parent

            parent.orbits.append(sat)

    total = 0
    for satellite in satellite_map.values():
        next_sat = satellite.parent
        while next_sat is not None and next_sat.parent is not None:
            satellite.id_orbits += 1
            next_sat = next_sat.parent
            # print(next_sat)
        total += satellite.id_orbits + len(satellite.orbits)
        print(satellite)

    COM = satellite_map["COM"]
    print(total)


if __name__ == '__main__':
    main()
