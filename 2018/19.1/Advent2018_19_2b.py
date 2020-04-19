target = 10551398
#target = 998

# sum up all factors (not just prime ones) of the target, including 1 and target

part2 = 1 + target + sum(x for x in range(2, target // 2 + 1) if not target % x)
print(part2)
