inputs = open('input.txt').read().split('\n\n')


def part1():
    indicesSum = 0
    pairs = []
    for idx, pair in enumerate(inputs):
        left, right = pair.split('\n')
        eval("pairs.append((" + left + ", " + right + "))")

    for idx, (left, right) in enumerate(pairs):
        if compare(left, right) < 0:
            indicesSum += idx + 1
    return indicesSum


def compare(left, right):
    match left, right:
        case int(), int():
            return left - right
        case list(), list():
            for l, r in zip(left, right):
                if r := compare(l, r):
                    return r
            else:
                return len(left) - len(right)
        case int(), list():
            return compare([left], right)
        case list(), int():
            return compare(left, [right])


def part2():
    packets = [[[2]], [[6]]]
    for idx, pair in enumerate(inputs):
        left, right = pair.split('\n')
        eval("packets.append(" + left + ")")
        eval("packets.append(" + right + ")")

    dividerPacketsIndices = 1
    for i in range(len(packets)):
        for j in range(1, len(packets) - i):
            if compare(packets[j], packets[j - 1]) < 0:
                packets[j - 1], packets[j] = packets[j], packets[j - 1]

    for idx, packet in enumerate(packets):
        if packet in [[[2]], [[6]]]:
            dividerPacketsIndices *= idx + 1

    return dividerPacketsIndices


print(part1())
print(part2())
