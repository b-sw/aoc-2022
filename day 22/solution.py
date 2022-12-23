import re
from enum import Enum

rows = open('input.txt').read().splitlines()


class Direction(Enum):
    LEFT = 2
    RIGHT = 0
    UP = 3
    DOWN = 1


class Tile:
    def __init__(self, x, y, isWall=False):
        self.x = x
        self.y = y
        self.isWall = isWall
        self.neighbors: dict[Direction, Tile] or None = {}


def getNodes() -> dict[(int, int), Tile]:
    emptyTiles: set[(int, int)] = set()
    nodes: dict[tuple[int, int], Tile] = {}

    for rowIndex, row in enumerate(rows[:-2]):
        for colIndex, tileType in enumerate(row):
            if tileType == ' ':
                emptyTiles.add((colIndex, rowIndex))
            else:
                nodes[(colIndex, rowIndex)] = Tile(colIndex, rowIndex, tileType == '#')

    for node in nodes.values():
        # left
        if (node.x - 1, node.y) in nodes:
            node.neighbors[Direction.LEFT] = (nodes[(node.x - 1, node.y)])
        else:
            wrappedNeighborCoords = \
                sorted(list(filter(lambda c: c[1] == node.y, list(nodes.keys()))), key=lambda c: c[0])[
                    -1]
            node.neighbors[Direction.LEFT] = nodes[wrappedNeighborCoords]

        # right
        if (node.x + 1, node.y) in nodes:
            node.neighbors[Direction.RIGHT] = (nodes[(node.x + 1, node.y)])
        else:
            wrappedNeighborCoords = \
                sorted(list(filter(lambda c: c[1] == node.y, list(nodes.keys()))), key=lambda c: c[0])[
                    0]
            node.neighbors[Direction.RIGHT] = nodes[wrappedNeighborCoords]

        # up
        if (node.x, node.y - 1) in nodes:
            node.neighbors[Direction.UP] = (nodes[(node.x, node.y - 1)])
        else:
            wrappedNeighborCoords = \
                sorted(list(filter(lambda c: c[0] == node.x, list(nodes.keys()))), key=lambda c: c[1])[
                    -1]
            node.neighbors[Direction.UP] = nodes[wrappedNeighborCoords]

        # down
        if (node.x, node.y + 1) in nodes:
            node.neighbors[Direction.DOWN] = (nodes[(node.x, node.y + 1)])
        else:
            wrappedNeighborCoords = \
                sorted(list(filter(lambda c: c[0] == node.x, list(nodes.keys()))), key=lambda c: c[1])[
                    0]
            node.neighbors[Direction.DOWN] = nodes[wrappedNeighborCoords]

    return nodes


def part1():
    nodes: dict[(int, int), Tile] = getNodes()
    steps = re.split('(\d+)', rows[-1])[1:-1]

    currentNode: (int, int) = sorted(list(filter(lambda c: c[1] == 0, nodes.keys())), key=lambda c: c[0])[0]
    direction = Direction.RIGHT
    for step in steps:
        # print('before step', currentNode, step)
        if not step.isnumeric():
            direction = Direction((direction.value + 1) % 4) if step == 'R' else Direction((direction.value - 1) % 4)
            # print('new direction', direction)
            continue
        for _ in range(int(step)):
            if nodes[currentNode].neighbors[direction].isWall:
                # print('hit wall')
                break
            nextNode = nodes[currentNode].neighbors[direction]
            # print('moving', direction, nextNode.x, nextNode.y)
            currentNode = (nextNode.x, nextNode.y)
        # print('after step', currentNode)

    colIndex, rowIndex = currentNode
    print(currentNode)
    return 1000 * (rowIndex + 1) + 4 * (colIndex + 1) + direction.value


def part2():
    pass


print(part1())
print(part2())
