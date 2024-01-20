# My Advent of Code 2023 notes

Documenting any interesting features, discoveries, concepts etc from the 2023 Advent of Code challenge.

# Day 1

-   Difficulty: Hard
-   Problem: String scanning / replacement / counting of numbers in a text

Part 1 was easy, could be done with regex our by just iterating through each line.

Part 2 was probably the hardest of any day 1 as the difficult cases ('oneight') where two numbers overlap were not covered in the examples. Resolved with forward looking regex; alternative would have been to replace each text number with a padded integer e.g. 'one' with 'o1e' to keep the first and last letter and hence preserve any overlapping numbers.

# Day 2

-   Difficulty: Easy
-   Problem: parsing the input (numbers, text), then calculating max values for each color (red, green, blue cubes)

Very easy, both parts easily parsed with regex and then just calculating max values

# Day 3

-   Difficulty: Medium
-   Problem: 2d grid with numbers and symbols. Each number adjacent to a symbol has special meaning. Parsing the numbers and symbols correctly

Part 1 was hard for day 3. Edge cases (number is at the end of the line) were not covered in the examples and I lost time here as I didn't handle the end of the line correctly, plus then had a +1 error for the end of line. Solved mostly with regex again, but parsing and finding adjacent symbols was also possible by just parsing each digit and looking for adjacent symbols individually.

# Day 4

-   Difficulty: Easy
-   Problem: Card game, simulating hands. Part 2 required only counting the resulting number of cards, not simulating each hand.

Parsing done with just splitting and converting to int. Part 2 increased the number of hands exponentially so if you tried simulating each hand (e.g. recursively), it would take **very** long. I just counted the cards instead of simulating (similar to the Lanternfish problem from a few years ago), which can be done in one pass. Very easy this way.

# Day 5

-   Difficulty: Hard
-   Problem: Seeds and recipes. Translate starting values (seeds) through a number of translations and then determine the lowest number. Solution for part 2 again expanded the problem space exponentially and required breaking the seed values into ranges and translating only the start and end of the range, but multiple times and splitting the range each time the next layer had multiple ranges.

This was probably the hardest problem up to day 8, very hard for the first week. Part 1 was easy, but part 2 required a different approach and breaking the seed numbers into ranges. My solution is quite ugly where I split the range into multiple ranges, this could be done much nicer:

```
       st-------end
            |----------|
       [---][-----][---]
       left  inner  right
```

where left and right could be width 0, depending if they overlap the interval on the left or right.

# Day 6

-   Difficulty: Easy
-   Problem: Racing boats - press button to charge. Calculate the number of times this wins. Both parts done with brute force (part 2 runs in 3 seconds)

This was very easy, even part 2 worked with brute force. Could have been solved with maths by calculating from lowest charging time (0) to the first win. Since the formula is linear, could have calculated from here at which point winning stops.

# Day 7

-   Difficulty: Easy
-   Problem: Poker simulation. Build a mechanism to calculate hand type (5 of a kind etc), then sort the results for tie-breaking.

Part 2 replaced J with jokers. Required minor adjustments and some additional sorting, but not a problem. Python `sorted` came in very handy.

# Day 8

-   Difficulty: Medium
-   Problem: Parsing (multiple lines, recipes like AAA= (BBB, CCC)). Part 2 required recognizing that the results repeat cyclicly and then using Least Common Multiple (LCM) or Chinese Remainder Theorem to calculate when all cycles converge.

Part 2 was hard if you tried to brute force. If you read the instructions correctly, it was already there - the examples had a very simple repeating pattern (one repeated every 2 cycles, the other every 3 - result was least common multiple 6) and the input instructions were also periodocally repeating.

I ran all individual replacements until they completed once, then wanted to see if they run the next cycle with the same length, but saw that all were looking like prime numbers and thought to just try LCM to find the lowest number of cycles where all replacements completed at the same time. Very similar to the Chinese Remainder Theorem problem from a few years ago (bus schedules).

Lots of people struggling with this one.

# Day 9

-   Difficulty: Easy
-   Problem: Calculate differences for a series of numbers, then predict the next or the previous number.

Could be solved with recursion, but did iteratively. Part 1 was easy to see that you just had to record the last number in each iteration and then add them up for the result (the next number in the series). Part 2 similar but required a slightly different calculation.

# Day 10

-   Difficulty: Hard
-   Problem: 2d grid with pipes and corners. BFS for part 1. Part 2 required BFS but also some additional preparation as gaps between pipes had to be recognized to find the inner and outer elements.

