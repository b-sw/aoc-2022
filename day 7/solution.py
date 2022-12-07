class Node:
    def __init__(self, parent=None, debugName=''):
        self.children = {}
        self.storage = 0
        self.parent = parent
        self.debugName = debugName


lines = open('input.txt').read().split('\n')[1:-1]


def buildTree() -> Node:
    root = Node(None, '/')
    currentNode: Node = root

    for line in lines:
        parts = line.split(' ')
        if parts[1] == 'ls':
            continue
        if parts[1] == 'cd' and parts[2] == '..':
            currentNode = currentNode.parent
            continue
        if parts[1] == 'cd':
            currentNode = currentNode.children[parts[2]]
            continue
        if parts[0] == 'dir':
            currentNode.children[parts[1]] = Node(currentNode, currentNode.debugName + parts[1] + '/')
            continue
        currentNode.storage += int(parts[0])

        parentNode = currentNode.parent
        while parentNode:
            parentNode.storage += int(parts[0])
            parentNode = parentNode.parent

    return root


def dfsPart1(root: Node, ans: [int]) -> None:
    ans += [root.storage if root.storage <= 100000 else 0]
    for child in root.children.values():
        dfsPart1(child, ans)


def part1():
    root = buildTree()
    ans = []
    dfsPart1(root, ans)
    return sum(ans)


def dfsPart2(root: Node, ans: [Node], spaceNeeded: int) -> None:
    for child in root.children.values():
        dfsPart2(child, ans, spaceNeeded)
    if root.storage >= spaceNeeded:
        ans[0] = root if root.storage < ans[0].storage else ans[0]


def part2():
    root = buildTree()
    spaceNeeded = 30000000 - (70000000 - root.storage)
    print('space needed', spaceNeeded)
    minNode = [root]
    dfsPart2(root, minNode, spaceNeeded)
    return minNode[0].storage


print(part1())
print(part2())
