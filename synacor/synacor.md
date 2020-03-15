# Synacor challenge - Documentation

# System architecture

- Byte order on my system is little endian, so we can convert each pair of bytes directly into integers using the `np.frombuffer` with `dtype=np.uint16' 


# Learnings

## Reading a binary file

Open a binary file and read from it:

```python
with open('challenge.bin', 'rb') as f:
    data = f.read()

    # read individual bytes, e.g. the first 16
    some_bytes = data[:16]
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

