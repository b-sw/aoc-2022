steps = open('input.txt').read().splitlines()


class Node:
    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.next = next
        self.prev = prev


def getMixedNodesMap(initialSteps: [int], decryptionKey=1, mixesCount=1) -> dict[(int, int), Node]:
    head = Node(initialSteps[0])
    # can have repeated numbers so key is (value, index in the original list)
    nodesMap: dict[(int, int), Node] = {(head.value, 0): head}

    prev = head
    for idx, number in enumerate(initialSteps[1:]):
        node = Node(number * decryptionKey, prev)
        prev.next = node
        prev = node
        nodesMap[(number, idx + 1)] = node
    prev.next = head
    head.prev = prev

    for mixIter in range(mixesCount):
        print('Mixing', mixIter)
        for idx, number in enumerate(initialSteps):
            actualStep = (number * decryptionKey) % (len(initialSteps) - 1)
            node = nodesMap[(number, idx)]

            while actualStep > 0:
                actualStep -= 1
                next = node.next
                prev = node.prev

                next.next.prev = node
                prev.next = next

                node.next = next.next
                node.prev = next

                next.next = node
                next.prev = prev
    return nodesMap


def getDecryptionSum(initialSteps: [int], nodesMap: dict[(int, int), Node]) -> int:
    zeroNode = nodesMap[(0, initialSteps.index(0))]
    decryptionSum = 0
    for i in range(1, 3001):
        zeroNode = zeroNode.next
        if i % 1000 == 0:
            decryptionSum += zeroNode.value
    return decryptionSum


def part1():
    initialSteps = [int(step) for step in steps]
    nodesMap = getMixedNodesMap(initialSteps)
    return getDecryptionSum(initialSteps, nodesMap)


def part2():
    initialSteps = [int(step) for step in steps]
    nodesMap = getMixedNodesMap(initialSteps, 811589153, 10)
    return getDecryptionSum(initialSteps, nodesMap)


print(part1())
print(part2())
