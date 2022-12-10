signals = open('input.txt').read().split('\n')[:-1]

# Find the signal strength during the 20th, 60th, 100th, 140th, 180th, and 220th cycles.
# What is the sum of these six signal strengths?


def part1():
    cycleCount = 1
    signalIter = 0
    strengthsSum = [0]
    registryValue = 1

    while cycleCount <= 220:
        signalParts = signals[signalIter].split(' ')
        signalIter += 1

        if signalParts[0] == 'noop':
            tryAddSignalStrength(strengthsSum, cycleCount, registryValue)
            cycleCount += 1
            continue

        addValue = int(signalParts[1])
        for _ in range(2):
            tryAddSignalStrength(strengthsSum, cycleCount, registryValue)
            cycleCount += 1
        registryValue += addValue

    return strengthsSum[0]


def tryAddSignalStrength(strengthsSum: [int], cycleCount: int, signalStrength: int) -> None:
    if cycleCount not in [20, 60, 100, 140, 180, 220]:
        return
    strengthsSum[0] += (signalStrength * cycleCount)


def part2():
    cycleCount = 0
    signalIter = 0
    spriteMiddle = 1
    signalsCount = len(signals)

    while signalIter < signalsCount:
        signalParts = signals[signalIter].split(' ')
        signalIter += 1

        if signalParts[0] == 'noop':
            draw(cycleCount, spriteMiddle)
            cycleCount += 1
            continue

        addValue = int(signalParts[1])
        for _ in range(2):
            draw(cycleCount, spriteMiddle)
            cycleCount += 1
        spriteMiddle += addValue

    return cycleCount


def draw(cycleCount, spriteMiddle) -> None:
    positionInLine = cycleCount % 40
    if positionInLine == 0:
        print('\n', end='')
    if positionInLine in [spriteMiddle - 1, spriteMiddle, spriteMiddle + 1]:
        print('#', end='')
    else:
        print('.', end='')


print(part1())
print(part2())