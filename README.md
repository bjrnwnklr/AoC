# Advent of Code 2019

Working through the [2019 Advent of Code](https://adventofcode.com/2019) coding challenge.

## Python repos:

[Gabriel Kanegae](https://github.com/KanegaeGabriel/advent-of-code-2019)
[gengkev](https://github.com/gengkev/adventofcode-2019)
[fuglede](https://github.com/fuglede/adventofcode/tree/master/2019)
[JanneJP](https://github.com/JanneJP/Advent-of-Code-2019)
[Dementophobia](https://github.com/Dementophobia/advent-of-code-2019) - has some interesting summaries with tips&tricks

## Reddit solution megathreads

[Reddit 2019 solution megathreads](https://www.reddit.com/r/adventofcode/wiki/solution_megathreads#wiki_december_2019)

## Reddit help

1. Post code > 5 lines using github or [paste](https://topaz.github.io/paste/).

## Download input

You can download the day's input from this URL: https://adventofcode.com/2019/day/1/input

I will document each day's learnings (what was the specific challenge, what techniques / algorithms were used to resolve). This will help with future challenges.

Template:

# Day x

## Challenge

### Part 1

### Part 2

## Learnings

# Summaries

|  Day | Link               | Comments                                                                                                                                                                                                           |
| ---: | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
|    1 | [Day 1](2019_1.md) | Fuel levels. Using either iteration or recursion                                                                                                                                                                   |
|    2 | [Day 2](2019_2.md) | First appearane of `intcode` interpreter.                                                                                                                                                                          |
|    3 | [Day 3](2019_3.md) | Wires crossing. Using a Union between sets to find intersections. Solve part 2 by looking up index of intersection in a list; could have done also by adding number of steps into a dictionary for each gridpoint. |
|    4 | [Day 4](2019_4.md) | Finding number combinations. Some regex and clever comparisons                                                                                                                                                     |
|    5 | [Day 5](2019_5.md) | 2nd appearance of `intcode` interpreter. Some new instructions. `zfill` to pad strings with leading zeros!                                                                                                         |
|    6 | [Day 6](2019_6.md) | First graph problem. Use BFS to find shortest path. Some nice examples of using `networkx` library in the other solutions.                                                                                         |
|    7 | [Day 7](2019_7.md) | 3rd appearance of `intcode`. Introduced input and output queues and intcode machines running in a loop. Some interesting solutions to handle input / output queues using Exceptions / Interrupts                   |
| 8 | [Day 8](2019_8.md) | Get a password from an image file - easily solved using numpy. Best solution to not convert to 3 dimensional array, but use a 2 dimensional array and only convert to 3 dimensions at the end. |
| 9 | [Day 9](2019_9.md) | 4th appearance of `intcode`. Apparently now the machine is complete and no further modifications required. This version introduced relative mode, so had to be rewritten to use relative address pointers. Pretty happy with the solution now! **Final version of `intcode` computer!!!**|
| 10 | [Day 10](2019_10.md) | Find line of sight to asteroids. Use numpy to generate vectors and `np.arctan2` to get angle between vectors - then compare vectors to see which asteroids have line of sight of each other. First solution was slow as it checked all combinations of vectors if they have line of sight of each other - unnecessary as we only need to count number of unique angles. |
| 11 | [Day 11](2019_11.md) | Next `intcode` use... Create a robot that reads colors, runs intcode based on color input, then generates two outputs (paint output color and turn) and then moves by one square. Had to get the sequence of moves, inputs and outputs correct to work. In 2nd part, print the matrix of painted squares (dump defaultdict into a string and print each line) |
| 12 | [Day 12](2019_12.md) | Movement of 4 moons. Part 1 was almost trivial in simulating the movement of the moons. Part 2 was difficult as brute force wouldnt work to find the cycles where movements repeat. Had to find the cycles for each dimension independently and then take the Least Common Multiple (LCM) of the three. LCM didnt produce accurate result using `np.lcm`, so had to write own version using `math.gcd`.  |
| 13 | [Day 13](2019_13.md) | This was the most fun so far! `intcode` again, running a Breakout style arcade game. Part 2 was fun as it required to study the output of the intcode program and determine what you needed to solve. The surprisingly simple strategy of following the x position of the ball with the paddle (one line of code) effectively solves the game. |
| 14 | [Day 14](2019_14.md) | Again, a very fun day, really loved it! Converting ORE into FUEL using a complicated formula with dependencies. Both parts were fun. First part could be solved with _topological sort_, but I developed my own solution based on layers of the formula (performance was factor 10 slower than the topological sort, but still much faster than other solutions). Part 2 was solved by doing a binary search for target values. Some good learning and I have documented the topological sort and binary search patterns for further re-use. |
| 15 | [Day 15](2019_15.md) | Another `intcode` challenge. Directing a repair droid through a maze. Part 1 was solved by doing a BFS from the starting position to explore / map the maze. The difficulty was how to backtrack in BFS, but this can be done by storing the state of the intcode computer for each grid and retrieving it (using `copy.deepcopy` on the `Intcode` object to freeze the state). I had a lot of difficulties in getting this right as the BFS didn't seem to work, apparently it was a problem with storing the intcode state copy as part of the deque, so I used a dictionary instead (I suspect I got the actual location the intcode copy referred to wrong!). I also built an alternative that used a "right wall hugging" technique to map the maze, which could have then be used to run a BFS on the mapped grid (but didnt use it since I got the initial BFS to work). Part 2 was easily solved by generating a graph of valid neighbors in part 1 and using that to run a BFS from the oxygen source. The correct answer was the node with the longest path from the oxygen source. This was really easy once part 1 worked. |
| 16 | [Day 16](2019_16.md) | This was again a lot of fun. Fast Fourier Transformation of an input signal. Part 1 was fairly easy using Numpy as it is very efficient to calcuate dot products between matrices and vectors. Part 2 was really a lot of fun as it required some hard thinking about optimizing the solution (brute force would have taken forever!) Again, Numpy helped - fastest solution was using `np.cumsum` to generate the cumulative sum of the input signals very efficiently. |
| 17 | [Day 17](2019_17.md) |   |


cookie: 53616c7465645f5fef72a3265f626c2b8f72497f9e328be92389299523c8d085ceb7e291c9deebbffac116a25f69e85d
