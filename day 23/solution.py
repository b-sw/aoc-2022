import os
from enum import Enum

rows = open('input.txt').read().splitlines()
ROUNDS_COUNT = 10
DIRECTIONS_COUNT = 4


class Direction(Enum):
    NORTH = 0
    SOUTH = 1
    WEST = 2
    EAST = 3


class Elf:
    def __init__(self, x: int, y: int):
        self.position: (int, int) = (x, y)
        self.proposedMove: (int, int) or None = None

    def getProposedMove(self, elves: dict[(int, int), 'Elf'], startDirection: Direction) -> (int, int) or None:
        currentX, currentY = self.position
        if all([coord not in elves.keys() for coord in [
            (currentX - 1, currentY - 1), (currentX, currentY - 1), (currentX + 1, currentY - 1),
            (currentX - 1, currentY), (currentX + 1, currentY),
            (currentX - 1, currentY + 1), (currentX, currentY + 1), (currentX + 1, currentY + 1),
        ]]):
            self.proposedMove = None
            return self.proposedMove

        currentDirection = startDirection

        proposedMove: (int, int) or None = None
        for _ in range(DIRECTIONS_COUNT):
            match currentDirection:
                case Direction.NORTH:
                    if all([coord not in elves.keys() for coord in
                            [(currentX - 1, currentY - 1), (currentX, currentY - 1),
                             (currentX + 1, currentY - 1)]]):
                        proposedMove = (currentX, currentY - 1)
                        break
                case Direction.SOUTH:
                    if all([coord not in elves.keys() for coord in
                            [(currentX - 1, currentY + 1), (currentX, currentY + 1),
                             (currentX + 1, currentY + 1)]]):
                        proposedMove = (currentX, currentY + 1)
                        break
                case Direction.WEST:
                    if all([coord not in elves.keys() for coord in
                            [(currentX - 1, currentY - 1), (currentX - 1, currentY),
                             (currentX - 1, currentY + 1)]]):
                        proposedMove = (currentX - 1, currentY)
                        break
                case Direction.EAST:
                    if all([coord not in elves.keys() for coord in
                            [(currentX + 1, currentY - 1), (currentX + 1, currentY),
                             (currentX + 1, currentY + 1)]]):
                        proposedMove = (currentX + 1, currentY)
                        break
            currentDirection = Direction((currentDirection.value + 1) % DIRECTIONS_COUNT)
        self.proposedMove = proposedMove
        return self.proposedMove

    def tryMove(self, proposals: dict[(int, int), int]) -> None:
        if self.proposedMove and proposals[self.proposedMove] == 1:
            self.position = self.proposedMove


def getElves() -> dict[(int, int), Elf]:
    elves: dict[(int, int), Elf] = {}
    for rowIndex, row in enumerate(rows):
        for columnIndex, column in enumerate(row):
            if row[columnIndex] == '#':
                elves[(columnIndex, rowIndex)] = (Elf(columnIndex, rowIndex))
    return elves


def solve():
    elves: dict[(int, int), Elf] = getElves()
    startDirection = Direction.NORTH

    for roundIndex in range(1000000):
        # key: proposal coords, value: count of elves who proposed these coords
        proposals: dict[(int, int), int] = {}
        newElvesCoords: dict[(int, int), Elf] = {}

        for elfCoords, elf in elves.items():
            proposalCoords: (int, int) or None = elf.getProposedMove(elves, startDirection)
            if proposalCoords:
                proposals[proposalCoords] = proposals.get(proposalCoords, 0) + 1

        for elfCoords, elf in elves.items():
            elf.tryMove(proposals)
            newElvesCoords[elf.position] = elf

        startDirection = Direction((startDirection.value + 1) % DIRECTIONS_COUNT)

        if roundIndex == 10:
            elvesSortedX = sorted(list(elves.keys()), key=lambda k: k[0])
            elvesSortedY = sorted(list(elves.keys()), key=lambda k: k[1])
            minX, maxX = elvesSortedX[0][0], elvesSortedX[-1][0]
            minY, maxY = elvesSortedY[0][1], elvesSortedY[-1][1]
            print('Part1:', abs(maxX - minX + 1) * abs(maxY - minY + 1) - len(elves))

        if set(elves.keys()) == set(newElvesCoords.keys()):
            print('Part2:', roundIndex)
            return roundIndex + 1

        elves = newElvesCoords
        # printElves(elves)


def printElves(elves: dict[(int, int), Elf]) -> None:
    os.system('clear')
    elvesSortedX = sorted(list(elves.keys()), key=lambda k: k[0])
    elvesSortedY = sorted(list(elves.keys()), key=lambda k: k[1])
    minX, maxX = elvesSortedX[0][0], elvesSortedX[-1][0]
    minY, maxY = elvesSortedY[0][1], elvesSortedY[-1][1]

    for y in range(minY, maxY + 1):
        for x in range(minX, maxX + 1):
            if (x, y) in elves.keys():
                print('#', end='')
            else:
                print('.', end='')
        print()


solve()
