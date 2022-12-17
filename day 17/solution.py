from enum import Enum
import os
import time

jetPattern = open('input.txt').read()


class Direction(Enum):
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'


rockShapes = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (0, 1), (1, 0), (1, 1)]
]


class Rock:
    def __init__(self, parts: [(int, int)], xOffset: int, yOffset: int):
        self.parts: [(int, int)] = [(x + xOffset, y + yOffset) for (x, y) in parts]

    def canMove(self, direction: Direction, fallenRocks: set['Rock']) -> bool:
        rockParts = []
        for rock in fallenRocks:
            rockParts.extend(rock.parts)

        if direction == Direction.DOWN:
            return all([(x, y - 1) not in rockParts for (x, y) in self.parts]) and self.getEdgePart(Direction.DOWN)[
                1] > 0
        elif direction == Direction.LEFT:
            return all([(x - 1, y) not in rockParts for (x, y) in self.parts]) and self.getEdgePart(Direction.LEFT)[
                0] > 0
        elif direction == Direction.RIGHT:
            return all([(x + 1, y) not in rockParts for (x, y) in self.parts]) and self.getEdgePart(Direction.RIGHT)[
                0] < 6

    def move(self, direction: Direction):
        if direction == Direction.DOWN:
            self.parts = [(x, y - 1) for (x, y) in self.parts]
        elif direction == Direction.LEFT:
            self.parts = [(x - 1, y) for (x, y) in self.parts]
        elif direction == Direction.RIGHT:
            self.parts = [(x + 1, y) for (x, y) in self.parts]

    def getEdgePart(self, direction: Direction) -> [(int, int)]:
        if direction == Direction.DOWN:
            return min(self.parts, key=lambda p: p[1])
        elif direction == Direction.LEFT:
            return min(self.parts, key=lambda p: p[0])
        elif direction == Direction.RIGHT:
            return max(self.parts, key=lambda p: p[0])


def part1(fallenRocksCap=2022):
    rockShapesIter = 0
    jetPatternIter = 0

    currentRock: Rock | None = None
    fallenRocks: set[Rock] = set()
    moveDirection: Direction = Direction.DOWN

    rockDropStartY = 4

    # for part 2 key: (shape, jetIter, position), value: height
    # cycleCache: dict[(int, int, (int, int)), (int, int, [int])] = {}
    # for part 2:
    # heights: [int] = []

    while len(fallenRocks) < fallenRocksCap:
        if currentRock is None:
            currentRock = Rock(rockShapes[rockShapesIter], 2, rockDropStartY)
            rockShapesIter = (rockShapesIter + 1) % len(rockShapes)

        match moveDirection:
            case Direction.DOWN:
                if currentRock.canMove(Direction.DOWN, fallenRocks):
                    currentRock.move(Direction.DOWN)
                    moveDirection = getNextSideMove(jetPattern, jetPatternIter)
                else:
                    fallenRocks.add(currentRock)
                    highestFallenRockY = getHighestFallenRockY(fallenRocks) + 1
                    rockDropStartY = highestFallenRockY + 4

                    # part 2 - find cycle
                    # fallenRocksX = min([p[0] for p in currentRock.parts])
                    # columnsMaxHeights = [0] * 7
                    # for rock in fallenRocks:
                    #     for (x, y) in rock.parts:
                    #         columnsMaxHeights[x] = max(columnsMaxHeights[x], y)
                    # columnsHeightsDiffs = [highestFallenRockY - columnsMaxHeights[x] for x in range(7)]
                    # cacheKey = (
                    #     rockShapesIter - 1,
                    #     jetPatternIter,
                    #     fallenRocksX,
                    #     frozenset(columnsHeightsDiffs)
                    # )

                    # if cacheKey not in cycleCache:
                    #     heights.append(highestFallenRockY)
                    #     cycleCache[cacheKey] = (highestFallenRockY, len(fallenRocks), heights)
                    # else:
                    #     cycleStartHighestY, startFallenRocksCount, heights = cycleCache[cacheKey]
                    #     print('minus', len(heights), heights)
                    #     cycleStepsHeights = [height - heights[startFallenRocksCount] for height in
                    #                          heights[startFallenRocksCount:]]
                    #     print(f'cycle found: {cycleStepsHeights}')
                    #
                    #     # cycleHeightIncrease = heights[-1] - heights[startFallenRocksCount - 1]
                    #     cycleHeightIncrease = highestFallenRockY - heights[startFallenRocksCount]
                    #     print(f'cycle height increase: {cycleHeightIncrease}')
                    #     rocksFallenDuringCycleCount = len(fallenRocks) - startFallenRocksCount - 1
                    #     print('cycle length', rocksFallenDuringCycleCount)
                    #     cyclesCount = (fallenRocksCap - startFallenRocksCount - 1) // rocksFallenDuringCycleCount
                    #     restRocksCount = (fallenRocksCap - startFallenRocksCount - 1) % rocksFallenDuringCycleCount
                    #
                    #
                    #     print('restRocksCount', restRocksCount)
                    #
                    #     return heights[startFallenRocksCount - 1] + cyclesCount * cycleHeightIncrease + \
                    #            cycleStepsHeights[restRocksCount]

                # part 1 animation
                #     nextRockShapes = Rock(rockShapes[rockShapesIter], 2, 0)
                #     drawFallenRocks(fallenRocks, rockDropStartY, nextRockShapes.parts)

                    currentRock = None
            case _:
                if currentRock.canMove(moveDirection, fallenRocks):
                    currentRock.move(moveDirection)
                moveDirection = Direction.DOWN
                jetPatternIter = (jetPatternIter + 1) % len(jetPattern)

    return getHighestFallenRockY(fallenRocks) + 1


def getNextSideMove(jetPattern: str, jetPatternIter: int) -> Direction:
    return Direction.LEFT if jetPattern[jetPatternIter] == '<' else Direction.RIGHT


def getHighestFallenRockY(fallenRocks: [Rock]) -> int:
    rockParts = []
    for rock in fallenRocks:
        rockParts.extend(rock.parts)
    return max(rockParts, key=lambda p: p[1])[1]


def drawFallenRocks(fallenRocks: [Rock], rockDropStartY, nextRock: [(int, int)]):
    os.system('clear')
    rocksParts = set()
    for rock in fallenRocks:
        rocksParts.update(rock.parts)

    maxRowsDrawn = 50
    y = rockDropStartY

    while y > 0 and maxRowsDrawn > 0:
        y -= 1
        maxRowsDrawn -= 1
        print('|', end='')
        for x in range(7):
            if (x, y) in rocksParts:
                print('█', end='')
            else:
                print('.', end='')
        print('|')

    print('\nFallen rocks count:', len(fallenRocks))
    for y in range(4, -1, -1):
        print('|', end='')
        for x in range(7):
            if (x, y) in nextRock:
                print('█', end='')
            else:
                print('.', end='')
        print('|')
    time.sleep(0.2)


print(part1())
