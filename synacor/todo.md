# Synacor challenge - todo


# Initial attempt


# TO DO

## Godmode

- build an input function that processes any input. 
- If keyword "g" is entered, switch to godmode

godmode commands:
- `debug` - set logging level to DEBUG
- `exit` - exit godmode
- `save` - save current state in a pickle file, with timestamp as filename
- `info` - show current instruction pointer and registers


## Load pickle file to skip self-test

- build a version of syn_run.py that loads a pickle file with a saved state instead of running through complete self-test (e.g. save after self-test completes)
  - Use a command line argument?



# DONE

- create an example program using the example from the arch-spec
- read the challenge.bin file and see if we can extract the program from it (binary file format)
- build simple instructions, starting with 0, 19, 21. Leverage Intcode implementation as much as possible.

- Implemented all opcodes, passed self-test
- Input reads from standard input and puts commands into an input buffer

