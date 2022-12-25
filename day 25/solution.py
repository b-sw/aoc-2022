snafuNumbers = open('input.txt').read().splitlines()

snafu = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2
}


def solve():
    fuelSum = 0
    for snafuNumber in snafuNumbers:
        for digitIndex, snafuDigit in enumerate(reversed(snafuNumber)):
            fuelSum += (snafu[snafuDigit] * 5 ** digitIndex)

    snafuFuelSum = ''
    while fuelSum:
        snafuDigit = fuelSum % 5
        match snafuDigit:
            case 0:
                snafuFuelSum = '0' + snafuFuelSum
            case 1:
                snafuFuelSum = '1' + snafuFuelSum
                fuelSum -= 1
            case 2:
                snafuFuelSum = '2' + snafuFuelSum
                fuelSum -= 2
            case 3:
                snafuFuelSum = '=' + snafuFuelSum
                fuelSum += 2
            case 4:
                snafuFuelSum = '-' + snafuFuelSum
                fuelSum += 1
        fuelSum //= 5

    return snafuFuelSum


print(solve())
