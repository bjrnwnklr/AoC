# https://www.hackerrank.com/challenges/journey-to-the-moon/problem?isFullScreen=true


def journeyToMoon(n, astronaut):
    # create a queue of astronauts
    print(f"{astronaut=}")
    astros = list(range(n))
    astro_countries = {}
    country = 0
    for a, b in astronaut:
        if a not in astro_countries and b not in astro_countries:
            astro_countries[a] = country
            astro_countries[b] = country
            country += 1
            continue

        if a in astro_countries:
            astro_countries[b] = astro_countries[a]
        elif b in astro_countries:
            astro_countries[a] = astro_countries[b]

    # now process the remaining astronauts and assign a country
    while astros:
        a = astros.pop(0)
        if a in astro_countries:
            continue
        astro_countries[a] = country
        country += 1

    combos = set()
    for a in astro_countries:
        others = [
            b for b in astro_countries if astro_countries[b] != astro_countries[a]
        ]
        for o in others:
            combos.add(tuple(sorted([a, o])))

    print(f"Result: {len(combos)}")
    print(f"{astro_countries=}")
    print(f"{combos=}")
    return len(combos)


if __name__ == "__main__":

    # test case 1
    print("Test case 1")
    n = 5
    astronaut = [[0, 1], [2, 3], [0, 4]]

    result = journeyToMoon(n, astronaut)
    assert result == 6

    # test case 2
    print("Test case 2")
    n = 4
    astronaut = [[0, 2]]

    result = journeyToMoon(n, astronaut)
    assert result == 5

    # test case 3
    print("Test case 3")
    n = 10
    astronaut = [[0, 2], [1, 8], [1, 4], [2, 8], [2, 6], [3, 5], [6, 9]]

    result = journeyToMoon(n, astronaut)
    assert result == 23
