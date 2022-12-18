from enum import Enum

coordsLines = open('input.txt').read().splitlines()


class Side(Enum):
    LEFT = 0
    RIGHT = 1
    TOP = 2
    BOTTOM = 3
    FRONT = 4
    BACK = 5


class Droplet:
    def __init__(self, position: (int, int, int)):
        self.position = position
        self.sides = [True] * 6
        # for part 2
        self.neighbors: set[Droplet] = set()
        self.isUnreachable = True
        # @@@@@@@@@@

    def updateConnectedSides(self, cube: 'Droplet') -> None:
        selfX, selfY, selfZ = self.position
        cubeX, cubeY, cubeZ = cube.position

        if abs(selfX - cubeX) > 1 and abs(selfY - cubeY) > 1 and abs(selfZ - cubeZ) > 1:
            return

        if not any(self.sides):
            return

        if selfX == cubeX and selfY == cubeY and abs(selfZ - cubeZ) == 1:
            if selfZ > cubeZ:
                self.sides[Side.BACK.value] = False
                cube.sides[Side.FRONT.value] = False
            else:
                self.sides[Side.FRONT.value] = False
                cube.sides[Side.BACK.value] = False
            # for part 2
            self.neighbors.add(cube)
            cube.neighbors.add(self)
            # @@@@@@@@@@
        elif selfX == cubeX and selfZ == cubeZ and abs(selfY - cubeY) == 1:
            if selfY > cubeY:
                self.sides[Side.TOP.value] = False
                cube.sides[Side.BOTTOM.value] = False
            else:
                self.sides[Side.BOTTOM.value] = False
                cube.sides[Side.TOP.value] = False
            # for part 2
            self.neighbors.add(cube)
            cube.neighbors.add(self)
            # @@@@@@@@@@
        elif selfY == cubeY and selfZ == cubeZ and abs(selfX - cubeX) == 1:
            if selfX > cubeX:
                self.sides[Side.LEFT.value] = False
                cube.sides[Side.RIGHT.value] = False
            else:
                self.sides[Side.RIGHT.value] = False
                cube.sides[Side.LEFT.value] = False
            # for part 2
            self.neighbors.add(cube)
            cube.neighbors.add(self)
            # @@@@@@@@@@




def part1():
    droplets: [Droplet] = []
    for coords in coordsLines:
        x, y, z = [int(coord) for coord in coords.split(',')]
        newDroplet = Droplet((x, y, z))
        for droplet in droplets:
            droplet.updateConnectedSides(newDroplet)
        droplets.append(newDroplet)

    seenSidesCount = 0
    for droplet in droplets:
        seenSidesCount += sum(droplet.sides)
    return seenSidesCount


def part2():
    droplets: [Droplet] = []

    dropletsPositions: set[(int, int, int)] = set()
    xCoords: set[int] = set()
    yCoords: set[int] = set()
    zCoords: set[int] = set()

    for coords in coordsLines:
        x, y, z = [int(coord) for coord in coords.split(',')]

        dropletsPositions.add((x, y, z))
        xCoords.add(x)
        yCoords.add(y)
        zCoords.add(z)

        newDroplet = Droplet((x, y, z))
        for droplet in droplets:
            droplet.updateConnectedSides(newDroplet)
        droplets.append(newDroplet)

    airCubes: [Droplet] = []
    for x in range(min(xCoords), max(xCoords) + 1):
        for y in range(min(yCoords), max(yCoords) + 1):
            for z in range(min(zCoords), max(zCoords) + 1):
                if (x, y, z) in dropletsPositions:
                    continue
                newAirCube = Droplet((x, y, z))
                for airCube in airCubes:
                    airCube.updateConnectedSides(newAirCube)
                airCubes.append(newAirCube)

    for airCube in airCubes:
        if bfs(airCube, xCoords, yCoords, zCoords):
            airCube.isUnreachable = False

    seenSidesCount = 0
    unseenSidesCount = 0

    for droplet in droplets:
        seenSidesCount += sum(droplet.sides)
    for airCube in filter(lambda cube: cube.isUnreachable, airCubes):
        unseenSidesCount += sum(airCube.sides)

    return seenSidesCount - unseenSidesCount


def bfs(
        cube: Droplet,
        xCoords: set[int],
        yCoords: set[int],
        zCoords: set[int]
) -> bool:
    visited: set[Droplet] = set()
    queue: [Droplet] = [cube]
    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)

        currentX, currentY, currentZ = current.position
        minX, maxX = min(xCoords), max(xCoords)
        minY, maxY = min(yCoords), max(yCoords)
        minZ, maxZ = min(zCoords), max(zCoords)

        if currentX in [minX, maxX] or currentY in [minY, maxY] or currentZ in [minZ, maxZ]:
            return True
        queue.extend(current.neighbors)
    return False


print(part1())
print(part2())
