lines = open('input.txt').readlines()
Y = 2000000


def getMap() -> set[tuple[tuple[int, int], tuple[int, int]]]:
    sbPairs = set()
    for line in lines:
        lineParts = line.split(' ')
        sensorX, sensorY = int(lineParts[2][2:-1]), int(lineParts[3][2:-1])
        beaconX, beaconY = int(lineParts[8][2:-1]), int(lineParts[9][2:])
        sbPairs.add(((sensorX, sensorY), (int(beaconX), int(beaconY))))
    return sbPairs


def part1() -> int:
    sbPairs = getMap()
    sensors = set()
    beacons = set()
    for sensor, beacon in sbPairs:
        sensors.add(sensor)
        beacons.add(beacon)

    overlapSegments = []
    for idx, (sensor, beacon) in enumerate(sbPairs):
        sbDist = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])

        if not sensor[1] - sbDist <= Y <= sensor[1] + sbDist:
            continue
        overlapSegmentWidth = sbDist - abs(sensor[1] - Y)
        overlapSegments.append((sensor[0] - overlapSegmentWidth, sensor[0] + overlapSegmentWidth))
    overlapSegments.sort()

    invalidPositionsCount = 0
    head = overlapSegments[0][0]
    for xStart, xEnd in overlapSegments:
        if head < xStart:
            invalidPositionsCount += xEnd - xStart + 1
            head = xEnd
        elif head < xEnd:
            invalidPositionsCount += xEnd - head
            head = xEnd

    return invalidPositionsCount


def part2() -> int:
    sbPairs = getMap()
    for row in range(0, 4000000):
        # if row % 100000 == 0:
        #     print(row)
        overlapSegments = []
        for (sx, sy), (bx, by) in sbPairs:
            sbDist = (abs(sx - bx) + abs(sy - by))
            if sy - sbDist <= row <= sy + sbDist:
                segWidth = sbDist - abs(sy - row)
                overlapSegments.append((sx - segWidth, sx + segWidth))

        overlapSegments.sort()
        head = overlapSegments[0][0]
        for xStart, xEnd in overlapSegments:
            if head + 1 < xStart:
                return 4000000 * (head + 1) + row
            if head < xEnd:
                head = xEnd

    Exception('No solution found')


print(part1())
print(part2())
