rows = open('input.txt').read().split('\n')[:-1]


def part1():
    trees: [[int]] = [[int(col) for col in row] for row in rows]
    visibleTreesCount = 0
    for rowIdx, row in enumerate(trees):
        for colIdx, col in enumerate(row):
            tree = trees[rowIdx][colIdx]
            
            visibleFromTop = [tree > row[colIdx] for row in trees[:rowIdx]]
            visibleFromLeft = [tree > col for col in trees[rowIdx][:colIdx]]
            visibleFromRight = [tree > col for col in trees[rowIdx][colIdx + 1:]]
            visibleFromBottom = [tree > row[colIdx] for row in trees[rowIdx + 1:]]

            if any([all(visibleFromTop), all(visibleFromLeft), all(visibleFromRight), all(visibleFromBottom)]):
                visibleTreesCount += 1

    return visibleTreesCount


def part2():
    trees: [[int]] = [[int(col) for col in row] for row in rows]
    maxScore = 0
    for rowIdx, row in enumerate(trees):
        for colIdx, col in enumerate(row):
            tree = trees[rowIdx][colIdx]

            topCount = leftCount = rightCount = bottomCount = 0
            for topRowTree in trees[:rowIdx][::-1]:
                topCount += 1
                if tree <= topRowTree[colIdx]:
                    break
            for leftColTree in trees[rowIdx][:colIdx][::-1]:
                leftCount += 1
                if tree <= leftColTree:
                    break
            for rightColTree in trees[rowIdx][colIdx + 1:]:
                rightCount += 1
                if tree <= rightColTree:
                    break
            for bottomRowTree in trees[rowIdx + 1:]:
                bottomCount += 1
                if tree <= bottomRowTree[colIdx]:
                    break

            maxScore = max(maxScore, topCount * leftCount * rightCount * bottomCount)

    return maxScore


print(part1())
print(part2())
