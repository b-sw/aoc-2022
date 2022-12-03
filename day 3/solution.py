from typing import Set


def getRucksacks():
    return [_ for _ in
            open('input.txt').read().split('\n')][:-1]


def getItemPriority(item: str):
    if ord(item) <= 90:  # A-Z
        return ord(item) - 65 + 27
    else:
        return ord(item) - 97 + 1


def part1():
    prioritiesSum = 0
    rucksacks = getRucksacks()

    for rucksack in rucksacks:
        half = len(rucksack) // 2
        firstCompartment = set(rucksack[:half])
        secondCompartment = set(rucksack[half:])

        commonItems = firstCompartment & secondCompartment
        for item in commonItems:
            prioritiesSum += getItemPriority(item)

    return prioritiesSum


def part2():
    prioritiesSum = 0
    rucksacks = getRucksacks()

    for i in range(0, len(rucksacks), 3):
        groupRucksacks = rucksacks[i:i + 3]
        item = set(groupRucksacks[0]) & set(groupRucksacks[1]) & set(groupRucksacks[2])
        prioritiesSum += getItemPriority(list(item)[0])

    return prioritiesSum


print(part1())
print(part2())
