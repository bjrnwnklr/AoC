# https://www.hackerrank.com/challenges/re-sub-regex-substitution/problem?isFullScreen=true

# Doesnt capture overlapping patterns e.g. where one space between two patterns:
# ' || && ' -> will result in ' or && '

# Enter your code here. Read input from STDIN. Print output to STDOUT
import re


def logical_repl(matchobj):
    if matchobj.group(0) == " || ":
        return " or "
    else:
        return " and "


n = int(input().strip())

for _ in range(n):
    line = input().strip("\n")

    regex = r"\s(&&|\|\|)\s"
    new_line = re.sub(regex, logical_repl, line, count=0)
    print(new_line)