Part 2 was probably the hardest problem so far this year. Part 1 very easy with a BFS, just follow the loop from the start and count the steps. Result is the maximum number of steps.

Part 2 required recognizing where adjacent pipes form a gap. This had multiple possible ways of solving:

-   increase the grid resolution by translating from 1x1 tiles to 3x3 tiles, then using that with BFS to find the loop, then flood filling from the outside to find any outside tiles and using that to calculate the number of inner tiles.
-   scanline algorithm - BFS first to find the loop (part 1), then scan each line and count how often the pipes are crossed and form a U shape or not. This can then be used to calculate if a tile is inside or outside
-   raytracing - look in all directions from each non-loop tile and count how often pipes are crossed
-   walking the loop and painting left and right tiles in a different color. Then flood fill each section. Requires some way to recognize which color is inner and outer tiles.

After trying flood fill from the outside and building logic to find gaps in the pipes - which proved very difficult as there are many different combinations - i tried with increasing the grid resolution, which worked very well.

-   scale each tile to a 3x3 tile
-   keep a dictionary of the middle of each 3x3 tile, which we use to count visited tiles (this takes us back to the 1x1 grid)
-   replace the start S with the tile that fits - this was the most difficult calculation and required 6 different cases - some people hardcoded this and replaced S in their input
-   do a first BFS to find the loop of pipes
-   do a second BFS from the top left corner to fill all outside tiles. This now also works where you need to squeeze between parallel pipes
-   mark the middle of each visited tile
-   calculate the remaining tiles by subtracting the number of pipeloop tiles from the unmarked tiles

# Day 11

-   Difficulty: Easy
-   Problem: scan through a 2d grid to identify galaxies. If column or row is empty, add additional empty columns or rows. Part 2 added 1_000_000 rows, so simulating with brute force (expanding the grid before going through galaxies) would be very slow. Instead, calculate number of empty rows and just increase the coordinates of the galaxies accordingly.

# Day 12

-   Difficulty: Hard
-   Problem: Matching a pattern '???..###' with groups of numbers that represent '#'. '?' is a wildcard for either '.' or '#'. Groups of # need to be separated by '.'. Problem was hard because a brute force (trying all possible combinations where wild cards are substituted) takes a long time already for part 1, and is impossible for part 2 (e.g. combinations with 29 wildcards don't finish).

First used all possible combinations and then generated a regex that matched any valid configuration. This worked fine for part 1, but part 2 required multiplying the part 1 input times 5, so resulted in lots of possible combinations.

Then tried recursively parsing the string, which worked fine but was tricky to get all possible cases. Part 2 required memoization to make it perform ok. Solved in under 1 second.

# Day 13

-   Difficulty: Medium
-   Problem: Find symmetry (vertical / horizontal) in a grid of . and #. Part 2 required flipping one cell to the other value and then checking if any different reflection line was found. This was the hard part, but brute force (just iterating through all changes) worked well enough.

I probably overcomplicated the solution by:

-   calculating MD5 hash per row and column - instead of comparing each cell. but this was very fast.
-   part 2 got very complicated as i found that some examples just returned the same reflecting line as in part 1, so had to use lists of returned reflecting lines and compare these (there seem to be easier solutions but have not yet understood how they work)

# Day 14

-   Difficulty: Medium
-   Problem: Simulate tilting a surface so that rocks roll and stop either at the edge or at other rocks. Calculate weight by counting rocks per row. Part 2 required simulating this 1_000_000_000 times. As usual there was a repeating pattern, which was easy to find.

Did this with brute force by simulating rotating the platform and rolling the rocks, then store a string of the pattern of the rocks and look up if the same pattern was seen multiple times. Spend a lot of time on calculating the actual result, which could have been done manually by looking up the periodicity. I found the result by then iterating through possible starting offsets where the pattern repeats - there is likely a better way to calculate this, but it works.

Runtime for part 2 is almost 5 seconds, so could probably be improved.

# Day 15

-   Difficulty: Easy
-   Problem: build a hash function and an implementation of a hashmap / dictionary.

Part 1 was very easy - just calculate a simple hash value for a comma separated list. Part 2 was implementing a hashmap and required adding, replacing or removing elements from the lists stored in the hashmap without changing the order. Not difficult, only slighlty problematic as the items in each list are tuples and you had to find / replace based on the first tuple value. This required iterating through each element and compare if the first tuple value was the same, then popping the item at that index from the list or replacing it.

