def sums():
    return [sum(int(calories) for calories in elfCalories.split()) for elfCalories in
            open('input.txt').read().split('\n\n')]


def part1():
    return max(sums())


def part2():
    return sum(sorted(sums())[-3:])


print(part1())
print(part2())
