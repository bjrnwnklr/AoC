#!/bin/bash

for i in {21..22}; do
	# ../aocsetup.sh 2023 ${i}
	curl https://adventofcode.com/2023/day/${i}/input --cookie "session=53616c7465645f5f7e641a062ed6c955b3e46755fa72db6b98bd99d711ffb1b941d3503514b832dac982ee8a5e74ceb8c77087acabc460c992876a8c383ad288" > input/${i}.txt
	# sleep 1
	curl https://adventofcode.com/2023/day/${i} --cookie "session=53616c7465645f5f7e641a062ed6c955b3e46755fa72db6b98bd99d711ffb1b941d3503514b832dac982ee8a5e74ceb8c77087acabc460c992876a8c383ad288" > puzzles/${i}.html
	sleep 2
done
