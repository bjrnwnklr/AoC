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
