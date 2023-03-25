# https://www.hackerrank.com/challenges/piling-up/problem?isFullScreen=true

# Enter your code here. Read input from STDIN. Print output to STDOUT
t = int(input().strip())

for _ in range(t):
    n = int(input().strip())
    sides = list(map(int, input().strip().split()))

    # if left and right are different, we have to take the
    # bigger value as we will otherwise not be able to fit
    # the bigger value onto the top
    # if they are the same size, it doesn't matter which one
    # we take as we will have to stack both on top of each other
    # anyway

    current = 1_000_000_000_000
    result = "Yes"
    while sides:
        left = sides[0]
        right = sides[-1]
        # if left and right are bigger than the current
        # we can stop right here
        if current < left and current < right:
            result = "No"
            break

        # pick the bigger of the two, if both same, pick left
        if left >= right:
            if left <= current:
                current = sides.pop(0)
            else:
                result = "No"
                break
        else:
            if right <= current:
                current = sides.pop()
            else:
                result = "No"
                break

    print(result)
