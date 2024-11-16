#!/bin/bash

for i in {01..25}; do
    echo "${i}"
    python -m solutions.aoc2023_${i} | grep seconds | awk '{ print $6"s" }'
done