# Day 16

-   Difficulty: Easy
-   Problem: in a 2d grid, generate a beam that gets redirected or split into two depending on mirrors or splitters it hits. Calculate how many cells of the grid get hit by the beam(s).

This was easy to solve with a BFS that just added each new cell the beam travels to into the queue and then process what the next steps are (e.g. continue in current direction, redirect when hitting a mirror, split when hitting a splitter). The `seen` set can be used to stop going through cells we have already visited.

Part 2 required the same algorithm but with starting points from each cell on the edge of the grid. This was easy to do by just running the BFS from each edge cell and looking for the maximum of visited cells. Runs in 2.5s.

# Day 17

-   Difficulty: Medium
-   Problem: Shortest path in a weighted graph with additional constraints. Each grid cell has a number from 1-9 that is a movement penalty. Calculate the cheapest way to get from top left to bottom right. Constraints were that you have to turn left or right after 3 steps straight ahead (part 1), and that you need to move at least 4 steps before you can turn or stop (i.e. reach the end) and turn after a maximum of 10 steps straight.

This was easy to recognize as a case for Dijkstra's algorithm, with the states represented by a tuple of (r, c, number_steps_straight, current_direction). The neighbours in the graph could be represented by steps allowed under the constraints (only moving straight when number of steps allow it, turning if we have to etc). Part 2 was only marginally more difficult because of the condition that you can only stop after a minimum of 4 steps straight, so just another check to find the end.

Implementing Dijkstra without any further optimization worked well on the examples but did not finish on the puzzle. Optimization was required by only adding next steps that allowed to reach a given cell if it was cheaper than previously seen. This could be done by keeping a defaultdict with the penalty to reach that cell with a number of steps straight from a given direction.

# Day 18

-   Difficulty: Hard
-   Problem: Measure the area contained by a wall in a 2d grid. Part 2 was exactly the same but on a much larger scale.

Part 1 was relatively easy to solve by creating the wall elements and then either using scanline or a flood fill to calculate the inner area. Scanline took me a while to implement but worked ok.

Part 2 made the dimensions of the grid so much bigger that brute force did not work. However the count of the nodes did not increase, just the distance.

Using the Shoelace formula you can calculate the area contained within the nodes, however this does not give the correct answer as it calculates the exact area in a cartesian grid, but does not account for the walls.

Using Pick's theorem, you can account half of the size of the walls as additional area, plus add one for the last closing piece of the wall. This gives the correct answer.

Hardest puzzle so far?

# Day 19

-   Difficulty: Easy - Medium
-   Problem: Some complex parsing of workflow rules (name{s<1423:hdj,m>12,A}) and attributs of machine parts (dictionary of keys and int values). Required a bit of parsing gymnastics. Part 1: run each part through the workflow, either ending in Accepted or Rejected. Sum up the parts that were accepted. Part 2: The same, but instead of parts, calculate the number of possible combinations that will be accepted from 4000\*\*4 possible combinations of values, so not possible to use brute force.

Easily solved both parts with a recursive function. Part 1 worked immediately; part 2 used the same solution as day 5, where you split the intervals of possible values into smaller intervals that you process further. Worked on first try with the recursive function. No memoization required either. Very easy for day 19.

# Day 20

-   Difficulty: Medium - Hard
-   Problem: build a virtual computer with flip-flop memory and registers. For part 1, count how many pulses / signals are sent between flipflops and registers. For part 2, calculate when a register was flipped from 0 to 1. This could not be simulated as it required a lot of cycles.

Part 1 was easy but the text was very complicated. My solution is probably a bit over engineered with a full simulation of the virtual computer, which was not really required. The brute force solution runs in well under 1 second to find the solution by just simulating the memory state of the machine and counting the number of pulses.

Part 2 was more complicated, but in the end very simple to resolve. By looking at the input, you could see that the final register depends on 4 different registers, which each get fed by 8 (3 of them) or 11 (1 of them) flipflops. The flipflops change status each cycle and can be ordered to show they are counting up binary numbers.

The solution was simply finding the first time each of the 4 registers sent a High pulse (i.e. all flipflops were 1) to the target register, then taking the Least Common Multiple (LCM) of the 4 values.

I also logged a lot more than required and found the correct order for all of the flipflops to show they are counting up. I also proved that the 4 registers hit HIGH on fixed cycles, but the first value is already enough.

This was a fun problem with ultimately a very simple solution. Great that we had to analyze the input to get to the solution - first time this year.

