import re

edges = []
with open('input.txt') as f:
    for line in f.readlines():
            l, r = map(int, line.strip('\n').split('/'))
            edges.append((min(l, r), max(l, r)))


for e in sorted(edges):
    print(e)

