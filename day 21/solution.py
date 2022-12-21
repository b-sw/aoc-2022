yells = open('input.txt').read().splitlines()


class Monkey:
    def __init__(self, name: str):
        self.name = name
        self.value: int | None = None
        self.dependencies: (str, str) | None = None
        self.operation: str | None = None


def part1():
    monkeys = getMonkeys()
    return int(dfs(monkeys, 'root'))


def part2():
    monkeys = getMonkeys()
    monkeys['humn'].value = 1j
    rootDependencies = monkeys['root'].dependencies
    left = dfs(monkeys, rootDependencies[0])
    right = dfs(monkeys, rootDependencies[1])

    if left.imag:
        return int(((left - right) / left.imag).real * (-1))
    else:
        return int(((right - left) / right.imag).real * (-1))


def getMonkeys() -> dict[str, Monkey]:
    monkeys: dict[str, Monkey] = {}
    for yell in yells:
        yellParts = yell.split(' ')

        monkey = Monkey(yellParts[0][:-1])
        monkeys[monkey.name] = monkey

        if len(yellParts) < 3:
            monkey.value = int(yellParts[1])
        else:
            monkey.operation = yellParts[2]
            monkey.dependencies = (yellParts[1], yellParts[3])
    return monkeys


def dfs(monkeys: dict[str, Monkey], currentMonkey: str) -> None | int:
    if monkeys[currentMonkey].value:
        return monkeys[currentMonkey].value

    dependencyA, dependencyB = monkeys[currentMonkey].dependencies

    match monkeys[currentMonkey].operation:
        case '+':
            return dfs(monkeys, dependencyA) + dfs(monkeys, dependencyB)
        case '-':
            return dfs(monkeys, dependencyA) - dfs(monkeys, dependencyB)
        case '*':
            return dfs(monkeys, dependencyA) * dfs(monkeys, dependencyB)
        case '/':
            return dfs(monkeys, dependencyA) / dfs(monkeys, dependencyB)


print(part1())
print(part2())