# Day 21

-   Difficulty: HARD!!!!
-   Problem: a 2d grid with rocks and unoccupied patches. Part 1: find all possible positions that can be reached in a given number of steps. Part 2: the grid can be expanded infinitely by copying the existing grid onto each side. Find the number of positions that can be reached in a ridiculously high number of steps.

Part 1: solved with BFS by observing that each position can be reached only in a even number of steps (because of backtracking - we can just step back and forth a number of times).

Part 2: very hard, didnt solve. I observed that the input square has the same side lengths, and that there is a highway of open positions from the middle (starting position) to each of the four sides. So you can reach each adjacent tile by just stepping along the middle. Once you reach an adjacent tile, you can reach the same number of positions as you can originally reach.

But didnt manage to solve the puzzle and used an answer from Reddit: [Python solution](https://topaz.github.io/paste/#XQAAAQDcAQAAAAAAAAAjiAOiE/kRLeQB1cGmfHakawz7UqVcDEZjf/KvIQv859I/42EN77Dcrnn9OX4FZv4wI5s+SrfDTO0LC2XuzGLqJC3wjkKvWuB2LyCUL9Z0QcLJrFUbwmkf77Xq5P/O0E/YvoPpuiZVCOiCrdCJbvp5VBGgQUq2W/lUzZg+PHeNUjAlNFqvlj1jujOY0TpNzYDQdntQcWEhTSTAtYFxi522TTRfEu4jFlD9SPQXH0epmzLFNfOh2NWtcKCsG9fOG+xMPub2Q02v/lxdMrdGjzPz5itqxUavxBQUUZd1UnLEYxPfyqSEEx6u74yM0rCaLDvdDY8CXPWhAd3CvQbHWN3SdWFhoZdao7GALjuB/fO2t5EIT+rTCSJ7japFhWfDagOF31XVKofp2eYnwA0NM3EE3dcDqv7RYc8=)

This was by far the hardest puzzle so far.

RETRY part 2 with the diamond solution - see notes. Finish in January.
https://www.reddit.com/r/adventofcode/comments/18o4y0m/2023_day_21_part_2_algebraic_solution_using_only/

# Day 22

-   Difficulty: Medium
-   Problem: Jenga - bricks falling down in a 3d grid. Bricks are described by their 3 corners and can stretch in 1 dimension. Part 1: Determine how bricks fall and come to rest. Then determine which of the bricks can be removed without impacting the bricks above (i.e. the brick is still supported by another brick). Part 2: Determine how many bricks would fall if any one brick was removed.

Part 1 was easy:

-   sort bricks by their z coordinate so we can process them from bottom to top. Then calculate all x/y coordinates occupied by the brick. Then check from current z height downwards if the brick would fit. This was easily done with a defaultdict storing the x/y/z coordinates of the grid. To determine dependencies, use two dictionaries for a bi-directional graph: depends_on and supported_by. Using the dictionaries, it was easy to see which bricks cannot be removed as they are the only brick supporting another brick.

Part 2 was not much more difficult:

-   Use solution from part 1
-   then use a BFS for each brick to be removed and remove the brick from the list of bricks the brick depends on. Once a brick has no more dependencies, it will fall down, so add to queue.
-   Part 2 took 5 seconds to run, could possibly be optimized with memoization - check if removing a brick was already seen to cause other bricks to fall?

# Day 23

-   Difficulty: Hard
-   Problem: 2d grid with walls and floor, and additionally slopes that can only be passed in one direction. Part 1: find the LONGEST path from start to end while only passing the slopes in the one allowed direction. Part 2: find the LONGEST path but ignore the slope direction.

Part 1 was easily done with BFS (bit slower) and Dijkstra (1.5s).

Part 2 was difficult as the grids had some intersections that didnt work with the Dijkstra algorithm as it would never evaluate them as they were shorter than the path to another grid, but resulting in an overall longer path. So tried BFS but this ran much too long without finishing.

The intersections were special in that each of them was surrounded by slopes. So we could build a much smaller graph by just using the intersections as nodes. This resulted in a graph with ca 30 nodes. BFS found all possible paths within 73 seconds. Slow, but worked.

# Day 24

-   Difficulty: Hard
-   Problem: Find intersections between trajectories of hailstones, defined by a x,y,z starting position and vx, vy, vz velocities. Part 1 required to find if any two of the hailstones have intersecting trajectories. Part 2 required to find starting x, y and z values for a rock that is thrown from the position at a velocity and hits all hailstones on it's way.

Part 1 was fairly easy again. A closed form could be found by resolving the equations given by the linear trajectories for each coordinate. This required transforming the parameterized equations (one equation for x, y each) into one rectangular (cartesian) equation f(x) = y = px + vx \* x

Part 2 was very hard. I tried with multiple equations e.g. since the rock travels at a constant speed, the distances between hits on hailstones needs to be similar to the distance of the hailstones. This yields some complicated equations that can be used to simplify further, where values for vx and vy could be tried out since they are very small.

In the end, after writing formulas for several pages, used z3 solver to define the constraints and have z3 solve.

Alternative solution 1 (linear algebra):

-   Tried resolving by hand by defining 6 equations based on 3 hailstones and resolving for the 6 unknowns (xr, yr, zr, vxr, vyr, vzr). After rearranging into 6 linear equations, tried to use numpy.linalg.solve to resolve the coefficient matrix into the correct values, but due to the large numbers in the input, numpy has some imprecision and the numbers are slightly off (off by 3 when summing up xr + yr + zr).
-   This finally worked after running the same equations with multiple combinations of 3 hailstones and taking the most frequent values for xr, yr, zr (vxr, vyr, vzr were always the same)

Alternative solution 2 (converging rocks):

-   This uses the knowledge that all hailstones will pass through the same coordinates at given times t1, t2, etc with the coordinates being the starting position of the rock - assuming the rock stays static and the hailstones' curves all intersect at the same point, the starting point of the rock.
-   In this case, xr = x1 + (vx1 - vxr) _ t1, yr = y1 + (vy1 - vyr) _ t1 etc (for z too, and for different hailstones h2, h3)
-   This then allows us to use the same methods as for part 1 and just trying out values for vxr and vyr, which are in a relatively small range.
-   We can calculate intersections between hailstones h1 and h2 with the velocities adjusted for vxr and vyr. This yields a number of values for xr and yr where the hailstones intersect. We can then do the same for h1 and h3 and this yields only one pair of xr and yr values where both stones intersect.
-   From there on, we can formulate 2 equations based on the x values and derive zr and vzr using substitions. This results in the formula zr = (t2 _ t1 _ (vz2 - vz1) + t1 _ z2 - t2 _ z1) / (t1 - t2), which allows us to calculate z3.

# Day 25

-   Difficulty: Medium
-   Problem: In a bi-directional graph, find 3 edges that if cut split the graph into two clusters ("communities" in graph terminology). Multiply the size of the communities for the result.

1. converted the graph into an image using Networkx. This showed for the example and the input that there are exactly three edges that split the graph into two.
2. Googling found a number of algorithms that split graphs into communities. The Girvan-Newman algorithm calculates a score (Edge betweeness) for each edge and the iteratively removes the highest scored edges from the graph, splitting the graph into two, then three, etc communities.
3. Networkx has a method nx.communities.girvan_newman() that does exactly this and returns the two partitions when called once.
4. Multiplying the size of the two partitions was the correct answer.
5. Another way to calculate is the minimum-cut for the graph, which can be done using Karger's algorithm. Networkx has a `minimum_cut` method that calculates the minimum cut required between two given nodes to split the graph in into two partitions. This could be used as well.

Manually writing the algorithms:

-   [Girvan-Newman](https://medium.com/analytics-vidhya/girvan-newman-the-clustering-technique-in-network-analysis-27fe6d665c92):

    -   basically run a BFS from each node in the graph to calculate the number of minimum length paths that can be taken to each node. Assign this number of paths to each node
    -   then calculate a score for each edge based on the number of paths
    -   Do this for all nodes
    -   Calculate another score out of the sum of the edge scores for each score
    -   Remove the edges with the highest scores to split the graph (here - remove the three edges with the highest scores)
    -   There is also a formula to calculate if the resulting partitions are truly partitions or not

-   [Karger's algorithm](https://medium.com/@dev.elect.iitd/kargers-algorithm-d8067eb1b790)
    -   Repeat this algorithm a number of times as it uses randomized selection, so is not guaranteed to give the best result on each single run
    -   select a random edge
    -   contract the edge together i.e. consolidate the nodes
    -   repeat until only 2 edges remain
    -   the minimum cut is the number of edges between the two nodes

I implemented Karger's algorithm and it runs actually much faster than the Network X Girvan-Newman. We could probably compare against the Networkx.minimum_cut function and see how fast that runs?
