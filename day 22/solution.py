from enum import Enum

rows = open('input.txt').read().splitlines()


class Direction(Enum):
    LEFT = 'left',
    RIGHT = 'right',
    UP = 'up',
    DOWN = 'down'


class Tile:
    def __init__(self, x, y, isWall=False, neighbors=None):
        self.x = x
        self.y = y
        self.isWall = isWall
        self.neighbors: dict[Direction, Tile] or None = neighbors


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
            wrappedNeighborCoords = list(filter(lambda c: c[1] == node.y, list(nodes.keys()))).sort(key=lambda c: c[0])[
                -1]
            node.neighbors[Direction.LEFT] = nodes[wrappedNeighborCoords]

        # right
        if (node.x + 1, node.y) in nodes:
            node.neighbors[Direction.RIGHT] = (nodes[(node.x + 1, node.y)])
        else:
            print(node)
            wrappedNeighborCoords = list(filter(lambda c: c[1] == node.y, list(nodes.keys()))).sort(key=lambda c: c[0])[
                0]
            node.neighbors[Direction.RIGHT] = nodes[wrappedNeighborCoords]

        # up
        if (node.x, node.y - 1) in nodes:
            node.neighbors[Direction.UP] = (nodes[(node.x, node.y - 1)])
        else:
            wrappedNeighborCoords = list(filter(lambda c: c[0] == node.x, list(nodes.keys()))).sort(key=lambda c: c[1])[
                -1]
            node.neighbors[Direction.UP] = nodes[wrappedNeighborCoords]

        # down
        if (node.x, node.y + 1) in nodes:
            node.neighbors[Direction.DOWN] = (nodes[(node.x, node.y + 1)])
        else:
            wrappedNeighborCoords = list(filter(lambda c: c[0] == node.y, list(nodes.keys()))).sort(key=lambda c: c[1])[
                0]
            node.neighbors[Direction.DOWN] = nodes[wrappedNeighborCoords]

    return nodes


def part1():
    nodes = getNodes()
    return nodes


def part2():
    pass


print(part1())
print(part2())
