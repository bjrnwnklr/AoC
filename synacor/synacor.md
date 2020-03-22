# Synacor challenge - Documentation

# Codes

1. Reading arch-spec: cxMJSJKnaTcr
1. First output, before self-test: zaxAXmJgbmFk
1. After self-test: xXqCcHPhkwGV
1. After taking tablet: oWiFbDGYUTNN
1. In twisty passages: xSoSzxDgGMtz 


# How to get the codes:

No 5: 
- From Twisty Passages main point (2377)
- West (2397)
- South (2402) (east is a grue)
- North ()


# Memory hacks

## Inventory

Taking tablet:
Index   PrevMem CurrMem
[2670]  2317    0

Take can:
Index   PrevMem CurrMem
[2686]  2417    0

Use tablet:
Index   PrevMem CurrMem
[6126]  28183   0
[6127]  30641   0
[6128]  20917   0

Find can: 
Index   PrevMem CurrMem
[2732]  2402    2417
[2733]  2402    2417
[3726]  24      88
[6126]  0       30670
[6127]  0       20155
[6128]  0       10617

## Items

can: You'll have to find something to put the oil into first.

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
| 2322 | ??? |
| 2327 | Dark cave / doorway |
| 2332 | Dark cave 2 |
| 2337 | Dark cave 3 (to bridge) |
| 2342 | Rope bridge |
| 2347 | Falling through the air! |
| 2352 | Moss cavern |
| | |
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
| 2417 | Twisty passages (5th code, can) |
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
