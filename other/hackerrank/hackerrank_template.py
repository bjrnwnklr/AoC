# Hackerrank template
#
# Run by feeding test cases via stdin:
# python hackerrank_template.py < test_input_1.txt
#
# Link to riddle:
# https://www.hackerrank.com/challenges/journey-to-the-moon/problem?isFullScreen=true


def solution(parameter):
    pass


if __name__ == "__main__":

    # copy / paste this from the Hackerrank code
    n = int(input().strip())

    petrolpumps = []

    for _ in range(n):
        petrolpumps.append(list(map(int, input().rstrip().split())))

    result = solution(petrolpumps)

    # assert the solution
    assert result == 0
