segments = open('input.txt').read().split('\n')

def part1():
    grid, xMin, xMax, yMax = getGrid()

    sandTilesCount = 0
    while sandTilesCount < len(grid) * len(grid[0]):
        tileX = 500 - xMin
        tileY = findLowestYInColumn(grid, tileX, 0)

        if tileX < 0 or tileX > xMax - xMin or tileY < 0 or tileY > yMax:
            break

        while grid[tileY + 1][tileX - 1] not in ['#', 'o'] or grid[tileY + 1][tileX + 1] not in ['#', 'o']:
            if grid[tileY + 1][tileX - 1] not in ['#', 'o']:
                tileX -= 1
                tileY = findLowestYInColumn(grid, tileX, tileY + 1)
            else:
                tileX += 1
                tileY = findLowestYInColumn(grid, tileX, tileY + 1)
            if tileX == 0 or tileX == xMax - xMin or tileY == 0 or tileY == yMax:
                return sandTilesCount
        grid[tileY][tileX] = 'o'
        sandTilesCount += 1

    return sandTilesCount


def part2():
    grid, minX, maxX, maxY = getGrid2()
    sandTiles = set()
    # drawGrid(grid, sandTiles)

    sandTilesCount = 0
    while True:
        tileX = 500
        for x in [tileX - 1, tileX, tileX + 1]:
            grid.add((x, maxY + 2))
        tileY = findLowestYInColumn2(grid, tileX, 0)

        if tileY == 0 and (tileX - 1, tileY + 1) in grid and (tileX + 1, tileY + 1) in grid:
            sandTiles.add((tileX, tileY))
            sandTilesCount += 1
            break
        while (tileX - 1, tileY + 1) not in grid or (tileX + 1, tileY + 1) not in grid:
            if (tileX - 1, tileY + 1) not in grid:
                tileX -= 1
            else:
                tileX += 1
            for x in [tileX - 1, tileX, tileX + 1]:
                grid.add((x, maxY + 2))
            tileY = findLowestYInColumn2(grid, tileX, tileY + 1)

        grid.add((tileX, tileY))
        sandTiles.add((tileX, tileY))
        sandTilesCount += 1
    # drawGrid(grid, sandTiles)
    return sandTilesCount


def drawGrid(grid: set[(int, int)], sandTiles: set[(int, int)]=None):
    minX = float('inf')
    maxX = maxY = 0
    for x, y in grid:
        minX = min(minX, x)
        maxX = max(maxX, x)
        maxY = max(maxY, y)

    for y in range(maxY + 1):
        for x in range(minX, maxX + 1):
            if sandTiles:
                if (x, y) in sandTiles:
                    print('o', end='')
                elif (x, y) in grid:
                    print('#', end='')
                else:
                    print('.', end='')
        print()


def findLowestYInColumn(grid, x, fromY):
    for y in range(fromY, len(grid)):
        if grid[y][x] in ['#', 'o']:
            return y - 1
    return float('inf')


def findLowestYInColumn2(grid: set[(int, int)], x, fromY):
    for y in range(fromY, len(grid)):
        if (x, y) in grid:
            return y - 1
    return float('inf')


def getGrid2() -> (set[(int, int)], int, int, int):
    grid = set()
    for segment in segments:
        points = [tuple(map(int, point.split(','))) for point in segment.split(' -> ')]
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    grid.add((x1, y))
            else:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    grid.add((x, y1))

    minX = float('inf')
    maxX = maxY = 0
    for x, y in grid:
        minX = min(minX, x)
        maxX = max(maxX, x)
        maxY = max(maxY, y)

    return grid, minX, maxX, maxY


def getGrid() -> [[str]]:
    minX = float('inf')
    maxX = maxY = 0
    for segment in segments:
        points = segment.split(' -> ')
        for point in points:
            x, y = map(int, point.split(','))
            minX = min(minX, x)
            maxX = max(maxX, x)
            maxY = max(maxY, y)

    grid = [['.' for _ in range(maxX - minX + 1)] for _ in range(maxY + 1)]
    grid[0][500 - minX] = '+'

    for segment in segments:
        points = [tuple(map(int, point.split(','))) for point in segment.split(' -> ')]
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    grid[y][x1 - minX] = '#'
            else:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    grid[y1][x - minX] = '#'
    return grid, minX, maxX, maxY


print(part1())
print(part2())

