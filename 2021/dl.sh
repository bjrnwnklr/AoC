#!/bin/bash

for i in {21..23}; do
	../aocsetup.sh 2021 ${i}
	curl https://adventofcode.com/2021/day/${i}/input --cookie "session=53616c7465645f5f58b5e33ca37677c1533e760352f12a2abffdb824483d7ec902266a88e062b8ee86fb2962354a04d0" > input/${i}.txt
	sleep 1
	curl https://adventofcode.com/2021/day/${i} --cookie "session=53616c7465645f5f58b5e33ca37677c1533e760352f12a2abffdb824483d7ec902266a88e062b8ee86fb2962354a04d0" > puzzles/${i}.html
	sleep 2
done
