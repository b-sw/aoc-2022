def getPairs():
    return [pair.split(',') for pair in
            open('input.txt').read().split('\n')][:-1]


def isWithinRange(b1, b2, a1, a2) -> bool:
    return b1 >= a1 and b2 <= a2


def overlaps(b1, b2, a1, a2) -> bool:
    if a1 <= b2 <= a2:
        return True
    if a1 <= b1 <= a2:
        return True
    return False


def part1() -> int:
    pairs = getPairs()
    rangesPairs = [(pair[0].split('-'), pair[1].split('-')) for pair in pairs]
    count = 0
    for elfA, elfB in rangesPairs:
        a1, a2 = int(elfA[0]), int(elfA[1])
        b1, b2 = int(elfB[0]), int(elfB[1])

        if isWithinRange(b1, b2, a1, a2) or isWithinRange(a1, a2, b1, b2):
            count += 1
    return count


def part2() -> int:
    pairs = getPairs()
    rangesPairs = [(pair[0].split('-'), pair[1].split('-')) for pair in pairs]
    count = 0
    for elfA, elfB in rangesPairs:
        a1, a2 = int(elfA[0]), int(elfA[1])
        b1, b2 = int(elfB[0]), int(elfB[1])

        if overlaps(b1, b2, a1, a2) or overlaps(a1, a2, b1, b2):
            count += 1
    return count


print(part1())
print(part2())
