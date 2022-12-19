from enum import Enum

blueprints = open('input.txt').read().splitlines()


class Resource(Enum):
    ORE = 'ore'
    CLAY = 'clay'
    OBSIDIAN = 'obsidian'
    GEODE = 'geode'


def iterateBlueprints(time=24, availableBlueprints=blueprints) -> [(int, int)]:
    qualityLevels: [(int, int)] = []
    for idx, blueprint in enumerate(availableBlueprints):
        parts = blueprint.split(' ')
        oreRobotCost = {Resource.ORE: int(parts[6])}
        clayRobotCost = {Resource.ORE: int(parts[12])}
        obsidianRobotCost = {Resource.ORE: int(parts[18]), Resource.CLAY: int(parts[21])}
        geodeRobotCost = {Resource.ORE: int(parts[27]), Resource.OBSIDIAN: int(parts[30])}

        robotsCosts = {Resource.ORE: oreRobotCost, Resource.CLAY: clayRobotCost, Resource.OBSIDIAN: obsidianRobotCost,
                       Resource.GEODE: geodeRobotCost}

        qualityLevels.append((idx + 1, dfs(robotsCosts, {Resource.ORE: 1}, {}, time, {}, 0)))
        print('Blueprint', idx, 'done')

    return qualityLevels


def dfs(robotsCosts: dict[Resource, dict[Resource, int]], robots: dict[Resource, int], resources: dict[Resource, int],
        timeLeft: int, cache, maxGeodesFound: int) -> int:
    if timeLeft == 0:
        return resources.get(Resource.GEODE, 0)

    # if there can't be more geodes than current max, don't bother
    potentialMaxGeodesFound = resources.get(Resource.GEODE, 0) + (
            2 * (robots.get(Resource.GEODE, 0) + timeLeft - 1)) * timeLeft // 2
    if potentialMaxGeodesFound <= maxGeodesFound:
        return 0

    # if we've already seen this state, don't bother
    if (frozenset(robots.items()), frozenset(resources.items()), timeLeft) in cache:
        return cache[(frozenset(robots.items()), frozenset(resources.items()), timeLeft)]

    maxGeodesFound: int = 0
    initialResources = resources.copy()
    newResources = resources.copy()

    # produce resources
    for robotType, robotsCount in robots.items():
        newResources[robotType] = newResources.get(robotType, 0) + robotsCount

    # produce robots
    for robotType, robotCost in robotsCosts.items():
        # if no robot requires more resources of this type than we have robots, don't produce this robot
        if robotType is not Resource.GEODE and \
                all([requirements.get(robotType, 0) * timeLeft <= robots.get(robotType, 0) * timeLeft + resources.get(
                    robotType, 0) for requirements in robotsCosts.values()]):
            continue

        hasSufficientResources = True
        for costType, cost in robotCost.items():
            if initialResources.get(costType, 0) < cost:
                hasSufficientResources = False
                break
        if not hasSufficientResources:
            continue

        dfsResources = newResources.copy()
        dfsRobots = robots.copy()
        dfsRobots[robotType] = dfsRobots.get(robotType, 0) + 1
        for costType, cost in robotCost.items():
            dfsResources[costType] -= cost
        maxGeodesFound = max(maxGeodesFound,
                             (dfs(robotsCosts, dfsRobots, dfsResources, timeLeft - 1, cache, maxGeodesFound)))

    maxGeodesFound = max(maxGeodesFound, (dfs(robotsCosts, robots, newResources, timeLeft - 1, cache, maxGeodesFound)))

    cache[(frozenset(robots.items()), frozenset(resources.items()), timeLeft)] = maxGeodesFound
    return maxGeodesFound


def part1():
    qualityLevels = iterateBlueprints()
    print(qualityLevels)
    return sum([level[0] * level[1] for level in qualityLevels])


def part2():
    qualityLevels = iterateBlueprints(32, blueprints[:3])
    print(qualityLevels)
    return qualityLevels[0][1] * qualityLevels[1][1] * qualityLevels[2][1]


print(part1())
print(part2())
