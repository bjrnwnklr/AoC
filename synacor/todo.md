# Synacor challenge - todo


# Initial attempt


# TO DO

Build Opcodes:

- set: 1 a b
  set register <a> to the value of <b>
- push: 2 a
  push <a> onto the stack
- pop: 3 a
  remove the top element from the stack and write it into <a>; empty stack = error
- eq: 4 a b c
  set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise
- gt: 5 a b c
  set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise
- jmp: 6 a
  jump to <a>
- jt: 7 a b
  if <a> is nonzero, jump to <b>
- jf: 8 a b
  if <a> is zero, jump to <b>
- add: 9 a b c
  assign into <a> the sum of <b> and <c> (modulo 32768)
- mult: 10 a b c
  store into <a> the product of <b> and <c> (modulo 32768)
- mod: 11 a b c
  store into <a> the remainder of <b> divided by <c>
- and: 12 a b c
  stores into <a> the bitwise and of <b> and <c>
- or: 13 a b c
  stores into <a> the bitwise or of <b> and <c>
- not: 14 a b
  stores 15-bit bitwise inverse of <b> in <a>
- rmem: 15 a b
  read memory at address <b> and write it to <a>
- wmem: 16 a b
  write the value from <b> into memory at address <a>
- call: 17 a
  write the address of the next instruction to the stack and jump to <a>
- ret: 18
  remove the top element from the stack and jump to it; empty stack = halt

- in: 20 a
  read a character from the terminal and write its ascii code to <a>; it can be assumed that once input starts, it will continue until a newline is encountered; this means that you can safely read whole lines from the keyboard and trust that they will be fully read



# DONE

- create an example program using the example from the arch-spec
- read the challenge.bin file and see if we can extract the program from it (binary file format)
- build simple instructions, starting with 0, 19, 21. Leverage Intcode implementation as much as possible.

Opcodes:
- halt: 0
  stop execution and terminate the program
- out: 19 a
  write the character represented by ascii code <a> to the terminal
- noop: 21
  no operation

