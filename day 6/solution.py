sequence = open('input.txt').read()[:-1]


def part1():
    return searchUniqueSequence(4)


def part2():
    return searchUniqueSequence(14)


def searchUniqueSequence(length: int):
    for idx, char in enumerate(sequence):
        window = set(sequence[idx:idx + length])
        if len(window) != length:
            continue
        return idx + length


print(part1())
print(part2())