from math import prod

rawMonkeys = open('input.txt').read().split('\n\n')

class Monkey:
    def __init__(
            self,
            index: int,
            items: [int],
            operation: str,
            test: int,
            testPassMonkey: int,
            testFailMonkey: int
    ):
        self.index = index
        self.items = items
        self.test = test
        self.testPassMonkey = testPassMonkey
        self.testFailMonkey = testFailMonkey
        self.op, self.opArg = operation.split(' ')

    def addItem(self, item) -> None:
        self.items.append(item)

    def playTurn(self, monkeys, monkeyInspections: [int], divideWorry) -> None:
        lcm = prod(monkey.test for monkey in monkeys)
        while self.items:
            item = self.items.pop(0)
            opArg = item if self.opArg == 'old' else int(self.opArg)
            if self.op == '+':
                item = (item + opArg) // divideWorry
            else:
                item = (item * opArg) // divideWorry
            item %= lcm

            if item % self.test == 0:
                monkeys[self.testPassMonkey].addItem(item)
            else:
                monkeys[self.testFailMonkey].addItem(item)
            monkeyInspections[self.index] += 1


def part1(divideWorry=3, rounds=20):
    monkeys: [Monkey] = []
    for idx, rawMonkey in enumerate(rawMonkeys):
        monkeyProps = rawMonkey.split('\n')
        monkeyItems = [int(item) for item in monkeyProps[1][18:].split(', ')]
        monkeyOperation = monkeyProps[2][23:]
        monkeyTest = int(monkeyProps[3][21:])
        monkeyTestPassMonkey = int(monkeyProps[4][29:])
        monkeyTestFailMonkey = int(monkeyProps[5][30:])

        monkeys.append(Monkey(
            idx,
            monkeyItems,
            monkeyOperation,
            monkeyTest,
            monkeyTestPassMonkey,
            monkeyTestFailMonkey
        ))

    monkeyInspections = [0] * len(monkeys)
    for roundIdx in range(rounds):
        if roundIdx % 100 == 0:
            print(f'Round {roundIdx}')
        for monkey in monkeys:
            monkey.playTurn(monkeys, monkeyInspections, divideWorry)
    return monkeyInspections


def part2():
    return part1(divideWorry=1, rounds=10000)


a, b = sorted(part1(), reverse=True)[:2]
print(a * b)

a, b = sorted(part2(), reverse=True)[:2]
print(a * b)

