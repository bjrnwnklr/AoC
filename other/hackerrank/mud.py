def solve(wallPositions, wallHeights):
    print("Starting ---")

    last_wall = wallPositions[-1]
    all_wall_heights = {p: h for p, h in zip(wallPositions, wallHeights)}
    max_height = 0

    # iterate through each wall position
    for i in range(1, last_wall + 1):
        print(f"Checking wall: {i}")
        # check if brick wall
        if i in all_wall_heights:
            print(f"Wall found: {i}")
            continue
        # otherwise, we need to build a mudwall
        # get left wall position (this is simply current - 1)
        left = i - 1
        # get rigth wall position (count up until we find it)
        j = 1
        while (i + j) not in all_wall_heights:
            j += 1
        right = i + j
        print(f"Found left and right wall: {left} {right}")

        # get gap between walls
        wall_gap = right - left
        # get height gap between walls
        height_gap = all_wall_heights[right] - all_wall_heights[left]
        print(f"{wall_gap=}, {height_gap=}")

        # if height gap is 0 or positive, build up
        if height_gap >= 0:
            all_wall_heights[i] = all_wall_heights[left] + 1
            print(f"Building up: {i}: {all_wall_heights[i]}")

        # if height gap is negative, determine if we
        # - build up: wall_gap > abs(height_gap) + 1
        # - stay: wall_gap = abs(height_gap) + 1 (exactly one step above)
        # - build down: wall_gap <= abs(height_gap)
        else:
            if wall_gap > abs(height_gap) + 1:
                delta = 1
            elif wall_gap == abs(height_gap) + 1:
                delta = 0
            else:
                delta = -1
            all_wall_heights[i] = all_wall_heights[left] + delta
            print(f"Adding delta: {delta}, {i}: {all_wall_heights[i]}")

        # update max_height
        max_height = max(max_height, all_wall_heights[i])
    print(f"Max height = {max_height}")
    return max_height


if __name__ == "__main__":
    wallPositions = [1, 2, 4, 7]
    wallHeights = [4, 6, 8, 11]

    result = solve(wallPositions, wallHeights)

    assert result == 10

    wallPositions = [1, 5]
    wallHeights = [3, 3]

    result = solve(wallPositions, wallHeights)

    assert result == 5

    wallPositions = [1, 10]
    wallHeights = [3, 7]

    result = solve(wallPositions, wallHeights)

    assert result == 9
