#!/bin/bash

for i in {01..20}; do
    echo "${i}"
    python -m solutions.aoc2021_${i} | grep seconds | awk '{ print $6"s" }'
done