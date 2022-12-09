moves = open('input.txt').read().split('\n')[:-1]


def part1():
    head = tail = (0, 0)
    tailVisited = set()

    for move in moves:
        direction = move[0]
        distance = int(move[1:])

        for _ in range(distance):
            prevHead = head
            if direction == 'U':
                head = (head[0], head[1] + 1)
            elif direction == 'D':
                head = (head[0], head[1] - 1)
            elif direction == 'L':
                head = (head[0] + 1, head[1])
            elif direction == 'R':
                head = (head[0] - 1, head[1])
            if abs(head[0] - tail[0]) == 2 or abs(head[1] - tail[1]) == 2:
                tail = prevHead
                tailVisited.add(tail)

    return len(tailVisited)


def part2():
    knots = [(0, 0) for _ in range(10)]
    tailVisited = set()

    for move in moves:
        direction = move[0]
        distance = int(move[1:])

        for _ in range(distance):
            if direction == 'U':
                knots[0] = (knots[0][0], knots[0][1] + 1)
            elif direction == 'D':
                knots[0] = (knots[0][0], knots[0][1] - 1)
            elif direction == 'L':
                knots[0] = (knots[0][0] + 1, knots[0][1])
            elif direction == 'R':
                knots[0] = (knots[0][0] - 1, knots[0][1])

            for i in range(1, len(knots)):
                xDiff = knots[i - 1][0] - knots[i][0]
                yDiff = knots[i - 1][1] - knots[i][1]
                if abs(xDiff) > 1 or abs(yDiff) > 1:
                    auxKnot = list(knots[i])
                    auxKnot[0] += (1 if xDiff > 0 else 0 if xDiff == 0 else -1)
                    auxKnot[1] += (1 if yDiff > 0 else 0 if yDiff == 0 else -1)
                    knots[i] = tuple(auxKnot)
            tailVisited.add(knots[-1])

    return len(tailVisited)


print(part1())
print(part2())