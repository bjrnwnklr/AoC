# Day 1

Difficulty: easy

A simple counting of numbers and loading numbers, transposing number pairs into separate lists.

# Day 2

Difficulty: easy

Comparing numbers in a list and determining if they

-   all increase or all decrease
-   if increments are between 1 and 3

Easy to solve, part 2 required dropping one element from each input list at a time and seeing if the algo from part 1 still worked.

# Day 3

Difficulty: Easy

Regular expression matching across a corrupted list of code. Detect patterns. Part 2 required simple logic to switch between two states.

I lost a few hours by not reading the description correctly as i assumed the switch would reset for every line of the code, but it was just set to an initial state at the beginning and then kept the state. Solution worked as designed after realizing that...

# Day 4

Difficulty: Easy

A bit more work: find words in a crossword. Part 1 required checking all horizontal, vertical and diagonal neighbors to find XMAS. Part 2 required finding cross sections where MAS was found diagonally around an A. Simple generating of neighbor coordinates and then checking if the word is matched.
