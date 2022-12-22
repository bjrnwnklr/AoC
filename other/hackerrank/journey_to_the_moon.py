# https://www.hackerrank.com/challenges/journey-to-the-moon/problem?isFullScreen=true


def journeyToMoon(n, astronaut):
    print(f"{astronaut=}")
    astros = list(range(n))

    # create a bidirectional graph of astronauts
    # same country = same graph
    graph = {a: [] for a in astros}
    for a, b in astronaut:
        graph[a].append(b)
        graph[b].append(a)

    print(f"{graph=}")
    seen = set()
    groups = {}
    country = 0
    for node in graph:
        if node in seen:
            continue

        seen.add(node)

        # traverse graph from node and visit each connected node
        groups[country] = [node]
        q = graph[node][:]
        while q:
            next = q.pop()
            if next in seen:
                continue
            seen.add(next)
            groups[country].append(next)
            q.extend(graph[next][:])

        country += 1

    lengths = [len(d) for d in groups.values()]
    result = 0
    while lengths:
        l = lengths.pop()
        for other in lengths:
            result += l * other

    print(f"{groups=}")
    return result


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

    # test case 7
    # 11082889

    print("Test case 7")
    with open("journey_test_7.txt") as f:
        first_multiple_input = f.readline().rstrip().split()

        n = int(first_multiple_input[0])

        p = int(first_multiple_input[1])

        astronaut = []

        for _ in range(p):
            astronaut.append(list(map(int, f.readline().rstrip().split())))

    result = journeyToMoon(n, astronaut)
    assert result == 11082889

    # test case 11
    print("Test case 11")
    with open("journey_test_11.txt") as f:
        first_multiple_input = f.readline().rstrip().split()

        n = int(first_multiple_input[0])

        p = int(first_multiple_input[1])

        astronaut = []

        for _ in range(p):
            astronaut.append(list(map(int, f.readline().rstrip().split())))

    result = journeyToMoon(n, astronaut)
    assert result == 4999949998
