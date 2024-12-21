#!/bin/bash
url="https://adventofcode.com"
url_day="${url}/2024/day"

for i in {6..21}
do
        curl "${url_day}/${i}" > ${i}.html
        sleep 4
done
