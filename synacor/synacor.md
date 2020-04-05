# Synacor challenge - Documentation

# Codes

1. Reading arch-spec: cxMJSJKnaTcr
1. First output, before self-test: zaxAXmJgbmFk
1. After self-test: xXqCcHPhkwGV
1. After taking tablet: oWiFbDGYUTNN
1. In twisty passages: xSoSzxDgGMtz 
1. After using teleporter in ruins: FwGIPVHecGNX
1. After using teleporter with energy level 25734: JELOdAveZwDG




# How to get the codes:

No 5: 
- From Twisty Passages main point (2377)
- West (2397)
- South (2402) (east is a grue)
- North ()

No 6: 
- crack riddle in ruins (2457)
- go to north
- take teleporter
- use teleporter


# Central hall of ruins (2457) - unlocking the north door

Monument with circular slots and unusual symbols.

_ + _ * _^2 + _^3 - _ = 399

(9, 2, 5, 7, 3) 399

**blue, red, shiny, concave, corroded** is the correct order. The value of the coins is 
red = 2
corroded = 3
shiny = 5
concave = 7
blue = 9

Descriptions:
- red coin: This coin is made of a red metal.  It has two dots on one side.
- corroded coin: This coin is somewhat corroded.  It has a triangle on one side.
- shiny coin: This coin is somehow still quite shiny.  It has a pentagon on one side.
- concave coin: 
This coin is slightly rounded, almost like a tiny bowl.  It has seven dots on one side.
- blue coin: This coin is made of a blue metal.  It has nine dots on one side.

These values can be seen in the memory positions 27102-27106 (which represent the parameters of the formula).

When the north door gets unlocked, the following memory value gets set:
Index   PrevMem CurrMem
[2462]  4       5

This can be used to unlock the north door in room 2457 (Ruins).


Putting coins in in wrong order (released to floor):
Index   PrevMem CurrMem
[2462]  4       0
[2690]  32767   2457
[2694]  0       2457
[2698]  32767   2457
[2702]  32767   2457
[2706]  32767   2457
[10376] 50      95
[10380] 51      95
[10384] 53      95
[10390] 55      95
[27106] 0       3   // [27106] 3       9

Putting red coin in:
Index   PrevMem CurrMem
[2462]  0       1
[2690]  0       32767
[10376] 95      50
[27103] 0       2

Putting corroded coin in:
Index   PrevMem CurrMem
[2462]  1       2
[2694]  0       32767
[10380] 95      51
[27104] 0       3

Putting shiny coin in:
Index   PrevMem CurrMem
[2462]  2       3
[2698]  0       32767
[10384] 95      53
[27105] 0       5

Putting concave coin in:
Index   PrevMem CurrMem
[2462]  3       4
[2702]  0       32767
[10390] 95      55
[27106] 0       7

Blue coin: 57
[27102] 0       9

# look strange book

Text:
The cover of this book subtly swirls with colors.  It is titled "A Brief Introduction to Interdimensional Physics".  It reads:

