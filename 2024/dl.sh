#!/bin/bash

for i in {2..7}; do
	../aocsetup.sh 2024 ${i}
    # curl https://adventofcode.com/2024/day/${i}/input -A "bjoern@bjoern-winkler.de via curl" --cookie "session=53616c7465645f5f65481baee8754e8c68ce3ca4c9b91ecea745a85fff72fde9bdb3417c3ddc49bc24bb05231d5e4014cfd90ce19dc4fd14e2ffcc572752783a" > input/0${i}.txt
	# sleep 2
done
