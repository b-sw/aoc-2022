import time
from copy import copy

lines = open('input.txt').read().split('\n')


class Node:
    def __init__(self, name: str, flow: int):
        self.name = name
        self.flow = flow
        self.neighbors = set()

    def addNeighbor(self, neighbor: 'Node'):
        self.neighbors.add(neighbor)



def part1():
    nodes = getGraph()
    time = 30
    return dfs(nodes, nodes['AA'], [], 0, time, {}, [])


def getGraph():
    nodes = {}
    for line in lines:
        lineParts = line.split(' ')
        name = lineParts[1]
        flow = int(lineParts[4][5:-1])
        neighborsNames = [name.replace(',', '') for name in lineParts[9:]]

        if name not in nodes:
            nodes[name] = Node(name, flow)
        else:
            nodes[name].flow = flow

        for neighborName in neighborsNames:
            if neighborName not in nodes:
                nodes[neighborName] = Node(neighborName, 0)
            nodes[name].addNeighbor(nodes[neighborName])
            nodes[neighborName].addNeighbor(nodes[name])
    return nodes


def dfs(nodes, node: Node, openedValves: [Node], pressureCount: int, timeLeft: int, cache: dict[(str, int, frozenset[str]), int], initiallyOpenedValves: [Node]) -> int:
    if (node.name, timeLeft, frozenset(openedValves)) in cache:
        return cache[(node.name, timeLeft, frozenset(openedValves))]

    pressureIncrease = sum([valve.flow for valve in openedValves])
    if timeLeft == 0:
        cache[(node.name, timeLeft, frozenset(openedValves))] = pressureIncrease
        return cache[(node.name, timeLeft, frozenset(openedValves))]

    neighborsVisits = []
    if node.flow > 0 and node not in openedValves and node not in initiallyOpenedValves:
        neighborsVisits.append(dfs(nodes, node, openedValves + [node], pressureIncrease, timeLeft - 1, cache, initiallyOpenedValves))
    for neighbor in node.neighbors:
        neighborsVisits.append(dfs(nodes, neighbor, openedValves, pressureIncrease, timeLeft - 1, cache, initiallyOpenedValves))

    cache[(node.name, timeLeft, frozenset(openedValves))] = pressureCount + max(neighborsVisits)

    return cache[(node.name, timeLeft, frozenset(openedValves))]

# only part 1
print(part1())