Recent advances in interdimensional physics have produced fascinating
predictions about the fundamentals of our universe!  For example,
interdimensional physics seems to predict that the universe is, at its root, a
purely mathematical construct, and that all events are caused by the
interactions between eight pockets of energy called "registers".
Furthermore, it seems that while the lower registers primarily control mundane
things like sound and light, the _highest register _(the so-called "eighth
register")_ is used to control interdimensional events such as teleportation.

A hypothetical such teleportation device would need to have have exactly two
destinations.  One destination would be used when the eighth register is at its
minimum energy level - this would be the default operation assuming the user
has no way to control the eighth register.  In this situation, the teleporter
should send the user to a preconfigured safe location as a default.

The second destination, however, is predicted to require a very specific
energy level in the eighth register.  The teleporter must take great care to
confirm that this energy level is exactly correct before teleporting its user!
If it is even slightly off, the user would (probably) arrive at the correct
location, but would briefly experience anomalies in the fabric of reality
itself - this is, of course, not recommended.  Any teleporter would need to test
the energy level in the eighth register and abort teleportation if it is not
exactly correct.

This required precision implies that the confirmation mechanism would be very
computationally expensive.  While this would likely not be an issue for large-
scale teleporters, a hypothetical hand-held teleporter would take billions of
years to compute the result and confirm that the eighth register is correct.

If you find yourself trapped in an alternate dimension with nothing but a
hand-held teleporter, you will need to **extract the confirmation algorithm,**
**reimplement it on more powerful hardware**, and **optimize it**.  This should, at the
very least, allow you to determine the value of the eighth register which would
have been accepted by the teleporter's confirmation mechanism.

Then, **set the eighth register to this value**, **activate the teleporter**, and
**bypass the confirmation mechanism**.  If the eighth register is set correctly, no
anomalies should be experienced, but beware - if it is set incorrectly, the
now-bypassed confirmation mechanism will not protect you!

Of course, since teleportation is impossible, this is all totally ridiculous.

So what has to be done:
- find the confirmation algorithm (triggered when using the teleporter)
- reimplement it (e.g. in Python)
- optimize it
- set the eight register to the value
- activate the teleporter
- bypass the confirmation mechanism


## Dumping code into a file
- Code is from memory 0 to 6068 (ending with ASCII code 4, end of transmission)
- text seems to start from 6069 to the end. It uses all available ASCII codes [http://www.asciitable.com/](http://www.asciitable.com/)

## General code analysis

- Self test seems to run until 1457 (up to there, the various error messages)
- At 1458, we have code starting again 

### 1458 - what does it do?

prints out characters from addresses

- save r0, r3, r4, r5, r6
    r6 = r0
    r5 = r1
    r4 = mem[r0]
    r1 = 0
    r3 = 1 + r1
    if r3 > r4:             --- return once r3 > r4
        return
    else:
        r3 += r6 (1+r1 + r0)
        r0 = mem[r3]
        call r5 (jump to r5, write next ip to stack)
        r1 = r1 + 1
        if r1 > 0:
            jump to 1480


Parameters that are required to call
r0 = 28844 = 169                (start address (will have length of text))
r1 = 1531                       (decoder / print function to call)
r2 = 1320 + 1867 = 3187         (key to decode)

Print function at 1458:
call 1458 (print)
r6 = 28844
r5 = 1531
r4 = 169
r1 = 0
r3 = 1
r3 += r6 (28845)
r0 = mem[28845] 3122
call 1531
r1 += 1 (2)

r3 = 1 + r1

1531: (print decoder)
r1 = r2 (3187)
call 2125
print r0

2125: (unscramble character)
r2 = r0 & r1 (3122 & 3187 = 3122)
r2 = ~r2 (not r2) (flip bits)
r0 = r0 | r1
r0 = r0 & r2

in short:
r0 = (r0 | r1) & ~(r0 & r1)

## Text that gets printed at teleport

### Non standard teleport

addr: 28844
p_func: 1531
key: 3187

A strange, electronic voice is projected into your mind:

"Unusual setting detected!  Starting confirmation process!  Estimated time to completion: 1 billion years."

addr: 29400
p_func: 1531
key: 22759

A strange, electronic voice is projected into your mind:

"Miscalibration detected!  Aborting teleportation!"

Nothing else seems to happen.

addr: 29014
p_func: 1531
key: 28385 (24388 + 3997)

You wake up on a sandy beach with a slight headache.  The last thing you remember is activating that teleporter... but now you can't find it anywhere in your pack.  Someone seems to have drawn a message in the sand here:

(message is missing!!!)

addr: 29245
p_func: 1531 
key: 10851

It begins to rain.  The message washes away.  You take a deep breath and feel firmly grounded in reality as the effects of the teleportation wear off.

### Normal teleport

addr: 29545
p_func: 1531
key: 13417

You activate the teleporter!  As you spiral through time and space, you think you see a pattern in the stars...


addr: 29667
p_func: 1531
key: 29545

After a few moments, you find yourself back on solid ground and a little disoriented.


## Try jumping over the calculation at 5483
- set r7 to a value > 0
- set r0 to 6 

setr 7 6
poke 5478 1
poke 5479 32768
poke 5480 6
poke 5481 6
poke 5482 5491


this works to jump over the calculation, however produces a wrong code. We still need to find the right energy level.

## Energy level calulaction at 6027

prep - starting values in r0, r1:
r0 = 4
r1 = 1
call to 6027
check if r0 == 6 - if yes continue, else give error message


### Code at 6027


```python
def f_6027():
    global r0
    global r1
    if not r0:
        r0 = r1 + 1
        return # return what?
    if not r1:
        r0 -= 1
        r1 = r7
        f_6027()
        return # return what?
    r0_tmp = r0 # push r0
    r1 -= 1
    f_6027()
    r1 = r0
    r0 = r0_tmp
    r0 -= 1
    f_6027()
    return

```

Ackermann function with
A(m, n) =
    n + 1               if m == 0
    A(m-1, k)           if m > 0 and n == 0
    A(m-1, A(m, n-1))   if m > 0 and n > 0

with k a constant.

Correct answer: 25734 (as shown in [https://github.com/jpcornwell/synacor-challenge/blob/master/useful/notes.txt](https://github.com/jpcornwell/synacor-challenge/blob/master/useful/notes.txt))

Good writeup here:
[https://github.com/kanegaegabriel/synacor-challenge/blob/master/writeup.md](https://github.com/kanegaegabriel/synacor-challenge/blob/master/writeup.md)

Try writing up the Ackermann function with memoization and run that? See when it returns 6.

**Finally able to solve it using C program**
I was finally able to solve this by using C on my WLS session.

I used the 3 C programs from [here](https://github.com/jpcornwell/synacor-challenge). The two optimized programs solve it in 10 (teleporter_small_opt.c) and 3 seconds (teleporter_opt.c)

How to compile C on WSL:

1. Launch WLS by typing `wsl` into command prompt
1. cd to the directory with the source code (in this case the mounted synacor dir on d:)
1. compile the C program with `gcc -o teleporter_opt teleporter_opt.c`
1. run the program with `./teleporter_opt`

## Log analysis:

- Register 7 (32775) is only checked once, at IP 5451. If it is 0 (teleport energy at minimum level), we jump to 5605.
DEBUG:root:Checking val 32775, returning 0.
DEBUG:root:Checking val 5605, returning 5605.
DEBUG:root:IP: 5451: jf 0 to 5605

- Check what happens if register 7 (32775) is not 0.

Pseudo code:

    6042: Get reg 7 (1)
    6042: Set reg 1 to 1
    6045: Call to 6027 (push 6047)
    6027: Get reg 0 (3)
    6027: Jump to 6035 if reg 0 > 0 (yes, it is 3)
    6035: Get reg 1 (1, our energy level from reg 7)
    6035: Jump to 6048 if reg 1 > 0 (yes, it is 1)
    6048: Push reg 0 (3)
    6050: Get reg 1 (1, our energy level)
    6050: Add into reg 1: reg 1 (1) + 32767 = 0   --- this really means "subtract 1 from reg 1"
    6054: Call to 6027 (push 6056)
    6027: Get reg 0 (3)
    6027: Jump to 6035 if reg 0 > 0 (yes it is 3)
    6035: Get reg 1 (0)
    6035: Jump to 6048 if reg 1 > 0 (no as it is 0)
    6038: Get reg 0 (3)
    6038: Add into reg 0: reg 0 (3) + 32767 = 2  --- subtract 1 from reg 0
    6042: Get reg 7 (1)
    6042: Set reg 1 to 1
    6045: Call to 6027 (push 6047)


    6042: reg[1] = reg[7]
    6027: while reg[0] > 0
    6035:   if reg[1] > 0:
    6048:       push reg[0]
    6050:       reg[1] -= 1
    6027:       if reg[0] > 0:
    6035:           if reg[1] > 0:

    6038:           else:
                        reg[0] -= 1

# Vault door (starting in 2623)

Moving from one room to the next, the following memory addresses get changed, again through some kind of formula. While walking, both the orb and the symbols on the floor change colors.

[3951]
[3952]  208     22
[3953]  5       0
[3954]  2824    0
[3955]  1186    0
[3956]  1541    0
[3957]  1345    0

# Memory hacks

## Inventory

Taking tablet:
Index   PrevMem CurrMem
[2670]  2317    0

Take can:
Index   PrevMem CurrMem
[2686]  2417    0

Take empty lantern:
Index   PrevMem CurrMem
[2674]  2357    0

Use tablet:
Index   PrevMem CurrMem
[6126]  0       28183
[6127]  0       30641
[6128]  0       20917

Find can: 
Index   PrevMem CurrMem
[2732]  2402    2417
[2733]  2402    2417
[3726]  24      88
[6126]  0       30670
[6127]  0       20155
[6128]  0       10617

Use can with lantern:
Index   PrevMem CurrMem
[2674]  0       32767   (address of empty lantern set to 23767)
[2678]  32767   0       (assume this is dark "yes" or "no"?)
[2686]  0       32767   (address of can set to 23767)

- this also makes the can disappear
- lantern changes from "empty lantern" to "lantern"

Dropping / taking lantern
Index   PrevMem CurrMem
[2678]  0       2367

Use lantern (light):
Index   PrevMem CurrMem
[2678]  0       32767
[2682]  32767   0

Take red coin:
Index   PrevMem CurrMem
[2690]  2452    0

Take concave coin:
Index   PrevMem CurrMem
[2702]  2468    0

Take blue coin:
Index   PrevMem CurrMem
[2706]  2478    0

Take shiny coin:
Index   PrevMem CurrMem
[2698]  2483    0

Take corroded coin:
Index   PrevMem CurrMem
[2694]  2473    0

Take teleporter:
Index   PrevMem CurrMem
[2710]  2463    0

Use teleporter:
Index   PrevMem CurrMem
[2732]  2463    2488
[2733]  2463    2488
[6126]  30670   5387
[6127]  20155   22372
[6128]  10617   1966
[6130]  120     70   (this is the code displayed)
[6131]  83      119
[6132]  111     71
[6133]  83      73
[6134]  122     80
[6135]  120     86
[6136]  68      72
[6137]  103     101
[6138]  71      99
[6139]  77      71
[6140]  116     78
[6141]  122     88

Take business card:
Index   PrevMem CurrMem
[2714]  2488    0

Take strange book:
Index   PrevMem CurrMem
[2726]  2488    0

## Items

can: You'll have to find something to put the oil into first.

tablet:             2670
empty lantern:      2674
lantern:            2678
lit lantern:        2682 
can:                2686
red coin:           2690 (found at 2452)
corroded coin:      2694 (found at 2473)
shiny coin:         2698 (found at 2483)
concave coin:       2702 (found at 2468)
blue coin:          2706 (found at 2478)
teleporter:         2710 (found at 2463)
business card:      2714 (found at 2488)
orb:                2718 (found at 2623)
strange book:       2726 (found at 2488)


## Positions

Changing position (moving 'doorway/north' from 'Foothills'):
Index   PrevMem CurrMem
[2732]  2317    2327
[2733]  2317    2327

Going into pitch black darkness (passage):
Index   PrevMem CurrMem
[2674]  2357    32767
[2732]  2372    2648
[2733]  2372    2648

Moving through twisty passages:
[3726]  0       2
[3726]  2       3
[3726]  0       8
[3726]  24      88 (finding can in 2417)

### Position table

| Position | Location |
|--|--|
| 2317 | Foothills |
| 2322 | Foothills (pulled north) |
| 2327 | Dark cave / doorway |
| 2332 | Dark cave 2 |
| 2337 | Dark cave 3 (to bridge) |
| 2342 | Rope bridge |
| 2347 | Falling through the air! |
| 2352 | Moss cavern |
| 2357 | Moss cavern **(empty lantern)** |
| 2362 | Moss cavern (to passage) |
| 2367 | Passage |
| 2372 | Passage (pitch black) |
| 2377 | Twisty passages (ladder back up) |
| 2387 | Twisty passages (south) |
| 2382 | Twisty passages (south) |
| 2392 | Twisty passages - grue to the east |
| 2397 | Twisty passages (west) |
| 2402 | Twisty passages (west, south) likely death in east |
| 2407 | Twisty passages |
| 2412 | Twisty passages (exit to west) |
| 2417 | Twisty passages **(5th code, can)** |
| 2427 | Dark passage (need light) |
| 2432 | Dark passage (need light) |
| 2437 | Dark passage (need light) |
| 2442 | Dark passage (need light) |
| 2447 | Ruins |
| 2452 | Ruins **(red coin)** |
| 2457 | Ruins (central hall, riddle) |
| 2463 | Ruins **teleporter** |
| 2468 | Ruins (dining hall, staircase down) **concave coin** |
| 2473 | Ruins (kitchen, down from 2457) **corroded coin** |
| 2478 | Ruins (living quarters, staircase up) **blue coin** |
| 2483 | Ruins (lavish throne room, up from 2478) **shiny coin** |

| 2488 | Synacor Headquarters **business card, strange book** |
| 2493 | Synacor HQ (outside) |
| 2498 | ??? |
| 2563 | Vault lock *** sign** |
| 2568 | Vault lock **8** |
| 2573 | Vault lock **-** |
| 2578 | Vault door **1**, door **30** |
| 2583 | Vault lock **4** |
| 2603 | Vault lock **+ sign** |
| 2623 | Vault antechamber **orb** **22** |

| 2648 | Fumbling around in the darkness (DEATH) |
| 2653 | Fumbling darkness, growling (DEATH) |
| 2658 | Panicked and lost (DEATH) |

# System architecture

- Byte order on my system is little endian, so we can convert each pair of bytes directly into integers using the `np.frombuffer` with `dtype=np.uint16' 
- Registers are treated differently than normal memory.
- Most instructions only write to registers, unless explicitely required (e.g. wmem)
- `Synacor._get_reg()` is used to calculate the register number of a value (if > 32767)
- We use `Synacor._get_val()` to determine whether something is a literal or a register. This can be used in any function expecting either a literal or a reference to a register. For `set`, where the number of a register is passed in, we can't use this and need to calculate the number of the register directly.


# Learnings

## Reading a binary file

Open a binary file and read from it:

```python
with open('challenge.bin', 'rb') as f:
    data = f.read()

    # read individual bytes, e.g. the first 16
    some_bytes = data[:16]
```

## Saving / loading objects from a JSON file

- Saving to JSON does a conversion of some object types, e.g. keys of dictionaries get automatically converted to strings. Hence they need to be converted to their original type again when loading.
- Only basic data types are supported, e.g. `int`, not `np.int64`. So values need to be converted before saving to a JSON object.

Saving: 
```python
import json

with open(f_name, 'w') as f:
    json.dump(state, f)
```

Loading:

```python
import json

with open(f_name, 'r') as f:
    vm_state = json.load(f)
``` 

The individual pieces of the JSON are now in a dictionary and can be loaded exactly like a dictionary. Note how the keys are converted back to integer.

```python
mem_copy_tmp = vm_state['mem_copy']
mem_copy = {int(k): v for k, v in mem_copy_tmp.items()}
print(f'mem_copy: length: {len(mem_copy)}')
```

## Converting bytes to integer

Show the byteorder of the system:

```python
import sys
print(sys.byteorder)
```

Convert individual bytes to int (e.g. two little endian bytes)

```python
import sys

print(int.from_bytes(b'\x15\x00', byteorder='little'))
```

Use Numpy to convert a large number of bytes into an array:

```python
import numpy as np

# this uses the sys.bytorder
int_data = np.frombuffer(data, dtype=np.uint16)
```

## Bitwise invert (NOT)

Bitwise NOT is done with `~x`, however this only works with signed integers and creates a negative integer.

For unsigned integers, it is easiest to XOR with the max value for the number of bits. E.g. for 15 bit wise inversion, use `0x7fff ^ i`, as `0x7fff` = (2 ** 15) - 1, the max value for 15 bits.
