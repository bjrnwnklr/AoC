def solve(wallPositions, wallHeights):

    last_wall = wallPositions[-1]
    all_wall_heights = {p: h for p, h in zip(wallPositions, wallHeights)}
    max_height = 0

    # iterate through each wall position
    for i in range(1, last_wall + 1):
        # check if brick wall
        if i in all_wall_heights:
            # we treat wallPositions as a queue and pop off an element once we find it
            assert i == wallPositions[0]
            wallPositions.pop(0)
            continue
        # otherwise, we need to build a mudwall
        # get left wall position (this is simply current - 1)
        left = i - 1
        # right wall is the first element in the wallPositions queue
        right = wallPositions[0]

        # get gap between walls
        wall_gap = right - left
        # get height gap between walls
        height_gap = all_wall_heights[right] - all_wall_heights[left]

        # if height gap is 0 or positive, build up
        if height_gap >= 0:
            all_wall_heights[i] = all_wall_heights[left] + 1

        # if height gap is negative, determine if we
        # - build up: wall_gap > abs(height_gap) + 1
        # - stay: wall_gap = abs(height_gap) + 1 (exactly one step above)
        # - build down: wall_gap <= abs(height_gap)
        else:
            wall_difference = wall_gap - abs(height_gap)
            if wall_difference > 1:
                delta = 1
            elif wall_difference == 1:
                delta = 0
            else:
                delta = -1
            all_wall_heights[i] = all_wall_heights[left] + delta

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
