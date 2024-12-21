#!/bin/bash

for i in {1..21}; do
	../aocsetup.sh 2024 ${i}
    # curl https://adventofcode.com/2024/day/${i}/input -A "bjoern@bjoern-winkler.de via curl" --cookie "session=" > input/${i}.txt
	# sleep 2
done
