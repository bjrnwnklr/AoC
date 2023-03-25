# Hackerrank template
#
# Run by feeding test cases via stdin:
# python hackerrank_template.py < test_input_1.txt
#
# Link to riddle:
# https://www.hackerrank.com/challenges/truck-tour/problem?isFullScreen=true


def truckTour(petrolpumps):
    pump_count = len(petrolpumps)
    for n, _ in enumerate(petrolpumps):
        tank = 0
        stops = 0
        while tank >= 0 and stops < pump_count:
            next_pump = (n + stops) % pump_count
            tank = tank + petrolpumps[next_pump][0] - petrolpumps[next_pump][1]
            stops += 1
        if stops == pump_count:
            break

    return n


if __name__ == "__main__":

    # copy / paste this from the Hackerrank code
    n = int(input().strip())

    petrolpumps = []

    for _ in range(n):
        petrolpumps.append(list(map(int, input().rstrip().split())))

    result = truckTour(petrolpumps)
    print("Result: ", result)

    # assert the solution
    # test case 0
    # assert result == 1
    # test case 1
    assert result == 573
