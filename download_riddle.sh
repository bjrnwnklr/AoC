#!/bin/bash
url="https://adventofcode.com"
url_day="${url}/2022/day"

for i in {12..21}
do
        curl "${url_day}/${i}" > ${i}.html
done