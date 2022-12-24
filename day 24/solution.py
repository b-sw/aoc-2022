import math
import sys
from enum import Enum

sys.setrecursionlimit(10000)

labyrinthRows = open('input.txt').read().splitlines()
maxX, maxY = len(labyrinthRows[0]) - 3, len(labyrinthRows) - 3
soFarMin = float('inf')
snapshotsCount = math.lcm(len(labyrinthRows[0]) - 2, len(labyrinthRows) - 2)


class Direction(Enum):
    UP = '^'
    RIGHT = '>'
    DOWN = 'v'
    LEFT = '<'


class Blizzard:
    def __init__(self, x: int, y: int, direction: Direction):
        self.position = (x, y)
        self.direction = direction

    def move(self) -> None:
        match self.direction:
            case Direction.UP:
                self.position = (self.position[0], (self.position[1] - 1) % (maxY + 1))
            case Direction.RIGHT:
                self.position = ((self.position[0] + 1) % (maxX + 1), self.position[1])
            case Direction.DOWN:
                self.position = (self.position[0], (self.position[1] + 1) % (maxY + 1))
            case Direction.LEFT:
                self.position = ((self.position[0] - 1) % (maxX + 1), self.position[1])


def getLabrynthSnapshots() -> [[[int]]]:
    blizzards: set[Blizzard] = set()
    for y, row in enumerate(labyrinthRows[1:-1]):
        for x, tile in enumerate(row[1:-1]):
            if tile == '.':
                continue
            blizzards.add(Blizzard(x, y, Direction(tile)))

    labrynthSnapshots: [[[int]]] = [[row[1:-1] for row in labyrinthRows[1:-1]]]

    for _ in range(snapshotsCount - 1):
        newBlizzards: set[Blizzard] = set()
        for blizzard in blizzards:
            blizzard.move()
            newBlizzards.add(blizzard)
        blizzards = newBlizzards

        blizzardsCoords = set([blizzard.position for blizzard in blizzards])

        gridSnapshot: [[str]] = []
        for y in range(maxY + 1):
            rowSnapshot: [str] = []
            for x in range(maxX + 1):
                rowSnapshot.append('.' if (x, y) not in blizzardsCoords else '#')
            gridSnapshot.append(rowSnapshot)

        labrynthSnapshots.append(gridSnapshot)

    return labrynthSnapshots


def part1():
    gridSnapshots = getLabrynthSnapshots()
    return bfs(gridSnapshots, (0, -1), (maxX, maxY))


gridSnapshotIter = 1


def part2():
    gridSnapshots = getLabrynthSnapshots()
    startToEnd = bfs(gridSnapshots, (0, 0), (maxX, maxY))

    rearrangeIndex = startToEnd % snapshotsCount
    gridSnapshots = gridSnapshots[rearrangeIndex:] + gridSnapshots[:rearrangeIndex]
    endToStart = bfs(gridSnapshots, (maxX, maxY + 1), (0, 0))

    rearrangeIndex = endToStart % snapshotsCount
    gridSnapshots = gridSnapshots[rearrangeIndex:] + gridSnapshots[:rearrangeIndex]
    startToEnd2 = bfs(gridSnapshots, (0, -1), (maxX, maxY))

    return startToEnd + endToStart + startToEnd2


def bfs(gridSnapshots: [[[int]]], start: (int, int), goal: (int, int)) -> int:
    # (position, time)
    queue = [(start, 0)]
    # (position, time), prior time count
    visited: set[((int, int), int)] = set()

    minTimeCount: int = float('inf')

    while queue:
        position, time = queue.pop(0)

        if (position, time) in visited:
            continue

        visited.add((position, time % snapshotsCount))
        if time >= minTimeCount:
            continue

        if position == goal:
            minTimeCount = min(minTimeCount, time + 1)

        nextGridSnapshot = gridSnapshots[(time + 1) % len(gridSnapshots)]
        for nextPosition in getPossibleNextPositions(position, nextGridSnapshot, start):
            queue.append((nextPosition, time + 1))

    return minTimeCount


def getPossibleNextPositions(currentPosition: (int, int), gridSnapshot: [[int]], start: (int, int)) -> [
    ((int, int), int)]:
    possibleNextPositions: [(int, int)] = []

    # printGridSnapshot(nextGridSnapshot)

    for delta in [(0, -1), (1, 0), (0, 1), (-1, 0), (0, 0)]:
        nextX, nextY = currentPosition[0] + delta[0], currentPosition[1] + delta[1]

        if (nextX, nextY) == start:
            possibleNextPositions.append((nextX, nextY))
            continue
        if nextX < 0 or nextX > maxX or nextY < 0 or nextY > maxY:
            continue
        if gridSnapshot[nextY][nextX] != '.':
            continue
        possibleNextPositions.append((nextX, nextY))

    return possibleNextPositions


def printGridSnapshot(grid: [[str]]) -> None:
    for row in grid:
        print(''.join(row))
    print()


print('result 1', part1())
print('result 2', part2())
