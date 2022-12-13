def part1():
    start = end = (-1, -1)
    rows = open('input.txt').read().split('\n')[:-1]
    for idx, row in enumerate(rows):
        if start[1] == -1 and row.find('S') != -1:
            start = (idx, row.find('S'))
        if end[1] == -1 and row.find('E') != -1:
            end = (idx, row.find('E'))
    rows[start[0]] = rows[start[0]].replace('S', 'a')
    rows[end[0]] = rows[end[0]].replace('E', 'z')
    return bfs(rows, start, end)


def part2():
    start = end = (-1, -1)
    rows = open('input.txt').read().split('\n')[:-1]
    for idx, row in enumerate(rows):
        if start[1] == -1 and row.find('S') != -1:
            start = (idx, row.find('S'))
        if end[1] == -1 and row.find('E') != -1:
            end = (idx, row.find('E'))
    rows[start[0]] = rows[start[0]].replace('S', 'a')
    rows[end[0]] = rows[end[0]].replace('E', 'z')

    minSteps = float('inf')
    for rowIdx, row in enumerate(rows):
        for colIdx, col in enumerate(row):
            if col != 'a':
                continue
            minSteps = min(minSteps, bfs(rows, (rowIdx, colIdx), end))
    return minSteps


def bfs(grid, start, goal):
    rowsCount, colsCount = len(grid), len(grid[0])
    queue = [(0, start)]
    visited = set()
    while queue:
        distance, currentNode = queue.pop(0)
        if currentNode == goal:
            return distance

        if currentNode not in visited:
            visited.add(currentNode)
            for neighbour in getNeighbours(grid, currentNode, rowsCount, colsCount):
                if neighbour in visited:
                    continue
                queue.append((distance + 1, neighbour))
    return float('inf')


def getNeighbours(grid, currentNode, rowsCount, colsCount):
    currentRow, currentCol = currentNode
    maxHeight = ord(grid[currentRow][currentCol]) + 1

    neighbours = []
    for neighbourRow, neighbourCol in (
            (currentRow + 1, currentCol),
            (currentRow - 1, currentCol),
            (currentRow, currentCol + 1),
            (currentRow, currentCol - 1)
    ):
        if 0 <= neighbourRow < rowsCount and 0 <= neighbourCol < colsCount:
            if ord(grid[neighbourRow][neighbourCol]) <= maxHeight:
                neighbours.append((neighbourRow, neighbourCol))
    return neighbours


print(part1())
print(part2())