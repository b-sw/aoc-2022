def roundsPicks():
    return [shapes.split(' ') for shapes in
            open('input.txt').read().split('\n')][:-1]

shapePoints = { 'X': 1, 'Y': 2, 'Z': 3, 'A': 1, 'B': 2, 'C': 3 }

def roundPoints(a: str, b: str):
    aScore = shapePoints[a]
    bScore = shapePoints[b]
    if aScore == bScore:
        return 3
    elif aScore > bScore and aScore - bScore == 1:
        return 6
    elif aScore < bScore and bScore - aScore == 2:
        return 6
    else:
        return 0

def part1():
    pointsSum = 0
    for [opponent, player] in roundsPicks():
        pointsSum += (roundPoints(player, opponent) + shapePoints[player])
    return pointsSum


tools = { 1: 'A', 2: 'B', 3: 'C' }
points = [3, 1, 2]

def shape(opponentShape: str, outcome: str):
    opponentPoints = shapePoints[opponentShape]
    if outcome == 'X':
        return tools[[3, 1, 2][opponentPoints - 1]]
    elif outcome == 'Y':
        return tools[opponentPoints]
    else:
        return tools[[0, 0, 2, 3, 1][opponentPoints + 1]]

def part2():
    pointsSum = 0
    for [opponent, outcome] in roundsPicks():
        player = shape(opponent, outcome)
        pointsSum += (roundPoints(player, opponent) + shapePoints[player])
    return pointsSum

print(part1())
print(part2())