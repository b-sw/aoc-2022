stacksRaw, stepsRaw = open('input.txt').read().split('\n\n')

def getStacks():
    stacksLevels = [
        stackElem.replace('    ', 'X').replace(' ', '').replace('[', '').replace(']', '')
        for stackElem in stacksRaw.split('\n')[:-1]
    ]
    stacks = [[] for _ in range(len(stacksLevels[0]))]
    for idx, stackLevel in enumerate(stacksLevels):
        for stackIdx, stackElem in enumerate(stackLevel):
            if stackElem == 'X':
                continue
            stacks[stackIdx].append(stackElem)
    return stacks

def getSteps():
    steps = [
        step.replace('move ', '').replace('from ', '').replace('to ', '').split(' ') for step in stepsRaw.split('\n')
    ]
    return steps


def part1():
    stacks = getStacks()
    steps = getSteps()

    for step in steps:
        quantity, fromStack, toStack = [int(stepPart) for stepPart in step]
        for _ in range(quantity):
            stacks[toStack - 1].insert(0, stacks[fromStack - 1].pop(0))
    return [stack[0] for stack in stacks]


def part2():
    stacks = getStacks()
    steps = getSteps()

    for step in steps:
        quantity, fromStack, toStack = [int(stepPart) for stepPart in step]
        stacks[toStack - 1] = stacks[fromStack - 1][:quantity] + stacks[toStack - 1]
        stacks[fromStack - 1] = stacks[fromStack - 1][quantity:]
    return [stack[0] if stack else '' for stack in stacks]


print(part1())
print(part2())