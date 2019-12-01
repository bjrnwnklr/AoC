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

1) Post code > 5 lines using github or [paste](https://topaz.github.io/paste/).

## Download input

You can download the day's input from this URL: https://adventofcode.com/2019/day/1/input

I will document each day's learnings (what was the specific challenge, what techniques / algorithms were used to resolve). This will help with future challenges.

Template:

# Day x

## Challenge

### Part 1


### Part 2


## Learnings



# Day 1

## Challenge

### Part 1

- Fuel required to launch a given module is based on its mass. Specifically, to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.
- To find it, individually calculate the fuel needed for the mass of each module (your puzzle input), then add together all the fuel values.
- What is the sum of the fuel requirements for all of the modules on your spacecraft?

** Solution **
Read file in with list comprehension, then use another list comprehension to calculate fuel. Sum up (easy!)

### Part 2

Fuel itself requires fuel just like a module - take its mass, divide by three, round down, and subtract 2. However, that fuel also requires fuel, and that fuel requires fuel, and so on. Any mass that would require negative fuel should instead be treated as if it requires zero fuel; the remaining mass, if any, is instead handled by wishing really hard, which has no mass and is outside the scope of this calculation.

So, for each module mass, calculate its fuel and add it to the total. Then, treat the fuel amount you just calculated as the input mass and repeat the process, continuing until a fuel requirement is zero or negative. 

** Solution ** 
Use a simple function that iterates (not recursive!) through the fuel levels and adds them up (using a `while f > 0` loop).

## Learnings

Could have used _recursion_ by passing the temp sum as a 2nd parameter:

```python
with open ("day01.txt") as file:
    temp = [int(i.rstrip()) for i in file]    

def function(x: int):
    return x//3-2    

def more_fuel(mass: int, fuel_needed=0):
    temp = function(mass)
    if temp < 0:
        return fuel_needed
    return more_fuel(temp, fuel_needed+temp)
    
print(sum(map(function, temp)))    
print(sum(map(more_fuel, temp)))
```

Or return the sum of the current value plus recursion (my own version) (and we could have used the walruss operator `:=` gere if using Python 3.8):

```python
def fuel_recursive(mass):
    f = fuel(mass)
    if f > 0:
        return f + fuel_recursive(f)
    else: 
        return 0

fuel_3 = sum(fuel_recursive(m) for m in masses)
```