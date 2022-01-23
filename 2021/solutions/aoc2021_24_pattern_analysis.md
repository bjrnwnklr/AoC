# Analyzing the program, step by step

## Header, input value all 1s

```log
INFO:root:Analyzing input value (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1):
DEBUG:root:Initializing new ALU with program of length 252.
DEBUG:root:Running program of length 252.
```

## Segments split by `inp` line

14 segments with 18 lines of code each, going from `inp w` to `add z y` - one input statement per input digit.

-   What are the different lines per segment?
-   What exactly does a segment do?

```log
DEBUG:root:[0000]: inp w - {'w': 0, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0001]: mul x 0 - {'w': 1, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0002]: add x z - {'w': 1, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0003]: mod x 26 - {'w': 1, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0004]: div z 1 - {'w': 1, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0005]: add x 12 - {'w': 1, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0006]: eql x w - {'w': 1, 'x': 12, 'y': 0, 'z': 0}
DEBUG:root:[0007]: eql x 0 - {'w': 1, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0008]: mul y 0 - {'w': 1, 'x': 1, 'y': 0, 'z': 0}
DEBUG:root:[0009]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 0}
DEBUG:root:[0010]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 0}
DEBUG:root:[0011]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 0}
DEBUG:root:[0012]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 0}
DEBUG:root:[0013]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 0}
DEBUG:root:[0014]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 0}
DEBUG:root:[0015]: add y 4 - {'w': 1, 'x': 1, 'y': 1, 'z': 0}
DEBUG:root:[0016]: mul y x - {'w': 1, 'x': 1, 'y': 5, 'z': 0}
DEBUG:root:[0017]: add z y - {'w': 1, 'x': 1, 'y': 5, 'z': 0}
```

```log
DEBUG:root:[0018]: inp w - {'w': 1, 'x': 1, 'y': 5, 'z': 5}
DEBUG:root:[0019]: mul x 0 - {'w': 1, 'x': 1, 'y': 5, 'z': 5}
DEBUG:root:[0020]: add x z - {'w': 1, 'x': 0, 'y': 5, 'z': 5}
DEBUG:root:[0021]: mod x 26 - {'w': 1, 'x': 5, 'y': 5, 'z': 5}
DEBUG:root:[0022]: div z 1 - {'w': 1, 'x': 5, 'y': 5, 'z': 5}
DEBUG:root:[0023]: add x 11 - {'w': 1, 'x': 5, 'y': 5, 'z': 5}
DEBUG:root:[0024]: eql x w - {'w': 1, 'x': 16, 'y': 5, 'z': 5}
DEBUG:root:[0025]: eql x 0 - {'w': 1, 'x': 0, 'y': 5, 'z': 5}
DEBUG:root:[0026]: mul y 0 - {'w': 1, 'x': 1, 'y': 5, 'z': 5}
DEBUG:root:[0027]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 5}
DEBUG:root:[0028]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 5}
DEBUG:root:[0029]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 5}
DEBUG:root:[0030]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 5}
DEBUG:root:[0031]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 130}
DEBUG:root:[0032]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 130}
DEBUG:root:[0033]: add y 11 - {'w': 1, 'x': 1, 'y': 1, 'z': 130}
DEBUG:root:[0034]: mul y x - {'w': 1, 'x': 1, 'y': 12, 'z': 130}
DEBUG:root:[0035]: add z y - {'w': 1, 'x': 1, 'y': 12, 'z': 130}
```

```log
DEBUG:root:[0036]: inp w - {'w': 1, 'x': 1, 'y': 12, 'z': 142}
DEBUG:root:[0037]: mul x 0 - {'w': 1, 'x': 1, 'y': 12, 'z': 142}
DEBUG:root:[0038]: add x z - {'w': 1, 'x': 0, 'y': 12, 'z': 142}
DEBUG:root:[0039]: mod x 26 - {'w': 1, 'x': 142, 'y': 12, 'z': 142}
DEBUG:root:[0040]: div z 1 - {'w': 1, 'x': 12, 'y': 12, 'z': 142}
DEBUG:root:[0041]: add x 13 - {'w': 1, 'x': 12, 'y': 12, 'z': 142}
DEBUG:root:[0042]: eql x w - {'w': 1, 'x': 25, 'y': 12, 'z': 142}
DEBUG:root:[0043]: eql x 0 - {'w': 1, 'x': 0, 'y': 12, 'z': 142}
DEBUG:root:[0044]: mul y 0 - {'w': 1, 'x': 1, 'y': 12, 'z': 142}
DEBUG:root:[0045]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 142}
DEBUG:root:[0046]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 142}
DEBUG:root:[0047]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 142}
DEBUG:root:[0048]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 142}
DEBUG:root:[0049]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 3692}
DEBUG:root:[0050]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 3692}
DEBUG:root:[0051]: add y 5 - {'w': 1, 'x': 1, 'y': 1, 'z': 3692}
DEBUG:root:[0052]: mul y x - {'w': 1, 'x': 1, 'y': 6, 'z': 3692}
DEBUG:root:[0053]: add z y - {'w': 1, 'x': 1, 'y': 6, 'z': 3692}
```

```log
DEBUG:root:[0054]: inp w - {'w': 1, 'x': 1, 'y': 6, 'z': 3698}
DEBUG:root:[0055]: mul x 0 - {'w': 1, 'x': 1, 'y': 6, 'z': 3698}
DEBUG:root:[0056]: add x z - {'w': 1, 'x': 0, 'y': 6, 'z': 3698}
DEBUG:root:[0057]: mod x 26 - {'w': 1, 'x': 3698, 'y': 6, 'z': 3698}
DEBUG:root:[0058]: div z 1 - {'w': 1, 'x': 6, 'y': 6, 'z': 3698}
DEBUG:root:[0059]: add x 11 - {'w': 1, 'x': 6, 'y': 6, 'z': 3698}
DEBUG:root:[0060]: eql x w - {'w': 1, 'x': 17, 'y': 6, 'z': 3698}
DEBUG:root:[0061]: eql x 0 - {'w': 1, 'x': 0, 'y': 6, 'z': 3698}
DEBUG:root:[0062]: mul y 0 - {'w': 1, 'x': 1, 'y': 6, 'z': 3698}
DEBUG:root:[0063]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 3698}
DEBUG:root:[0064]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 3698}
DEBUG:root:[0065]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 3698}
DEBUG:root:[0066]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 3698}
DEBUG:root:[0067]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 96148}
DEBUG:root:[0068]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 96148}
DEBUG:root:[0069]: add y 11 - {'w': 1, 'x': 1, 'y': 1, 'z': 96148}
DEBUG:root:[0070]: mul y x - {'w': 1, 'x': 1, 'y': 12, 'z': 96148}
DEBUG:root:[0071]: add z y - {'w': 1, 'x': 1, 'y': 12, 'z': 96148}
```

```log
DEBUG:root:[0072]: inp w - {'w': 1, 'x': 1, 'y': 12, 'z': 96160}
DEBUG:root:[0073]: mul x 0 - {'w': 1, 'x': 1, 'y': 12, 'z': 96160}
DEBUG:root:[0074]: add x z - {'w': 1, 'x': 0, 'y': 12, 'z': 96160}
DEBUG:root:[0075]: mod x 26 - {'w': 1, 'x': 96160, 'y': 12, 'z': 96160}
DEBUG:root:[0076]: div z 1 - {'w': 1, 'x': 12, 'y': 12, 'z': 96160}
DEBUG:root:[0077]: add x 14 - {'w': 1, 'x': 12, 'y': 12, 'z': 96160}
DEBUG:root:[0078]: eql x w - {'w': 1, 'x': 26, 'y': 12, 'z': 96160}
DEBUG:root:[0079]: eql x 0 - {'w': 1, 'x': 0, 'y': 12, 'z': 96160}
DEBUG:root:[0080]: mul y 0 - {'w': 1, 'x': 1, 'y': 12, 'z': 96160}
DEBUG:root:[0081]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 96160}
DEBUG:root:[0082]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 96160}
DEBUG:root:[0083]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 96160}
DEBUG:root:[0084]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 96160}
DEBUG:root:[0085]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 2500160}
DEBUG:root:[0086]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 2500160}
DEBUG:root:[0087]: add y 14 - {'w': 1, 'x': 1, 'y': 1, 'z': 2500160}
DEBUG:root:[0088]: mul y x - {'w': 1, 'x': 1, 'y': 15, 'z': 2500160}
DEBUG:root:[0089]: add z y - {'w': 1, 'x': 1, 'y': 15, 'z': 2500160}
```

```log
DEBUG:root:[0090]: inp w - {'w': 1, 'x': 1, 'y': 15, 'z': 2500175}
DEBUG:root:[0091]: mul x 0 - {'w': 1, 'x': 1, 'y': 15, 'z': 2500175}
DEBUG:root:[0092]: add x z - {'w': 1, 'x': 0, 'y': 15, 'z': 2500175}
DEBUG:root:[0093]: mod x 26 - {'w': 1, 'x': 2500175, 'y': 15, 'z': 2500175}
DEBUG:root:[0094]: div z 26 - {'w': 1, 'x': 15, 'y': 15, 'z': 2500175}
DEBUG:root:[0095]: add x -10 - {'w': 1, 'x': 15, 'y': 15, 'z': 96160}
DEBUG:root:[0096]: eql x w - {'w': 1, 'x': 5, 'y': 15, 'z': 96160}
DEBUG:root:[0097]: eql x 0 - {'w': 1, 'x': 0, 'y': 15, 'z': 96160}
DEBUG:root:[0098]: mul y 0 - {'w': 1, 'x': 1, 'y': 15, 'z': 96160}
DEBUG:root:[0099]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 96160}
DEBUG:root:[0100]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 96160}
DEBUG:root:[0101]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 96160}
DEBUG:root:[0102]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 96160}
DEBUG:root:[0103]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 2500160}
DEBUG:root:[0104]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 2500160}
DEBUG:root:[0105]: add y 7 - {'w': 1, 'x': 1, 'y': 1, 'z': 2500160}
DEBUG:root:[0106]: mul y x - {'w': 1, 'x': 1, 'y': 8, 'z': 2500160}
DEBUG:root:[0107]: add z y - {'w': 1, 'x': 1, 'y': 8, 'z': 2500160}
```

```log
DEBUG:root:[0108]: inp w - {'w': 1, 'x': 1, 'y': 8, 'z': 2500168}
DEBUG:root:[0109]: mul x 0 - {'w': 1, 'x': 1, 'y': 8, 'z': 2500168}
DEBUG:root:[0110]: add x z - {'w': 1, 'x': 0, 'y': 8, 'z': 2500168}
DEBUG:root:[0111]: mod x 26 - {'w': 1, 'x': 2500168, 'y': 8, 'z': 2500168}
DEBUG:root:[0112]: div z 1 - {'w': 1, 'x': 8, 'y': 8, 'z': 2500168}
DEBUG:root:[0113]: add x 11 - {'w': 1, 'x': 8, 'y': 8, 'z': 2500168}
DEBUG:root:[0114]: eql x w - {'w': 1, 'x': 19, 'y': 8, 'z': 2500168}
DEBUG:root:[0115]: eql x 0 - {'w': 1, 'x': 0, 'y': 8, 'z': 2500168}
DEBUG:root:[0116]: mul y 0 - {'w': 1, 'x': 1, 'y': 8, 'z': 2500168}
DEBUG:root:[0117]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 2500168}
DEBUG:root:[0118]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0119]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0120]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 2500168}
DEBUG:root:[0121]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 65004368}
DEBUG:root:[0122]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 65004368}
DEBUG:root:[0123]: add y 11 - {'w': 1, 'x': 1, 'y': 1, 'z': 65004368}
DEBUG:root:[0124]: mul y x - {'w': 1, 'x': 1, 'y': 12, 'z': 65004368}
DEBUG:root:[0125]: add z y - {'w': 1, 'x': 1, 'y': 12, 'z': 65004368}
```

```log
DEBUG:root:[0126]: inp w - {'w': 1, 'x': 1, 'y': 12, 'z': 65004380}
DEBUG:root:[0127]: mul x 0 - {'w': 1, 'x': 1, 'y': 12, 'z': 65004380}
DEBUG:root:[0128]: add x z - {'w': 1, 'x': 0, 'y': 12, 'z': 65004380}
DEBUG:root:[0129]: mod x 26 - {'w': 1, 'x': 65004380, 'y': 12, 'z': 65004380}
DEBUG:root:[0130]: div z 26 - {'w': 1, 'x': 12, 'y': 12, 'z': 65004380}
DEBUG:root:[0131]: add x -9 - {'w': 1, 'x': 12, 'y': 12, 'z': 2500168}
DEBUG:root:[0132]: eql x w - {'w': 1, 'x': 3, 'y': 12, 'z': 2500168}
DEBUG:root:[0133]: eql x 0 - {'w': 1, 'x': 0, 'y': 12, 'z': 2500168}
DEBUG:root:[0134]: mul y 0 - {'w': 1, 'x': 1, 'y': 12, 'z': 2500168}
DEBUG:root:[0135]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 2500168}
DEBUG:root:[0136]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0137]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0138]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 2500168}
DEBUG:root:[0139]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 65004368}
DEBUG:root:[0140]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 65004368}
DEBUG:root:[0141]: add y 4 - {'w': 1, 'x': 1, 'y': 1, 'z': 65004368}
DEBUG:root:[0142]: mul y x - {'w': 1, 'x': 1, 'y': 5, 'z': 65004368}
DEBUG:root:[0143]: add z y - {'w': 1, 'x': 1, 'y': 5, 'z': 65004368}
```

```log
DEBUG:root:[0144]: inp w - {'w': 1, 'x': 1, 'y': 5, 'z': 65004373}
DEBUG:root:[0145]: mul x 0 - {'w': 1, 'x': 1, 'y': 5, 'z': 65004373}
DEBUG:root:[0146]: add x z - {'w': 1, 'x': 0, 'y': 5, 'z': 65004373}
DEBUG:root:[0147]: mod x 26 - {'w': 1, 'x': 65004373, 'y': 5, 'z': 65004373}
DEBUG:root:[0148]: div z 26 - {'w': 1, 'x': 5, 'y': 5, 'z': 65004373}
DEBUG:root:[0149]: add x -3 - {'w': 1, 'x': 5, 'y': 5, 'z': 2500168}
DEBUG:root:[0150]: eql x w - {'w': 1, 'x': 2, 'y': 5, 'z': 2500168}
DEBUG:root:[0151]: eql x 0 - {'w': 1, 'x': 0, 'y': 5, 'z': 2500168}
DEBUG:root:[0152]: mul y 0 - {'w': 1, 'x': 1, 'y': 5, 'z': 2500168}
DEBUG:root:[0153]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 2500168}
DEBUG:root:[0154]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0155]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0156]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 2500168}
DEBUG:root:[0157]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 65004368}
DEBUG:root:[0158]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 65004368}
DEBUG:root:[0159]: add y 6 - {'w': 1, 'x': 1, 'y': 1, 'z': 65004368}
DEBUG:root:[0160]: mul y x - {'w': 1, 'x': 1, 'y': 7, 'z': 65004368}
DEBUG:root:[0161]: add z y - {'w': 1, 'x': 1, 'y': 7, 'z': 65004368}
```

```log
DEBUG:root:[0162]: inp w - {'w': 1, 'x': 1, 'y': 7, 'z': 65004375}
DEBUG:root:[0163]: mul x 0 - {'w': 1, 'x': 1, 'y': 7, 'z': 65004375}
DEBUG:root:[0164]: add x z - {'w': 1, 'x': 0, 'y': 7, 'z': 65004375}
DEBUG:root:[0165]: mod x 26 - {'w': 1, 'x': 65004375, 'y': 7, 'z': 65004375}
DEBUG:root:[0166]: div z 1 - {'w': 1, 'x': 7, 'y': 7, 'z': 65004375}
DEBUG:root:[0167]: add x 13 - {'w': 1, 'x': 7, 'y': 7, 'z': 65004375}
DEBUG:root:[0168]: eql x w - {'w': 1, 'x': 20, 'y': 7, 'z': 65004375}
DEBUG:root:[0169]: eql x 0 - {'w': 1, 'x': 0, 'y': 7, 'z': 65004375}
DEBUG:root:[0170]: mul y 0 - {'w': 1, 'x': 1, 'y': 7, 'z': 65004375}
DEBUG:root:[0171]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 65004375}
DEBUG:root:[0172]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 65004375}
DEBUG:root:[0173]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 65004375}
DEBUG:root:[0174]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 65004375}
DEBUG:root:[0175]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 1690113750}
DEBUG:root:[0176]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 1690113750}
DEBUG:root:[0177]: add y 5 - {'w': 1, 'x': 1, 'y': 1, 'z': 1690113750}
DEBUG:root:[0178]: mul y x - {'w': 1, 'x': 1, 'y': 6, 'z': 1690113750}
DEBUG:root:[0179]: add z y - {'w': 1, 'x': 1, 'y': 6, 'z': 1690113750}
```

```log
DEBUG:root:[0180]: inp w - {'w': 1, 'x': 1, 'y': 6, 'z': 1690113756}
DEBUG:root:[0181]: mul x 0 - {'w': 1, 'x': 1, 'y': 6, 'z': 1690113756}
DEBUG:root:[0182]: add x z - {'w': 1, 'x': 0, 'y': 6, 'z': 1690113756}
DEBUG:root:[0183]: mod x 26 - {'w': 1, 'x': 1690113756, 'y': 6, 'z': 1690113756}
DEBUG:root:[0184]: div z 26 - {'w': 1, 'x': 6, 'y': 6, 'z': 1690113756}
DEBUG:root:[0185]: add x -5 - {'w': 1, 'x': 6, 'y': 6, 'z': 65004375}
DEBUG:root:[0186]: eql x w - {'w': 1, 'x': 1, 'y': 6, 'z': 65004375}
DEBUG:root:[0187]: eql x 0 - {'w': 1, 'x': 1, 'y': 6, 'z': 65004375}
DEBUG:root:[0188]: mul y 0 - {'w': 1, 'x': 0, 'y': 6, 'z': 65004375}
DEBUG:root:[0189]: add y 25 - {'w': 1, 'x': 0, 'y': 0, 'z': 65004375}
DEBUG:root:[0190]: mul y x - {'w': 1, 'x': 0, 'y': 25, 'z': 65004375}
DEBUG:root:[0191]: add y 1 - {'w': 1, 'x': 0, 'y': 0, 'z': 65004375}
DEBUG:root:[0192]: mul z y - {'w': 1, 'x': 0, 'y': 1, 'z': 65004375}
DEBUG:root:[0193]: mul y 0 - {'w': 1, 'x': 0, 'y': 1, 'z': 65004375}
DEBUG:root:[0194]: add y w - {'w': 1, 'x': 0, 'y': 0, 'z': 65004375}
DEBUG:root:[0195]: add y 9 - {'w': 1, 'x': 0, 'y': 1, 'z': 65004375}
DEBUG:root:[0196]: mul y x - {'w': 1, 'x': 0, 'y': 10, 'z': 65004375}
DEBUG:root:[0197]: add z y - {'w': 1, 'x': 0, 'y': 0, 'z': 65004375}
```

```log
DEBUG:root:[0198]: inp w - {'w': 1, 'x': 0, 'y': 0, 'z': 65004375}
DEBUG:root:[0199]: mul x 0 - {'w': 1, 'x': 0, 'y': 0, 'z': 65004375}
DEBUG:root:[0200]: add x z - {'w': 1, 'x': 0, 'y': 0, 'z': 65004375}
DEBUG:root:[0201]: mod x 26 - {'w': 1, 'x': 65004375, 'y': 0, 'z': 65004375}
DEBUG:root:[0202]: div z 26 - {'w': 1, 'x': 7, 'y': 0, 'z': 65004375}
DEBUG:root:[0203]: add x -10 - {'w': 1, 'x': 7, 'y': 0, 'z': 2500168}
DEBUG:root:[0204]: eql x w - {'w': 1, 'x': -3, 'y': 0, 'z': 2500168}
DEBUG:root:[0205]: eql x 0 - {'w': 1, 'x': 0, 'y': 0, 'z': 2500168}
DEBUG:root:[0206]: mul y 0 - {'w': 1, 'x': 1, 'y': 0, 'z': 2500168}
DEBUG:root:[0207]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 2500168}
DEBUG:root:[0208]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0209]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0210]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 2500168}
DEBUG:root:[0211]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 65004368}
DEBUG:root:[0212]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 65004368}
DEBUG:root:[0213]: add y 12 - {'w': 1, 'x': 1, 'y': 1, 'z': 65004368}
DEBUG:root:[0214]: mul y x - {'w': 1, 'x': 1, 'y': 13, 'z': 65004368}
DEBUG:root:[0215]: add z y - {'w': 1, 'x': 1, 'y': 13, 'z': 65004368}
```

```log
DEBUG:root:[0216]: inp w - {'w': 1, 'x': 1, 'y': 13, 'z': 65004381}
DEBUG:root:[0217]: mul x 0 - {'w': 1, 'x': 1, 'y': 13, 'z': 65004381}
DEBUG:root:[0218]: add x z - {'w': 1, 'x': 0, 'y': 13, 'z': 65004381}
DEBUG:root:[0219]: mod x 26 - {'w': 1, 'x': 65004381, 'y': 13, 'z': 65004381}
DEBUG:root:[0220]: div z 26 - {'w': 1, 'x': 13, 'y': 13, 'z': 65004381}
DEBUG:root:[0221]: add x -4 - {'w': 1, 'x': 13, 'y': 13, 'z': 2500168}
DEBUG:root:[0222]: eql x w - {'w': 1, 'x': 9, 'y': 13, 'z': 2500168}
DEBUG:root:[0223]: eql x 0 - {'w': 1, 'x': 0, 'y': 13, 'z': 2500168}
DEBUG:root:[0224]: mul y 0 - {'w': 1, 'x': 1, 'y': 13, 'z': 2500168}
DEBUG:root:[0225]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 2500168}
DEBUG:root:[0226]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0227]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0228]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 2500168}
DEBUG:root:[0229]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 65004368}
DEBUG:root:[0230]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 65004368}
DEBUG:root:[0231]: add y 14 - {'w': 1, 'x': 1, 'y': 1, 'z': 65004368}
DEBUG:root:[0232]: mul y x - {'w': 1, 'x': 1, 'y': 15, 'z': 65004368}
DEBUG:root:[0233]: add z y - {'w': 1, 'x': 1, 'y': 15, 'z': 65004368}
```

```log
DEBUG:root:[0234]: inp w - {'w': 1, 'x': 1, 'y': 15, 'z': 65004383}
DEBUG:root:[0235]: mul x 0 - {'w': 1, 'x': 1, 'y': 15, 'z': 65004383}
DEBUG:root:[0236]: add x z - {'w': 1, 'x': 0, 'y': 15, 'z': 65004383}
DEBUG:root:[0237]: mod x 26 - {'w': 1, 'x': 65004383, 'y': 15, 'z': 65004383}
DEBUG:root:[0238]: div z 26 - {'w': 1, 'x': 15, 'y': 15, 'z': 65004383}
DEBUG:root:[0239]: add x -5 - {'w': 1, 'x': 15, 'y': 15, 'z': 2500168}
DEBUG:root:[0240]: eql x w - {'w': 1, 'x': 10, 'y': 15, 'z': 2500168}
DEBUG:root:[0241]: eql x 0 - {'w': 1, 'x': 0, 'y': 15, 'z': 2500168}
DEBUG:root:[0242]: mul y 0 - {'w': 1, 'x': 1, 'y': 15, 'z': 2500168}
DEBUG:root:[0243]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 2500168}
DEBUG:root:[0244]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0245]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0246]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 2500168}
DEBUG:root:[0247]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 65004368}
DEBUG:root:[0248]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 65004368}
DEBUG:root:[0249]: add y 14 - {'w': 1, 'x': 1, 'y': 1, 'z': 65004368}
DEBUG:root:[0250]: mul y x - {'w': 1, 'x': 1, 'y': 15, 'z': 65004368}
DEBUG:root:[0251]: add z y - {'w': 1, 'x': 1, 'y': 15, 'z': 65004368}
```

```log
INFO:root:Invalid model number: (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1). alu.vars={'w': 1, 'x': 1, 'y': 15, 'z': 65004383}
```

# Rest of the input values

```
INFO:root:Analyzing input value (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 1):
DEBUG:root:Initializing new ALU with program of length 252.
DEBUG:root:Running program of length 252.
DEBUG:root:[0000]: inp w - {'w': 0, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0001]: mul x 0 - {'w': 1, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0002]: add x z - {'w': 1, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0003]: mod x 26 - {'w': 1, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0004]: div z 1 - {'w': 1, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0005]: add x 12 - {'w': 1, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0006]: eql x w - {'w': 1, 'x': 12, 'y': 0, 'z': 0}
DEBUG:root:[0007]: eql x 0 - {'w': 1, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0008]: mul y 0 - {'w': 1, 'x': 1, 'y': 0, 'z': 0}
DEBUG:root:[0009]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 0}
DEBUG:root:[0010]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 0}
DEBUG:root:[0011]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 0}
DEBUG:root:[0012]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 0}
DEBUG:root:[0013]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 0}
DEBUG:root:[0014]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 0}
DEBUG:root:[0015]: add y 4 - {'w': 1, 'x': 1, 'y': 1, 'z': 0}
DEBUG:root:[0016]: mul y x - {'w': 1, 'x': 1, 'y': 5, 'z': 0}
DEBUG:root:[0017]: add z y - {'w': 1, 'x': 1, 'y': 5, 'z': 0}
DEBUG:root:[0018]: inp w - {'w': 1, 'x': 1, 'y': 5, 'z': 5}
DEBUG:root:[0019]: mul x 0 - {'w': 1, 'x': 1, 'y': 5, 'z': 5}
DEBUG:root:[0020]: add x z - {'w': 1, 'x': 0, 'y': 5, 'z': 5}
DEBUG:root:[0021]: mod x 26 - {'w': 1, 'x': 5, 'y': 5, 'z': 5}
DEBUG:root:[0022]: div z 1 - {'w': 1, 'x': 5, 'y': 5, 'z': 5}
DEBUG:root:[0023]: add x 11 - {'w': 1, 'x': 5, 'y': 5, 'z': 5}
DEBUG:root:[0024]: eql x w - {'w': 1, 'x': 16, 'y': 5, 'z': 5}
DEBUG:root:[0025]: eql x 0 - {'w': 1, 'x': 0, 'y': 5, 'z': 5}
DEBUG:root:[0026]: mul y 0 - {'w': 1, 'x': 1, 'y': 5, 'z': 5}
DEBUG:root:[0027]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 5}
DEBUG:root:[0028]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 5}
DEBUG:root:[0029]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 5}
DEBUG:root:[0030]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 5}
DEBUG:root:[0031]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 130}
DEBUG:root:[0032]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 130}
DEBUG:root:[0033]: add y 11 - {'w': 1, 'x': 1, 'y': 1, 'z': 130}
DEBUG:root:[0034]: mul y x - {'w': 1, 'x': 1, 'y': 12, 'z': 130}
DEBUG:root:[0035]: add z y - {'w': 1, 'x': 1, 'y': 12, 'z': 130}
DEBUG:root:[0036]: inp w - {'w': 1, 'x': 1, 'y': 12, 'z': 142}
DEBUG:root:[0037]: mul x 0 - {'w': 1, 'x': 1, 'y': 12, 'z': 142}
DEBUG:root:[0038]: add x z - {'w': 1, 'x': 0, 'y': 12, 'z': 142}
DEBUG:root:[0039]: mod x 26 - {'w': 1, 'x': 142, 'y': 12, 'z': 142}
DEBUG:root:[0040]: div z 1 - {'w': 1, 'x': 12, 'y': 12, 'z': 142}
DEBUG:root:[0041]: add x 13 - {'w': 1, 'x': 12, 'y': 12, 'z': 142}
DEBUG:root:[0042]: eql x w - {'w': 1, 'x': 25, 'y': 12, 'z': 142}
DEBUG:root:[0043]: eql x 0 - {'w': 1, 'x': 0, 'y': 12, 'z': 142}
DEBUG:root:[0044]: mul y 0 - {'w': 1, 'x': 1, 'y': 12, 'z': 142}
DEBUG:root:[0045]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 142}
DEBUG:root:[0046]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 142}
DEBUG:root:[0047]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 142}
DEBUG:root:[0048]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 142}
DEBUG:root:[0049]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 3692}
DEBUG:root:[0050]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 3692}
DEBUG:root:[0051]: add y 5 - {'w': 1, 'x': 1, 'y': 1, 'z': 3692}
DEBUG:root:[0052]: mul y x - {'w': 1, 'x': 1, 'y': 6, 'z': 3692}
DEBUG:root:[0053]: add z y - {'w': 1, 'x': 1, 'y': 6, 'z': 3692}
DEBUG:root:[0054]: inp w - {'w': 1, 'x': 1, 'y': 6, 'z': 3698}
DEBUG:root:[0055]: mul x 0 - {'w': 1, 'x': 1, 'y': 6, 'z': 3698}
DEBUG:root:[0056]: add x z - {'w': 1, 'x': 0, 'y': 6, 'z': 3698}
DEBUG:root:[0057]: mod x 26 - {'w': 1, 'x': 3698, 'y': 6, 'z': 3698}
DEBUG:root:[0058]: div z 1 - {'w': 1, 'x': 6, 'y': 6, 'z': 3698}
DEBUG:root:[0059]: add x 11 - {'w': 1, 'x': 6, 'y': 6, 'z': 3698}
DEBUG:root:[0060]: eql x w - {'w': 1, 'x': 17, 'y': 6, 'z': 3698}
DEBUG:root:[0061]: eql x 0 - {'w': 1, 'x': 0, 'y': 6, 'z': 3698}
DEBUG:root:[0062]: mul y 0 - {'w': 1, 'x': 1, 'y': 6, 'z': 3698}
DEBUG:root:[0063]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 3698}
DEBUG:root:[0064]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 3698}
DEBUG:root:[0065]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 3698}
DEBUG:root:[0066]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 3698}
DEBUG:root:[0067]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 96148}
DEBUG:root:[0068]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 96148}
DEBUG:root:[0069]: add y 11 - {'w': 1, 'x': 1, 'y': 1, 'z': 96148}
DEBUG:root:[0070]: mul y x - {'w': 1, 'x': 1, 'y': 12, 'z': 96148}
DEBUG:root:[0071]: add z y - {'w': 1, 'x': 1, 'y': 12, 'z': 96148}
DEBUG:root:[0072]: inp w - {'w': 1, 'x': 1, 'y': 12, 'z': 96160}
DEBUG:root:[0073]: mul x 0 - {'w': 1, 'x': 1, 'y': 12, 'z': 96160}
DEBUG:root:[0074]: add x z - {'w': 1, 'x': 0, 'y': 12, 'z': 96160}
DEBUG:root:[0075]: mod x 26 - {'w': 1, 'x': 96160, 'y': 12, 'z': 96160}
DEBUG:root:[0076]: div z 1 - {'w': 1, 'x': 12, 'y': 12, 'z': 96160}
DEBUG:root:[0077]: add x 14 - {'w': 1, 'x': 12, 'y': 12, 'z': 96160}
DEBUG:root:[0078]: eql x w - {'w': 1, 'x': 26, 'y': 12, 'z': 96160}
DEBUG:root:[0079]: eql x 0 - {'w': 1, 'x': 0, 'y': 12, 'z': 96160}
DEBUG:root:[0080]: mul y 0 - {'w': 1, 'x': 1, 'y': 12, 'z': 96160}
DEBUG:root:[0081]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 96160}
DEBUG:root:[0082]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 96160}
DEBUG:root:[0083]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 96160}
DEBUG:root:[0084]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 96160}
DEBUG:root:[0085]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 2500160}
DEBUG:root:[0086]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 2500160}
DEBUG:root:[0087]: add y 14 - {'w': 1, 'x': 1, 'y': 1, 'z': 2500160}
DEBUG:root:[0088]: mul y x - {'w': 1, 'x': 1, 'y': 15, 'z': 2500160}
DEBUG:root:[0089]: add z y - {'w': 1, 'x': 1, 'y': 15, 'z': 2500160}
DEBUG:root:[0090]: inp w - {'w': 1, 'x': 1, 'y': 15, 'z': 2500175}
DEBUG:root:[0091]: mul x 0 - {'w': 1, 'x': 1, 'y': 15, 'z': 2500175}
DEBUG:root:[0092]: add x z - {'w': 1, 'x': 0, 'y': 15, 'z': 2500175}
DEBUG:root:[0093]: mod x 26 - {'w': 1, 'x': 2500175, 'y': 15, 'z': 2500175}
DEBUG:root:[0094]: div z 26 - {'w': 1, 'x': 15, 'y': 15, 'z': 2500175}
DEBUG:root:[0095]: add x -10 - {'w': 1, 'x': 15, 'y': 15, 'z': 96160}
DEBUG:root:[0096]: eql x w - {'w': 1, 'x': 5, 'y': 15, 'z': 96160}
DEBUG:root:[0097]: eql x 0 - {'w': 1, 'x': 0, 'y': 15, 'z': 96160}
DEBUG:root:[0098]: mul y 0 - {'w': 1, 'x': 1, 'y': 15, 'z': 96160}
DEBUG:root:[0099]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 96160}
DEBUG:root:[0100]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 96160}
DEBUG:root:[0101]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 96160}
DEBUG:root:[0102]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 96160}
DEBUG:root:[0103]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 2500160}
DEBUG:root:[0104]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 2500160}
DEBUG:root:[0105]: add y 7 - {'w': 1, 'x': 1, 'y': 1, 'z': 2500160}
DEBUG:root:[0106]: mul y x - {'w': 1, 'x': 1, 'y': 8, 'z': 2500160}
DEBUG:root:[0107]: add z y - {'w': 1, 'x': 1, 'y': 8, 'z': 2500160}
DEBUG:root:[0108]: inp w - {'w': 1, 'x': 1, 'y': 8, 'z': 2500168}
DEBUG:root:[0109]: mul x 0 - {'w': 1, 'x': 1, 'y': 8, 'z': 2500168}
DEBUG:root:[0110]: add x z - {'w': 1, 'x': 0, 'y': 8, 'z': 2500168}
DEBUG:root:[0111]: mod x 26 - {'w': 1, 'x': 2500168, 'y': 8, 'z': 2500168}
DEBUG:root:[0112]: div z 1 - {'w': 1, 'x': 8, 'y': 8, 'z': 2500168}
DEBUG:root:[0113]: add x 11 - {'w': 1, 'x': 8, 'y': 8, 'z': 2500168}
DEBUG:root:[0114]: eql x w - {'w': 1, 'x': 19, 'y': 8, 'z': 2500168}
DEBUG:root:[0115]: eql x 0 - {'w': 1, 'x': 0, 'y': 8, 'z': 2500168}
DEBUG:root:[0116]: mul y 0 - {'w': 1, 'x': 1, 'y': 8, 'z': 2500168}
DEBUG:root:[0117]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 2500168}
DEBUG:root:[0118]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0119]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0120]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 2500168}
DEBUG:root:[0121]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 65004368}
DEBUG:root:[0122]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 65004368}
DEBUG:root:[0123]: add y 11 - {'w': 1, 'x': 1, 'y': 1, 'z': 65004368}
DEBUG:root:[0124]: mul y x - {'w': 1, 'x': 1, 'y': 12, 'z': 65004368}
DEBUG:root:[0125]: add z y - {'w': 1, 'x': 1, 'y': 12, 'z': 65004368}
DEBUG:root:[0126]: inp w - {'w': 1, 'x': 1, 'y': 12, 'z': 65004380}
DEBUG:root:[0127]: mul x 0 - {'w': 1, 'x': 1, 'y': 12, 'z': 65004380}
DEBUG:root:[0128]: add x z - {'w': 1, 'x': 0, 'y': 12, 'z': 65004380}
DEBUG:root:[0129]: mod x 26 - {'w': 1, 'x': 65004380, 'y': 12, 'z': 65004380}
DEBUG:root:[0130]: div z 26 - {'w': 1, 'x': 12, 'y': 12, 'z': 65004380}
DEBUG:root:[0131]: add x -9 - {'w': 1, 'x': 12, 'y': 12, 'z': 2500168}
DEBUG:root:[0132]: eql x w - {'w': 1, 'x': 3, 'y': 12, 'z': 2500168}
DEBUG:root:[0133]: eql x 0 - {'w': 1, 'x': 0, 'y': 12, 'z': 2500168}
DEBUG:root:[0134]: mul y 0 - {'w': 1, 'x': 1, 'y': 12, 'z': 2500168}
DEBUG:root:[0135]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 2500168}
DEBUG:root:[0136]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0137]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0138]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 2500168}
DEBUG:root:[0139]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 65004368}
DEBUG:root:[0140]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 65004368}
DEBUG:root:[0141]: add y 4 - {'w': 1, 'x': 1, 'y': 1, 'z': 65004368}
DEBUG:root:[0142]: mul y x - {'w': 1, 'x': 1, 'y': 5, 'z': 65004368}
DEBUG:root:[0143]: add z y - {'w': 1, 'x': 1, 'y': 5, 'z': 65004368}
DEBUG:root:[0144]: inp w - {'w': 1, 'x': 1, 'y': 5, 'z': 65004373}
DEBUG:root:[0145]: mul x 0 - {'w': 1, 'x': 1, 'y': 5, 'z': 65004373}
DEBUG:root:[0146]: add x z - {'w': 1, 'x': 0, 'y': 5, 'z': 65004373}
DEBUG:root:[0147]: mod x 26 - {'w': 1, 'x': 65004373, 'y': 5, 'z': 65004373}
DEBUG:root:[0148]: div z 26 - {'w': 1, 'x': 5, 'y': 5, 'z': 65004373}
DEBUG:root:[0149]: add x -3 - {'w': 1, 'x': 5, 'y': 5, 'z': 2500168}
DEBUG:root:[0150]: eql x w - {'w': 1, 'x': 2, 'y': 5, 'z': 2500168}
DEBUG:root:[0151]: eql x 0 - {'w': 1, 'x': 0, 'y': 5, 'z': 2500168}
DEBUG:root:[0152]: mul y 0 - {'w': 1, 'x': 1, 'y': 5, 'z': 2500168}
DEBUG:root:[0153]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 2500168}
DEBUG:root:[0154]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0155]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0156]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 2500168}
DEBUG:root:[0157]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 65004368}
DEBUG:root:[0158]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 65004368}
DEBUG:root:[0159]: add y 6 - {'w': 1, 'x': 1, 'y': 1, 'z': 65004368}
DEBUG:root:[0160]: mul y x - {'w': 1, 'x': 1, 'y': 7, 'z': 65004368}
DEBUG:root:[0161]: add z y - {'w': 1, 'x': 1, 'y': 7, 'z': 65004368}
DEBUG:root:[0162]: inp w - {'w': 1, 'x': 1, 'y': 7, 'z': 65004375}
DEBUG:root:[0163]: mul x 0 - {'w': 1, 'x': 1, 'y': 7, 'z': 65004375}
DEBUG:root:[0164]: add x z - {'w': 1, 'x': 0, 'y': 7, 'z': 65004375}
DEBUG:root:[0165]: mod x 26 - {'w': 1, 'x': 65004375, 'y': 7, 'z': 65004375}
DEBUG:root:[0166]: div z 1 - {'w': 1, 'x': 7, 'y': 7, 'z': 65004375}
DEBUG:root:[0167]: add x 13 - {'w': 1, 'x': 7, 'y': 7, 'z': 65004375}
DEBUG:root:[0168]: eql x w - {'w': 1, 'x': 20, 'y': 7, 'z': 65004375}
DEBUG:root:[0169]: eql x 0 - {'w': 1, 'x': 0, 'y': 7, 'z': 65004375}
DEBUG:root:[0170]: mul y 0 - {'w': 1, 'x': 1, 'y': 7, 'z': 65004375}
DEBUG:root:[0171]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 65004375}
DEBUG:root:[0172]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 65004375}
DEBUG:root:[0173]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 65004375}
DEBUG:root:[0174]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 65004375}
DEBUG:root:[0175]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 1690113750}
DEBUG:root:[0176]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 1690113750}
DEBUG:root:[0177]: add y 5 - {'w': 1, 'x': 1, 'y': 1, 'z': 1690113750}
DEBUG:root:[0178]: mul y x - {'w': 1, 'x': 1, 'y': 6, 'z': 1690113750}
DEBUG:root:[0179]: add z y - {'w': 1, 'x': 1, 'y': 6, 'z': 1690113750}
DEBUG:root:[0180]: inp w - {'w': 1, 'x': 1, 'y': 6, 'z': 1690113756}
DEBUG:root:[0181]: mul x 0 - {'w': 1, 'x': 1, 'y': 6, 'z': 1690113756}
DEBUG:root:[0182]: add x z - {'w': 1, 'x': 0, 'y': 6, 'z': 1690113756}
DEBUG:root:[0183]: mod x 26 - {'w': 1, 'x': 1690113756, 'y': 6, 'z': 1690113756}
DEBUG:root:[0184]: div z 26 - {'w': 1, 'x': 6, 'y': 6, 'z': 1690113756}
DEBUG:root:[0185]: add x -5 - {'w': 1, 'x': 6, 'y': 6, 'z': 65004375}
DEBUG:root:[0186]: eql x w - {'w': 1, 'x': 1, 'y': 6, 'z': 65004375}
DEBUG:root:[0187]: eql x 0 - {'w': 1, 'x': 1, 'y': 6, 'z': 65004375}
DEBUG:root:[0188]: mul y 0 - {'w': 1, 'x': 0, 'y': 6, 'z': 65004375}
DEBUG:root:[0189]: add y 25 - {'w': 1, 'x': 0, 'y': 0, 'z': 65004375}
DEBUG:root:[0190]: mul y x - {'w': 1, 'x': 0, 'y': 25, 'z': 65004375}
DEBUG:root:[0191]: add y 1 - {'w': 1, 'x': 0, 'y': 0, 'z': 65004375}
DEBUG:root:[0192]: mul z y - {'w': 1, 'x': 0, 'y': 1, 'z': 65004375}
DEBUG:root:[0193]: mul y 0 - {'w': 1, 'x': 0, 'y': 1, 'z': 65004375}
DEBUG:root:[0194]: add y w - {'w': 1, 'x': 0, 'y': 0, 'z': 65004375}
DEBUG:root:[0195]: add y 9 - {'w': 1, 'x': 0, 'y': 1, 'z': 65004375}
DEBUG:root:[0196]: mul y x - {'w': 1, 'x': 0, 'y': 10, 'z': 65004375}
DEBUG:root:[0197]: add z y - {'w': 1, 'x': 0, 'y': 0, 'z': 65004375}
DEBUG:root:[0198]: inp w - {'w': 1, 'x': 0, 'y': 0, 'z': 65004375}
DEBUG:root:[0199]: mul x 0 - {'w': 1, 'x': 0, 'y': 0, 'z': 65004375}
DEBUG:root:[0200]: add x z - {'w': 1, 'x': 0, 'y': 0, 'z': 65004375}
DEBUG:root:[0201]: mod x 26 - {'w': 1, 'x': 65004375, 'y': 0, 'z': 65004375}
DEBUG:root:[0202]: div z 26 - {'w': 1, 'x': 7, 'y': 0, 'z': 65004375}
DEBUG:root:[0203]: add x -10 - {'w': 1, 'x': 7, 'y': 0, 'z': 2500168}
DEBUG:root:[0204]: eql x w - {'w': 1, 'x': -3, 'y': 0, 'z': 2500168}
DEBUG:root:[0205]: eql x 0 - {'w': 1, 'x': 0, 'y': 0, 'z': 2500168}
DEBUG:root:[0206]: mul y 0 - {'w': 1, 'x': 1, 'y': 0, 'z': 2500168}
DEBUG:root:[0207]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 2500168}
DEBUG:root:[0208]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0209]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0210]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 2500168}
DEBUG:root:[0211]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 65004368}
DEBUG:root:[0212]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 65004368}
DEBUG:root:[0213]: add y 12 - {'w': 1, 'x': 1, 'y': 1, 'z': 65004368}
DEBUG:root:[0214]: mul y x - {'w': 1, 'x': 1, 'y': 13, 'z': 65004368}
DEBUG:root:[0215]: add z y - {'w': 1, 'x': 1, 'y': 13, 'z': 65004368}
DEBUG:root:[0216]: inp w - {'w': 1, 'x': 1, 'y': 13, 'z': 65004381}
DEBUG:root:[0217]: mul x 0 - {'w': 9, 'x': 1, 'y': 13, 'z': 65004381}
DEBUG:root:[0218]: add x z - {'w': 9, 'x': 0, 'y': 13, 'z': 65004381}
DEBUG:root:[0219]: mod x 26 - {'w': 9, 'x': 65004381, 'y': 13, 'z': 65004381}
DEBUG:root:[0220]: div z 26 - {'w': 9, 'x': 13, 'y': 13, 'z': 65004381}
DEBUG:root:[0221]: add x -4 - {'w': 9, 'x': 13, 'y': 13, 'z': 2500168}
DEBUG:root:[0222]: eql x w - {'w': 9, 'x': 9, 'y': 13, 'z': 2500168}
DEBUG:root:[0223]: eql x 0 - {'w': 9, 'x': 1, 'y': 13, 'z': 2500168}
DEBUG:root:[0224]: mul y 0 - {'w': 9, 'x': 0, 'y': 13, 'z': 2500168}
DEBUG:root:[0225]: add y 25 - {'w': 9, 'x': 0, 'y': 0, 'z': 2500168}
DEBUG:root:[0226]: mul y x - {'w': 9, 'x': 0, 'y': 25, 'z': 2500168}
DEBUG:root:[0227]: add y 1 - {'w': 9, 'x': 0, 'y': 0, 'z': 2500168}
DEBUG:root:[0228]: mul z y - {'w': 9, 'x': 0, 'y': 1, 'z': 2500168}
DEBUG:root:[0229]: mul y 0 - {'w': 9, 'x': 0, 'y': 1, 'z': 2500168}
DEBUG:root:[0230]: add y w - {'w': 9, 'x': 0, 'y': 0, 'z': 2500168}
DEBUG:root:[0231]: add y 14 - {'w': 9, 'x': 0, 'y': 9, 'z': 2500168}
DEBUG:root:[0232]: mul y x - {'w': 9, 'x': 0, 'y': 23, 'z': 2500168}
DEBUG:root:[0233]: add z y - {'w': 9, 'x': 0, 'y': 0, 'z': 2500168}
DEBUG:root:[0234]: inp w - {'w': 9, 'x': 0, 'y': 0, 'z': 2500168}
DEBUG:root:[0235]: mul x 0 - {'w': 1, 'x': 0, 'y': 0, 'z': 2500168}
DEBUG:root:[0236]: add x z - {'w': 1, 'x': 0, 'y': 0, 'z': 2500168}
DEBUG:root:[0237]: mod x 26 - {'w': 1, 'x': 2500168, 'y': 0, 'z': 2500168}
DEBUG:root:[0238]: div z 26 - {'w': 1, 'x': 8, 'y': 0, 'z': 2500168}
DEBUG:root:[0239]: add x -5 - {'w': 1, 'x': 8, 'y': 0, 'z': 96160}
DEBUG:root:[0240]: eql x w - {'w': 1, 'x': 3, 'y': 0, 'z': 96160}
DEBUG:root:[0241]: eql x 0 - {'w': 1, 'x': 0, 'y': 0, 'z': 96160}
DEBUG:root:[0242]: mul y 0 - {'w': 1, 'x': 1, 'y': 0, 'z': 96160}
DEBUG:root:[0243]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 96160}
DEBUG:root:[0244]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 96160}
DEBUG:root:[0245]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 96160}
DEBUG:root:[0246]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 96160}
DEBUG:root:[0247]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 2500160}
DEBUG:root:[0248]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 2500160}
DEBUG:root:[0249]: add y 14 - {'w': 1, 'x': 1, 'y': 1, 'z': 2500160}
DEBUG:root:[0250]: mul y x - {'w': 1, 'x': 1, 'y': 15, 'z': 2500160}
DEBUG:root:[0251]: add z y - {'w': 1, 'x': 1, 'y': 15, 'z': 2500160}
INFO:root:Invalid model number: (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 1). alu.vars={'w': 1, 'x': 1, 'y': 15, 'z': 2500175}
INFO:root:Analyzing input value (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 3):
DEBUG:root:Initializing new ALU with program of length 252.
DEBUG:root:Running program of length 252.
DEBUG:root:[0000]: inp w - {'w': 0, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0001]: mul x 0 - {'w': 1, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0002]: add x z - {'w': 1, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0003]: mod x 26 - {'w': 1, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0004]: div z 1 - {'w': 1, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0005]: add x 12 - {'w': 1, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0006]: eql x w - {'w': 1, 'x': 12, 'y': 0, 'z': 0}
DEBUG:root:[0007]: eql x 0 - {'w': 1, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0008]: mul y 0 - {'w': 1, 'x': 1, 'y': 0, 'z': 0}
DEBUG:root:[0009]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 0}
DEBUG:root:[0010]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 0}
DEBUG:root:[0011]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 0}
DEBUG:root:[0012]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 0}
DEBUG:root:[0013]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 0}
DEBUG:root:[0014]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 0}
DEBUG:root:[0015]: add y 4 - {'w': 1, 'x': 1, 'y': 1, 'z': 0}
DEBUG:root:[0016]: mul y x - {'w': 1, 'x': 1, 'y': 5, 'z': 0}
DEBUG:root:[0017]: add z y - {'w': 1, 'x': 1, 'y': 5, 'z': 0}
DEBUG:root:[0018]: inp w - {'w': 1, 'x': 1, 'y': 5, 'z': 5}
DEBUG:root:[0019]: mul x 0 - {'w': 1, 'x': 1, 'y': 5, 'z': 5}
DEBUG:root:[0020]: add x z - {'w': 1, 'x': 0, 'y': 5, 'z': 5}
DEBUG:root:[0021]: mod x 26 - {'w': 1, 'x': 5, 'y': 5, 'z': 5}
DEBUG:root:[0022]: div z 1 - {'w': 1, 'x': 5, 'y': 5, 'z': 5}
DEBUG:root:[0023]: add x 11 - {'w': 1, 'x': 5, 'y': 5, 'z': 5}
DEBUG:root:[0024]: eql x w - {'w': 1, 'x': 16, 'y': 5, 'z': 5}
DEBUG:root:[0025]: eql x 0 - {'w': 1, 'x': 0, 'y': 5, 'z': 5}
DEBUG:root:[0026]: mul y 0 - {'w': 1, 'x': 1, 'y': 5, 'z': 5}
DEBUG:root:[0027]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 5}
DEBUG:root:[0028]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 5}
DEBUG:root:[0029]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 5}
DEBUG:root:[0030]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 5}
DEBUG:root:[0031]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 130}
DEBUG:root:[0032]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 130}
DEBUG:root:[0033]: add y 11 - {'w': 1, 'x': 1, 'y': 1, 'z': 130}
DEBUG:root:[0034]: mul y x - {'w': 1, 'x': 1, 'y': 12, 'z': 130}
DEBUG:root:[0035]: add z y - {'w': 1, 'x': 1, 'y': 12, 'z': 130}
DEBUG:root:[0036]: inp w - {'w': 1, 'x': 1, 'y': 12, 'z': 142}
DEBUG:root:[0037]: mul x 0 - {'w': 1, 'x': 1, 'y': 12, 'z': 142}
DEBUG:root:[0038]: add x z - {'w': 1, 'x': 0, 'y': 12, 'z': 142}
DEBUG:root:[0039]: mod x 26 - {'w': 1, 'x': 142, 'y': 12, 'z': 142}
DEBUG:root:[0040]: div z 1 - {'w': 1, 'x': 12, 'y': 12, 'z': 142}
DEBUG:root:[0041]: add x 13 - {'w': 1, 'x': 12, 'y': 12, 'z': 142}
DEBUG:root:[0042]: eql x w - {'w': 1, 'x': 25, 'y': 12, 'z': 142}
DEBUG:root:[0043]: eql x 0 - {'w': 1, 'x': 0, 'y': 12, 'z': 142}
DEBUG:root:[0044]: mul y 0 - {'w': 1, 'x': 1, 'y': 12, 'z': 142}
DEBUG:root:[0045]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 142}
DEBUG:root:[0046]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 142}
DEBUG:root:[0047]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 142}
DEBUG:root:[0048]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 142}
DEBUG:root:[0049]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 3692}
DEBUG:root:[0050]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 3692}
DEBUG:root:[0051]: add y 5 - {'w': 1, 'x': 1, 'y': 1, 'z': 3692}
DEBUG:root:[0052]: mul y x - {'w': 1, 'x': 1, 'y': 6, 'z': 3692}
DEBUG:root:[0053]: add z y - {'w': 1, 'x': 1, 'y': 6, 'z': 3692}
DEBUG:root:[0054]: inp w - {'w': 1, 'x': 1, 'y': 6, 'z': 3698}
DEBUG:root:[0055]: mul x 0 - {'w': 1, 'x': 1, 'y': 6, 'z': 3698}
DEBUG:root:[0056]: add x z - {'w': 1, 'x': 0, 'y': 6, 'z': 3698}
DEBUG:root:[0057]: mod x 26 - {'w': 1, 'x': 3698, 'y': 6, 'z': 3698}
DEBUG:root:[0058]: div z 1 - {'w': 1, 'x': 6, 'y': 6, 'z': 3698}
DEBUG:root:[0059]: add x 11 - {'w': 1, 'x': 6, 'y': 6, 'z': 3698}
DEBUG:root:[0060]: eql x w - {'w': 1, 'x': 17, 'y': 6, 'z': 3698}
DEBUG:root:[0061]: eql x 0 - {'w': 1, 'x': 0, 'y': 6, 'z': 3698}
DEBUG:root:[0062]: mul y 0 - {'w': 1, 'x': 1, 'y': 6, 'z': 3698}
DEBUG:root:[0063]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 3698}
DEBUG:root:[0064]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 3698}
DEBUG:root:[0065]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 3698}
DEBUG:root:[0066]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 3698}
DEBUG:root:[0067]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 96148}
DEBUG:root:[0068]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 96148}
DEBUG:root:[0069]: add y 11 - {'w': 1, 'x': 1, 'y': 1, 'z': 96148}
DEBUG:root:[0070]: mul y x - {'w': 1, 'x': 1, 'y': 12, 'z': 96148}
DEBUG:root:[0071]: add z y - {'w': 1, 'x': 1, 'y': 12, 'z': 96148}
DEBUG:root:[0072]: inp w - {'w': 1, 'x': 1, 'y': 12, 'z': 96160}
DEBUG:root:[0073]: mul x 0 - {'w': 1, 'x': 1, 'y': 12, 'z': 96160}
DEBUG:root:[0074]: add x z - {'w': 1, 'x': 0, 'y': 12, 'z': 96160}
DEBUG:root:[0075]: mod x 26 - {'w': 1, 'x': 96160, 'y': 12, 'z': 96160}
DEBUG:root:[0076]: div z 1 - {'w': 1, 'x': 12, 'y': 12, 'z': 96160}
DEBUG:root:[0077]: add x 14 - {'w': 1, 'x': 12, 'y': 12, 'z': 96160}
DEBUG:root:[0078]: eql x w - {'w': 1, 'x': 26, 'y': 12, 'z': 96160}
DEBUG:root:[0079]: eql x 0 - {'w': 1, 'x': 0, 'y': 12, 'z': 96160}
DEBUG:root:[0080]: mul y 0 - {'w': 1, 'x': 1, 'y': 12, 'z': 96160}
DEBUG:root:[0081]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 96160}
DEBUG:root:[0082]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 96160}
DEBUG:root:[0083]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 96160}
DEBUG:root:[0084]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 96160}
DEBUG:root:[0085]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 2500160}
DEBUG:root:[0086]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 2500160}
DEBUG:root:[0087]: add y 14 - {'w': 1, 'x': 1, 'y': 1, 'z': 2500160}
DEBUG:root:[0088]: mul y x - {'w': 1, 'x': 1, 'y': 15, 'z': 2500160}
DEBUG:root:[0089]: add z y - {'w': 1, 'x': 1, 'y': 15, 'z': 2500160}
DEBUG:root:[0090]: inp w - {'w': 1, 'x': 1, 'y': 15, 'z': 2500175}
DEBUG:root:[0091]: mul x 0 - {'w': 1, 'x': 1, 'y': 15, 'z': 2500175}
DEBUG:root:[0092]: add x z - {'w': 1, 'x': 0, 'y': 15, 'z': 2500175}
DEBUG:root:[0093]: mod x 26 - {'w': 1, 'x': 2500175, 'y': 15, 'z': 2500175}
DEBUG:root:[0094]: div z 26 - {'w': 1, 'x': 15, 'y': 15, 'z': 2500175}
DEBUG:root:[0095]: add x -10 - {'w': 1, 'x': 15, 'y': 15, 'z': 96160}
DEBUG:root:[0096]: eql x w - {'w': 1, 'x': 5, 'y': 15, 'z': 96160}
DEBUG:root:[0097]: eql x 0 - {'w': 1, 'x': 0, 'y': 15, 'z': 96160}
DEBUG:root:[0098]: mul y 0 - {'w': 1, 'x': 1, 'y': 15, 'z': 96160}
DEBUG:root:[0099]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 96160}
DEBUG:root:[0100]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 96160}
DEBUG:root:[0101]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 96160}
DEBUG:root:[0102]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 96160}
DEBUG:root:[0103]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 2500160}
DEBUG:root:[0104]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 2500160}
DEBUG:root:[0105]: add y 7 - {'w': 1, 'x': 1, 'y': 1, 'z': 2500160}
DEBUG:root:[0106]: mul y x - {'w': 1, 'x': 1, 'y': 8, 'z': 2500160}
DEBUG:root:[0107]: add z y - {'w': 1, 'x': 1, 'y': 8, 'z': 2500160}
DEBUG:root:[0108]: inp w - {'w': 1, 'x': 1, 'y': 8, 'z': 2500168}
DEBUG:root:[0109]: mul x 0 - {'w': 1, 'x': 1, 'y': 8, 'z': 2500168}
DEBUG:root:[0110]: add x z - {'w': 1, 'x': 0, 'y': 8, 'z': 2500168}
DEBUG:root:[0111]: mod x 26 - {'w': 1, 'x': 2500168, 'y': 8, 'z': 2500168}
DEBUG:root:[0112]: div z 1 - {'w': 1, 'x': 8, 'y': 8, 'z': 2500168}
DEBUG:root:[0113]: add x 11 - {'w': 1, 'x': 8, 'y': 8, 'z': 2500168}
DEBUG:root:[0114]: eql x w - {'w': 1, 'x': 19, 'y': 8, 'z': 2500168}
DEBUG:root:[0115]: eql x 0 - {'w': 1, 'x': 0, 'y': 8, 'z': 2500168}
DEBUG:root:[0116]: mul y 0 - {'w': 1, 'x': 1, 'y': 8, 'z': 2500168}
DEBUG:root:[0117]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 2500168}
DEBUG:root:[0118]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0119]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0120]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 2500168}
DEBUG:root:[0121]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 65004368}
DEBUG:root:[0122]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 65004368}
DEBUG:root:[0123]: add y 11 - {'w': 1, 'x': 1, 'y': 1, 'z': 65004368}
DEBUG:root:[0124]: mul y x - {'w': 1, 'x': 1, 'y': 12, 'z': 65004368}
DEBUG:root:[0125]: add z y - {'w': 1, 'x': 1, 'y': 12, 'z': 65004368}
DEBUG:root:[0126]: inp w - {'w': 1, 'x': 1, 'y': 12, 'z': 65004380}
DEBUG:root:[0127]: mul x 0 - {'w': 1, 'x': 1, 'y': 12, 'z': 65004380}
DEBUG:root:[0128]: add x z - {'w': 1, 'x': 0, 'y': 12, 'z': 65004380}
DEBUG:root:[0129]: mod x 26 - {'w': 1, 'x': 65004380, 'y': 12, 'z': 65004380}
DEBUG:root:[0130]: div z 26 - {'w': 1, 'x': 12, 'y': 12, 'z': 65004380}
DEBUG:root:[0131]: add x -9 - {'w': 1, 'x': 12, 'y': 12, 'z': 2500168}
DEBUG:root:[0132]: eql x w - {'w': 1, 'x': 3, 'y': 12, 'z': 2500168}
DEBUG:root:[0133]: eql x 0 - {'w': 1, 'x': 0, 'y': 12, 'z': 2500168}
DEBUG:root:[0134]: mul y 0 - {'w': 1, 'x': 1, 'y': 12, 'z': 2500168}
DEBUG:root:[0135]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 2500168}
DEBUG:root:[0136]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0137]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0138]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 2500168}
DEBUG:root:[0139]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 65004368}
DEBUG:root:[0140]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 65004368}
DEBUG:root:[0141]: add y 4 - {'w': 1, 'x': 1, 'y': 1, 'z': 65004368}
DEBUG:root:[0142]: mul y x - {'w': 1, 'x': 1, 'y': 5, 'z': 65004368}
DEBUG:root:[0143]: add z y - {'w': 1, 'x': 1, 'y': 5, 'z': 65004368}
DEBUG:root:[0144]: inp w - {'w': 1, 'x': 1, 'y': 5, 'z': 65004373}
DEBUG:root:[0145]: mul x 0 - {'w': 1, 'x': 1, 'y': 5, 'z': 65004373}
DEBUG:root:[0146]: add x z - {'w': 1, 'x': 0, 'y': 5, 'z': 65004373}
DEBUG:root:[0147]: mod x 26 - {'w': 1, 'x': 65004373, 'y': 5, 'z': 65004373}
DEBUG:root:[0148]: div z 26 - {'w': 1, 'x': 5, 'y': 5, 'z': 65004373}
DEBUG:root:[0149]: add x -3 - {'w': 1, 'x': 5, 'y': 5, 'z': 2500168}
DEBUG:root:[0150]: eql x w - {'w': 1, 'x': 2, 'y': 5, 'z': 2500168}
DEBUG:root:[0151]: eql x 0 - {'w': 1, 'x': 0, 'y': 5, 'z': 2500168}
DEBUG:root:[0152]: mul y 0 - {'w': 1, 'x': 1, 'y': 5, 'z': 2500168}
DEBUG:root:[0153]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 2500168}
DEBUG:root:[0154]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0155]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0156]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 2500168}
DEBUG:root:[0157]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 65004368}
DEBUG:root:[0158]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 65004368}
DEBUG:root:[0159]: add y 6 - {'w': 1, 'x': 1, 'y': 1, 'z': 65004368}
DEBUG:root:[0160]: mul y x - {'w': 1, 'x': 1, 'y': 7, 'z': 65004368}
DEBUG:root:[0161]: add z y - {'w': 1, 'x': 1, 'y': 7, 'z': 65004368}
DEBUG:root:[0162]: inp w - {'w': 1, 'x': 1, 'y': 7, 'z': 65004375}
DEBUG:root:[0163]: mul x 0 - {'w': 1, 'x': 1, 'y': 7, 'z': 65004375}
DEBUG:root:[0164]: add x z - {'w': 1, 'x': 0, 'y': 7, 'z': 65004375}
DEBUG:root:[0165]: mod x 26 - {'w': 1, 'x': 65004375, 'y': 7, 'z': 65004375}
DEBUG:root:[0166]: div z 1 - {'w': 1, 'x': 7, 'y': 7, 'z': 65004375}
DEBUG:root:[0167]: add x 13 - {'w': 1, 'x': 7, 'y': 7, 'z': 65004375}
DEBUG:root:[0168]: eql x w - {'w': 1, 'x': 20, 'y': 7, 'z': 65004375}
DEBUG:root:[0169]: eql x 0 - {'w': 1, 'x': 0, 'y': 7, 'z': 65004375}
DEBUG:root:[0170]: mul y 0 - {'w': 1, 'x': 1, 'y': 7, 'z': 65004375}
DEBUG:root:[0171]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 65004375}
DEBUG:root:[0172]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 65004375}
DEBUG:root:[0173]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 65004375}
DEBUG:root:[0174]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 65004375}
DEBUG:root:[0175]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 1690113750}
DEBUG:root:[0176]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 1690113750}
DEBUG:root:[0177]: add y 5 - {'w': 1, 'x': 1, 'y': 1, 'z': 1690113750}
DEBUG:root:[0178]: mul y x - {'w': 1, 'x': 1, 'y': 6, 'z': 1690113750}
DEBUG:root:[0179]: add z y - {'w': 1, 'x': 1, 'y': 6, 'z': 1690113750}
DEBUG:root:[0180]: inp w - {'w': 1, 'x': 1, 'y': 6, 'z': 1690113756}
DEBUG:root:[0181]: mul x 0 - {'w': 1, 'x': 1, 'y': 6, 'z': 1690113756}
DEBUG:root:[0182]: add x z - {'w': 1, 'x': 0, 'y': 6, 'z': 1690113756}
DEBUG:root:[0183]: mod x 26 - {'w': 1, 'x': 1690113756, 'y': 6, 'z': 1690113756}
DEBUG:root:[0184]: div z 26 - {'w': 1, 'x': 6, 'y': 6, 'z': 1690113756}
DEBUG:root:[0185]: add x -5 - {'w': 1, 'x': 6, 'y': 6, 'z': 65004375}
DEBUG:root:[0186]: eql x w - {'w': 1, 'x': 1, 'y': 6, 'z': 65004375}
DEBUG:root:[0187]: eql x 0 - {'w': 1, 'x': 1, 'y': 6, 'z': 65004375}
DEBUG:root:[0188]: mul y 0 - {'w': 1, 'x': 0, 'y': 6, 'z': 65004375}
DEBUG:root:[0189]: add y 25 - {'w': 1, 'x': 0, 'y': 0, 'z': 65004375}
DEBUG:root:[0190]: mul y x - {'w': 1, 'x': 0, 'y': 25, 'z': 65004375}
DEBUG:root:[0191]: add y 1 - {'w': 1, 'x': 0, 'y': 0, 'z': 65004375}
DEBUG:root:[0192]: mul z y - {'w': 1, 'x': 0, 'y': 1, 'z': 65004375}
DEBUG:root:[0193]: mul y 0 - {'w': 1, 'x': 0, 'y': 1, 'z': 65004375}
DEBUG:root:[0194]: add y w - {'w': 1, 'x': 0, 'y': 0, 'z': 65004375}
DEBUG:root:[0195]: add y 9 - {'w': 1, 'x': 0, 'y': 1, 'z': 65004375}
DEBUG:root:[0196]: mul y x - {'w': 1, 'x': 0, 'y': 10, 'z': 65004375}
DEBUG:root:[0197]: add z y - {'w': 1, 'x': 0, 'y': 0, 'z': 65004375}
DEBUG:root:[0198]: inp w - {'w': 1, 'x': 0, 'y': 0, 'z': 65004375}
DEBUG:root:[0199]: mul x 0 - {'w': 1, 'x': 0, 'y': 0, 'z': 65004375}
DEBUG:root:[0200]: add x z - {'w': 1, 'x': 0, 'y': 0, 'z': 65004375}
DEBUG:root:[0201]: mod x 26 - {'w': 1, 'x': 65004375, 'y': 0, 'z': 65004375}
DEBUG:root:[0202]: div z 26 - {'w': 1, 'x': 7, 'y': 0, 'z': 65004375}
DEBUG:root:[0203]: add x -10 - {'w': 1, 'x': 7, 'y': 0, 'z': 2500168}
DEBUG:root:[0204]: eql x w - {'w': 1, 'x': -3, 'y': 0, 'z': 2500168}
DEBUG:root:[0205]: eql x 0 - {'w': 1, 'x': 0, 'y': 0, 'z': 2500168}
DEBUG:root:[0206]: mul y 0 - {'w': 1, 'x': 1, 'y': 0, 'z': 2500168}
DEBUG:root:[0207]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 2500168}
DEBUG:root:[0208]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0209]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0210]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 2500168}
DEBUG:root:[0211]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 65004368}
DEBUG:root:[0212]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 65004368}
DEBUG:root:[0213]: add y 12 - {'w': 1, 'x': 1, 'y': 1, 'z': 65004368}
DEBUG:root:[0214]: mul y x - {'w': 1, 'x': 1, 'y': 13, 'z': 65004368}
DEBUG:root:[0215]: add z y - {'w': 1, 'x': 1, 'y': 13, 'z': 65004368}
DEBUG:root:[0216]: inp w - {'w': 1, 'x': 1, 'y': 13, 'z': 65004381}
DEBUG:root:[0217]: mul x 0 - {'w': 9, 'x': 1, 'y': 13, 'z': 65004381}
DEBUG:root:[0218]: add x z - {'w': 9, 'x': 0, 'y': 13, 'z': 65004381}
DEBUG:root:[0219]: mod x 26 - {'w': 9, 'x': 65004381, 'y': 13, 'z': 65004381}
DEBUG:root:[0220]: div z 26 - {'w': 9, 'x': 13, 'y': 13, 'z': 65004381}
DEBUG:root:[0221]: add x -4 - {'w': 9, 'x': 13, 'y': 13, 'z': 2500168}
DEBUG:root:[0222]: eql x w - {'w': 9, 'x': 9, 'y': 13, 'z': 2500168}
DEBUG:root:[0223]: eql x 0 - {'w': 9, 'x': 1, 'y': 13, 'z': 2500168}
DEBUG:root:[0224]: mul y 0 - {'w': 9, 'x': 0, 'y': 13, 'z': 2500168}
DEBUG:root:[0225]: add y 25 - {'w': 9, 'x': 0, 'y': 0, 'z': 2500168}
DEBUG:root:[0226]: mul y x - {'w': 9, 'x': 0, 'y': 25, 'z': 2500168}
DEBUG:root:[0227]: add y 1 - {'w': 9, 'x': 0, 'y': 0, 'z': 2500168}
DEBUG:root:[0228]: mul z y - {'w': 9, 'x': 0, 'y': 1, 'z': 2500168}
DEBUG:root:[0229]: mul y 0 - {'w': 9, 'x': 0, 'y': 1, 'z': 2500168}
DEBUG:root:[0230]: add y w - {'w': 9, 'x': 0, 'y': 0, 'z': 2500168}
DEBUG:root:[0231]: add y 14 - {'w': 9, 'x': 0, 'y': 9, 'z': 2500168}
DEBUG:root:[0232]: mul y x - {'w': 9, 'x': 0, 'y': 23, 'z': 2500168}
DEBUG:root:[0233]: add z y - {'w': 9, 'x': 0, 'y': 0, 'z': 2500168}
DEBUG:root:[0234]: inp w - {'w': 9, 'x': 0, 'y': 0, 'z': 2500168}
DEBUG:root:[0235]: mul x 0 - {'w': 3, 'x': 0, 'y': 0, 'z': 2500168}
DEBUG:root:[0236]: add x z - {'w': 3, 'x': 0, 'y': 0, 'z': 2500168}
DEBUG:root:[0237]: mod x 26 - {'w': 3, 'x': 2500168, 'y': 0, 'z': 2500168}
DEBUG:root:[0238]: div z 26 - {'w': 3, 'x': 8, 'y': 0, 'z': 2500168}
DEBUG:root:[0239]: add x -5 - {'w': 3, 'x': 8, 'y': 0, 'z': 96160}
DEBUG:root:[0240]: eql x w - {'w': 3, 'x': 3, 'y': 0, 'z': 96160}
DEBUG:root:[0241]: eql x 0 - {'w': 3, 'x': 1, 'y': 0, 'z': 96160}
DEBUG:root:[0242]: mul y 0 - {'w': 3, 'x': 0, 'y': 0, 'z': 96160}
DEBUG:root:[0243]: add y 25 - {'w': 3, 'x': 0, 'y': 0, 'z': 96160}
DEBUG:root:[0244]: mul y x - {'w': 3, 'x': 0, 'y': 25, 'z': 96160}
DEBUG:root:[0245]: add y 1 - {'w': 3, 'x': 0, 'y': 0, 'z': 96160}
DEBUG:root:[0246]: mul z y - {'w': 3, 'x': 0, 'y': 1, 'z': 96160}
DEBUG:root:[0247]: mul y 0 - {'w': 3, 'x': 0, 'y': 1, 'z': 96160}
DEBUG:root:[0248]: add y w - {'w': 3, 'x': 0, 'y': 0, 'z': 96160}
DEBUG:root:[0249]: add y 14 - {'w': 3, 'x': 0, 'y': 3, 'z': 96160}
DEBUG:root:[0250]: mul y x - {'w': 3, 'x': 0, 'y': 17, 'z': 96160}
DEBUG:root:[0251]: add z y - {'w': 3, 'x': 0, 'y': 0, 'z': 96160}
INFO:root:Invalid model number: (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 3). alu.vars={'w': 3, 'x': 0, 'y': 0, 'z': 96160}
INFO:root:Analyzing input value (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1):
DEBUG:root:Initializing new ALU with program of length 252.
DEBUG:root:Running program of length 252.
DEBUG:root:[0000]: inp w - {'w': 0, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0001]: mul x 0 - {'w': 1, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0002]: add x z - {'w': 1, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0003]: mod x 26 - {'w': 1, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0004]: div z 1 - {'w': 1, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0005]: add x 12 - {'w': 1, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0006]: eql x w - {'w': 1, 'x': 12, 'y': 0, 'z': 0}
DEBUG:root:[0007]: eql x 0 - {'w': 1, 'x': 0, 'y': 0, 'z': 0}
DEBUG:root:[0008]: mul y 0 - {'w': 1, 'x': 1, 'y': 0, 'z': 0}
DEBUG:root:[0009]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 0}
DEBUG:root:[0010]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 0}
DEBUG:root:[0011]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 0}
DEBUG:root:[0012]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 0}
DEBUG:root:[0013]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 0}
DEBUG:root:[0014]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 0}
DEBUG:root:[0015]: add y 4 - {'w': 1, 'x': 1, 'y': 1, 'z': 0}
DEBUG:root:[0016]: mul y x - {'w': 1, 'x': 1, 'y': 5, 'z': 0}
DEBUG:root:[0017]: add z y - {'w': 1, 'x': 1, 'y': 5, 'z': 0}
DEBUG:root:[0018]: inp w - {'w': 1, 'x': 1, 'y': 5, 'z': 5}
DEBUG:root:[0019]: mul x 0 - {'w': 1, 'x': 1, 'y': 5, 'z': 5}
DEBUG:root:[0020]: add x z - {'w': 1, 'x': 0, 'y': 5, 'z': 5}
DEBUG:root:[0021]: mod x 26 - {'w': 1, 'x': 5, 'y': 5, 'z': 5}
DEBUG:root:[0022]: div z 1 - {'w': 1, 'x': 5, 'y': 5, 'z': 5}
DEBUG:root:[0023]: add x 11 - {'w': 1, 'x': 5, 'y': 5, 'z': 5}
DEBUG:root:[0024]: eql x w - {'w': 1, 'x': 16, 'y': 5, 'z': 5}
DEBUG:root:[0025]: eql x 0 - {'w': 1, 'x': 0, 'y': 5, 'z': 5}
DEBUG:root:[0026]: mul y 0 - {'w': 1, 'x': 1, 'y': 5, 'z': 5}
DEBUG:root:[0027]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 5}
DEBUG:root:[0028]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 5}
DEBUG:root:[0029]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 5}
DEBUG:root:[0030]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 5}
DEBUG:root:[0031]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 130}
DEBUG:root:[0032]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 130}
DEBUG:root:[0033]: add y 11 - {'w': 1, 'x': 1, 'y': 1, 'z': 130}
DEBUG:root:[0034]: mul y x - {'w': 1, 'x': 1, 'y': 12, 'z': 130}
DEBUG:root:[0035]: add z y - {'w': 1, 'x': 1, 'y': 12, 'z': 130}
DEBUG:root:[0036]: inp w - {'w': 1, 'x': 1, 'y': 12, 'z': 142}
DEBUG:root:[0037]: mul x 0 - {'w': 1, 'x': 1, 'y': 12, 'z': 142}
DEBUG:root:[0038]: add x z - {'w': 1, 'x': 0, 'y': 12, 'z': 142}
DEBUG:root:[0039]: mod x 26 - {'w': 1, 'x': 142, 'y': 12, 'z': 142}
DEBUG:root:[0040]: div z 1 - {'w': 1, 'x': 12, 'y': 12, 'z': 142}
DEBUG:root:[0041]: add x 13 - {'w': 1, 'x': 12, 'y': 12, 'z': 142}
DEBUG:root:[0042]: eql x w - {'w': 1, 'x': 25, 'y': 12, 'z': 142}
DEBUG:root:[0043]: eql x 0 - {'w': 1, 'x': 0, 'y': 12, 'z': 142}
DEBUG:root:[0044]: mul y 0 - {'w': 1, 'x': 1, 'y': 12, 'z': 142}
DEBUG:root:[0045]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 142}
DEBUG:root:[0046]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 142}
DEBUG:root:[0047]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 142}
DEBUG:root:[0048]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 142}
DEBUG:root:[0049]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 3692}
DEBUG:root:[0050]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 3692}
DEBUG:root:[0051]: add y 5 - {'w': 1, 'x': 1, 'y': 1, 'z': 3692}
DEBUG:root:[0052]: mul y x - {'w': 1, 'x': 1, 'y': 6, 'z': 3692}
DEBUG:root:[0053]: add z y - {'w': 1, 'x': 1, 'y': 6, 'z': 3692}
DEBUG:root:[0054]: inp w - {'w': 1, 'x': 1, 'y': 6, 'z': 3698}
DEBUG:root:[0055]: mul x 0 - {'w': 1, 'x': 1, 'y': 6, 'z': 3698}
DEBUG:root:[0056]: add x z - {'w': 1, 'x': 0, 'y': 6, 'z': 3698}
DEBUG:root:[0057]: mod x 26 - {'w': 1, 'x': 3698, 'y': 6, 'z': 3698}
DEBUG:root:[0058]: div z 1 - {'w': 1, 'x': 6, 'y': 6, 'z': 3698}
DEBUG:root:[0059]: add x 11 - {'w': 1, 'x': 6, 'y': 6, 'z': 3698}
DEBUG:root:[0060]: eql x w - {'w': 1, 'x': 17, 'y': 6, 'z': 3698}
DEBUG:root:[0061]: eql x 0 - {'w': 1, 'x': 0, 'y': 6, 'z': 3698}
DEBUG:root:[0062]: mul y 0 - {'w': 1, 'x': 1, 'y': 6, 'z': 3698}
DEBUG:root:[0063]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 3698}
DEBUG:root:[0064]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 3698}
DEBUG:root:[0065]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 3698}
DEBUG:root:[0066]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 3698}
DEBUG:root:[0067]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 96148}
DEBUG:root:[0068]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 96148}
DEBUG:root:[0069]: add y 11 - {'w': 1, 'x': 1, 'y': 1, 'z': 96148}
DEBUG:root:[0070]: mul y x - {'w': 1, 'x': 1, 'y': 12, 'z': 96148}
DEBUG:root:[0071]: add z y - {'w': 1, 'x': 1, 'y': 12, 'z': 96148}
DEBUG:root:[0072]: inp w - {'w': 1, 'x': 1, 'y': 12, 'z': 96160}
DEBUG:root:[0073]: mul x 0 - {'w': 1, 'x': 1, 'y': 12, 'z': 96160}
DEBUG:root:[0074]: add x z - {'w': 1, 'x': 0, 'y': 12, 'z': 96160}
DEBUG:root:[0075]: mod x 26 - {'w': 1, 'x': 96160, 'y': 12, 'z': 96160}
DEBUG:root:[0076]: div z 1 - {'w': 1, 'x': 12, 'y': 12, 'z': 96160}
DEBUG:root:[0077]: add x 14 - {'w': 1, 'x': 12, 'y': 12, 'z': 96160}
DEBUG:root:[0078]: eql x w - {'w': 1, 'x': 26, 'y': 12, 'z': 96160}
DEBUG:root:[0079]: eql x 0 - {'w': 1, 'x': 0, 'y': 12, 'z': 96160}
DEBUG:root:[0080]: mul y 0 - {'w': 1, 'x': 1, 'y': 12, 'z': 96160}
DEBUG:root:[0081]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 96160}
DEBUG:root:[0082]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 96160}
DEBUG:root:[0083]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 96160}
DEBUG:root:[0084]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 96160}
DEBUG:root:[0085]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 2500160}
DEBUG:root:[0086]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 2500160}
DEBUG:root:[0087]: add y 14 - {'w': 1, 'x': 1, 'y': 1, 'z': 2500160}
DEBUG:root:[0088]: mul y x - {'w': 1, 'x': 1, 'y': 15, 'z': 2500160}
DEBUG:root:[0089]: add z y - {'w': 1, 'x': 1, 'y': 15, 'z': 2500160}
DEBUG:root:[0090]: inp w - {'w': 1, 'x': 1, 'y': 15, 'z': 2500175}
DEBUG:root:[0091]: mul x 0 - {'w': 1, 'x': 1, 'y': 15, 'z': 2500175}
DEBUG:root:[0092]: add x z - {'w': 1, 'x': 0, 'y': 15, 'z': 2500175}
DEBUG:root:[0093]: mod x 26 - {'w': 1, 'x': 2500175, 'y': 15, 'z': 2500175}
DEBUG:root:[0094]: div z 26 - {'w': 1, 'x': 15, 'y': 15, 'z': 2500175}
DEBUG:root:[0095]: add x -10 - {'w': 1, 'x': 15, 'y': 15, 'z': 96160}
DEBUG:root:[0096]: eql x w - {'w': 1, 'x': 5, 'y': 15, 'z': 96160}
DEBUG:root:[0097]: eql x 0 - {'w': 1, 'x': 0, 'y': 15, 'z': 96160}
DEBUG:root:[0098]: mul y 0 - {'w': 1, 'x': 1, 'y': 15, 'z': 96160}
DEBUG:root:[0099]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 96160}
DEBUG:root:[0100]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 96160}
DEBUG:root:[0101]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 96160}
DEBUG:root:[0102]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 96160}
DEBUG:root:[0103]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 2500160}
DEBUG:root:[0104]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 2500160}
DEBUG:root:[0105]: add y 7 - {'w': 1, 'x': 1, 'y': 1, 'z': 2500160}
DEBUG:root:[0106]: mul y x - {'w': 1, 'x': 1, 'y': 8, 'z': 2500160}
DEBUG:root:[0107]: add z y - {'w': 1, 'x': 1, 'y': 8, 'z': 2500160}
DEBUG:root:[0108]: inp w - {'w': 1, 'x': 1, 'y': 8, 'z': 2500168}
DEBUG:root:[0109]: mul x 0 - {'w': 1, 'x': 1, 'y': 8, 'z': 2500168}
DEBUG:root:[0110]: add x z - {'w': 1, 'x': 0, 'y': 8, 'z': 2500168}
DEBUG:root:[0111]: mod x 26 - {'w': 1, 'x': 2500168, 'y': 8, 'z': 2500168}
DEBUG:root:[0112]: div z 1 - {'w': 1, 'x': 8, 'y': 8, 'z': 2500168}
DEBUG:root:[0113]: add x 11 - {'w': 1, 'x': 8, 'y': 8, 'z': 2500168}
DEBUG:root:[0114]: eql x w - {'w': 1, 'x': 19, 'y': 8, 'z': 2500168}
DEBUG:root:[0115]: eql x 0 - {'w': 1, 'x': 0, 'y': 8, 'z': 2500168}
DEBUG:root:[0116]: mul y 0 - {'w': 1, 'x': 1, 'y': 8, 'z': 2500168}
DEBUG:root:[0117]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 2500168}
DEBUG:root:[0118]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0119]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0120]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 2500168}
DEBUG:root:[0121]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 65004368}
DEBUG:root:[0122]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 65004368}
DEBUG:root:[0123]: add y 11 - {'w': 1, 'x': 1, 'y': 1, 'z': 65004368}
DEBUG:root:[0124]: mul y x - {'w': 1, 'x': 1, 'y': 12, 'z': 65004368}
DEBUG:root:[0125]: add z y - {'w': 1, 'x': 1, 'y': 12, 'z': 65004368}
DEBUG:root:[0126]: inp w - {'w': 1, 'x': 1, 'y': 12, 'z': 65004380}
DEBUG:root:[0127]: mul x 0 - {'w': 1, 'x': 1, 'y': 12, 'z': 65004380}
DEBUG:root:[0128]: add x z - {'w': 1, 'x': 0, 'y': 12, 'z': 65004380}
DEBUG:root:[0129]: mod x 26 - {'w': 1, 'x': 65004380, 'y': 12, 'z': 65004380}
DEBUG:root:[0130]: div z 26 - {'w': 1, 'x': 12, 'y': 12, 'z': 65004380}
DEBUG:root:[0131]: add x -9 - {'w': 1, 'x': 12, 'y': 12, 'z': 2500168}
DEBUG:root:[0132]: eql x w - {'w': 1, 'x': 3, 'y': 12, 'z': 2500168}
DEBUG:root:[0133]: eql x 0 - {'w': 1, 'x': 0, 'y': 12, 'z': 2500168}
DEBUG:root:[0134]: mul y 0 - {'w': 1, 'x': 1, 'y': 12, 'z': 2500168}
DEBUG:root:[0135]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 2500168}
DEBUG:root:[0136]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0137]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0138]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 2500168}
DEBUG:root:[0139]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 65004368}
DEBUG:root:[0140]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 65004368}
DEBUG:root:[0141]: add y 4 - {'w': 1, 'x': 1, 'y': 1, 'z': 65004368}
DEBUG:root:[0142]: mul y x - {'w': 1, 'x': 1, 'y': 5, 'z': 65004368}
DEBUG:root:[0143]: add z y - {'w': 1, 'x': 1, 'y': 5, 'z': 65004368}
DEBUG:root:[0144]: inp w - {'w': 1, 'x': 1, 'y': 5, 'z': 65004373}
DEBUG:root:[0145]: mul x 0 - {'w': 1, 'x': 1, 'y': 5, 'z': 65004373}
DEBUG:root:[0146]: add x z - {'w': 1, 'x': 0, 'y': 5, 'z': 65004373}
DEBUG:root:[0147]: mod x 26 - {'w': 1, 'x': 65004373, 'y': 5, 'z': 65004373}
DEBUG:root:[0148]: div z 26 - {'w': 1, 'x': 5, 'y': 5, 'z': 65004373}
DEBUG:root:[0149]: add x -3 - {'w': 1, 'x': 5, 'y': 5, 'z': 2500168}
DEBUG:root:[0150]: eql x w - {'w': 1, 'x': 2, 'y': 5, 'z': 2500168}
DEBUG:root:[0151]: eql x 0 - {'w': 1, 'x': 0, 'y': 5, 'z': 2500168}
DEBUG:root:[0152]: mul y 0 - {'w': 1, 'x': 1, 'y': 5, 'z': 2500168}
DEBUG:root:[0153]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 2500168}
DEBUG:root:[0154]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0155]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 2500168}
DEBUG:root:[0156]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 2500168}
DEBUG:root:[0157]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 65004368}
DEBUG:root:[0158]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 65004368}
DEBUG:root:[0159]: add y 6 - {'w': 1, 'x': 1, 'y': 1, 'z': 65004368}
DEBUG:root:[0160]: mul y x - {'w': 1, 'x': 1, 'y': 7, 'z': 65004368}
DEBUG:root:[0161]: add z y - {'w': 1, 'x': 1, 'y': 7, 'z': 65004368}
DEBUG:root:[0162]: inp w - {'w': 1, 'x': 1, 'y': 7, 'z': 65004375}
DEBUG:root:[0163]: mul x 0 - {'w': 1, 'x': 1, 'y': 7, 'z': 65004375}
DEBUG:root:[0164]: add x z - {'w': 1, 'x': 0, 'y': 7, 'z': 65004375}
DEBUG:root:[0165]: mod x 26 - {'w': 1, 'x': 65004375, 'y': 7, 'z': 65004375}
DEBUG:root:[0166]: div z 1 - {'w': 1, 'x': 7, 'y': 7, 'z': 65004375}
DEBUG:root:[0167]: add x 13 - {'w': 1, 'x': 7, 'y': 7, 'z': 65004375}
DEBUG:root:[0168]: eql x w - {'w': 1, 'x': 20, 'y': 7, 'z': 65004375}
DEBUG:root:[0169]: eql x 0 - {'w': 1, 'x': 0, 'y': 7, 'z': 65004375}
DEBUG:root:[0170]: mul y 0 - {'w': 1, 'x': 1, 'y': 7, 'z': 65004375}
DEBUG:root:[0171]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 65004375}
DEBUG:root:[0172]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 65004375}
DEBUG:root:[0173]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 65004375}
DEBUG:root:[0174]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 65004375}
DEBUG:root:[0175]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 1690113750}
DEBUG:root:[0176]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 1690113750}
DEBUG:root:[0177]: add y 5 - {'w': 1, 'x': 1, 'y': 1, 'z': 1690113750}
DEBUG:root:[0178]: mul y x - {'w': 1, 'x': 1, 'y': 6, 'z': 1690113750}
DEBUG:root:[0179]: add z y - {'w': 1, 'x': 1, 'y': 6, 'z': 1690113750}
DEBUG:root:[0180]: inp w - {'w': 1, 'x': 1, 'y': 6, 'z': 1690113756}
DEBUG:root:[0181]: mul x 0 - {'w': 2, 'x': 1, 'y': 6, 'z': 1690113756}
DEBUG:root:[0182]: add x z - {'w': 2, 'x': 0, 'y': 6, 'z': 1690113756}
DEBUG:root:[0183]: mod x 26 - {'w': 2, 'x': 1690113756, 'y': 6, 'z': 1690113756}
DEBUG:root:[0184]: div z 26 - {'w': 2, 'x': 6, 'y': 6, 'z': 1690113756}
DEBUG:root:[0185]: add x -5 - {'w': 2, 'x': 6, 'y': 6, 'z': 65004375}
DEBUG:root:[0186]: eql x w - {'w': 2, 'x': 1, 'y': 6, 'z': 65004375}
DEBUG:root:[0187]: eql x 0 - {'w': 2, 'x': 0, 'y': 6, 'z': 65004375}
DEBUG:root:[0188]: mul y 0 - {'w': 2, 'x': 1, 'y': 6, 'z': 65004375}
DEBUG:root:[0189]: add y 25 - {'w': 2, 'x': 1, 'y': 0, 'z': 65004375}
DEBUG:root:[0190]: mul y x - {'w': 2, 'x': 1, 'y': 25, 'z': 65004375}
DEBUG:root:[0191]: add y 1 - {'w': 2, 'x': 1, 'y': 25, 'z': 65004375}
DEBUG:root:[0192]: mul z y - {'w': 2, 'x': 1, 'y': 26, 'z': 65004375}
DEBUG:root:[0193]: mul y 0 - {'w': 2, 'x': 1, 'y': 26, 'z': 1690113750}
DEBUG:root:[0194]: add y w - {'w': 2, 'x': 1, 'y': 0, 'z': 1690113750}
DEBUG:root:[0195]: add y 9 - {'w': 2, 'x': 1, 'y': 2, 'z': 1690113750}
DEBUG:root:[0196]: mul y x - {'w': 2, 'x': 1, 'y': 11, 'z': 1690113750}
DEBUG:root:[0197]: add z y - {'w': 2, 'x': 1, 'y': 11, 'z': 1690113750}
DEBUG:root:[0198]: inp w - {'w': 2, 'x': 1, 'y': 11, 'z': 1690113761}
DEBUG:root:[0199]: mul x 0 - {'w': 2, 'x': 1, 'y': 11, 'z': 1690113761}
DEBUG:root:[0200]: add x z - {'w': 2, 'x': 0, 'y': 11, 'z': 1690113761}
DEBUG:root:[0201]: mod x 26 - {'w': 2, 'x': 1690113761, 'y': 11, 'z': 1690113761}
DEBUG:root:[0202]: div z 26 - {'w': 2, 'x': 11, 'y': 11, 'z': 1690113761}
DEBUG:root:[0203]: add x -10 - {'w': 2, 'x': 11, 'y': 11, 'z': 65004375}
DEBUG:root:[0204]: eql x w - {'w': 2, 'x': 1, 'y': 11, 'z': 65004375}
DEBUG:root:[0205]: eql x 0 - {'w': 2, 'x': 0, 'y': 11, 'z': 65004375}
DEBUG:root:[0206]: mul y 0 - {'w': 2, 'x': 1, 'y': 11, 'z': 65004375}
DEBUG:root:[0207]: add y 25 - {'w': 2, 'x': 1, 'y': 0, 'z': 65004375}
DEBUG:root:[0208]: mul y x - {'w': 2, 'x': 1, 'y': 25, 'z': 65004375}
DEBUG:root:[0209]: add y 1 - {'w': 2, 'x': 1, 'y': 25, 'z': 65004375}
DEBUG:root:[0210]: mul z y - {'w': 2, 'x': 1, 'y': 26, 'z': 65004375}
DEBUG:root:[0211]: mul y 0 - {'w': 2, 'x': 1, 'y': 26, 'z': 1690113750}
DEBUG:root:[0212]: add y w - {'w': 2, 'x': 1, 'y': 0, 'z': 1690113750}
DEBUG:root:[0213]: add y 12 - {'w': 2, 'x': 1, 'y': 2, 'z': 1690113750}
DEBUG:root:[0214]: mul y x - {'w': 2, 'x': 1, 'y': 14, 'z': 1690113750}
DEBUG:root:[0215]: add z y - {'w': 2, 'x': 1, 'y': 14, 'z': 1690113750}
DEBUG:root:[0216]: inp w - {'w': 2, 'x': 1, 'y': 14, 'z': 1690113764}
DEBUG:root:[0217]: mul x 0 - {'w': 1, 'x': 1, 'y': 14, 'z': 1690113764}
DEBUG:root:[0218]: add x z - {'w': 1, 'x': 0, 'y': 14, 'z': 1690113764}
DEBUG:root:[0219]: mod x 26 - {'w': 1, 'x': 1690113764, 'y': 14, 'z': 1690113764}
DEBUG:root:[0220]: div z 26 - {'w': 1, 'x': 14, 'y': 14, 'z': 1690113764}
DEBUG:root:[0221]: add x -4 - {'w': 1, 'x': 14, 'y': 14, 'z': 65004375}
DEBUG:root:[0222]: eql x w - {'w': 1, 'x': 10, 'y': 14, 'z': 65004375}
DEBUG:root:[0223]: eql x 0 - {'w': 1, 'x': 0, 'y': 14, 'z': 65004375}
DEBUG:root:[0224]: mul y 0 - {'w': 1, 'x': 1, 'y': 14, 'z': 65004375}
DEBUG:root:[0225]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 65004375}
DEBUG:root:[0226]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 65004375}
DEBUG:root:[0227]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 65004375}
DEBUG:root:[0228]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 65004375}
DEBUG:root:[0229]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 1690113750}
DEBUG:root:[0230]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 1690113750}
DEBUG:root:[0231]: add y 14 - {'w': 1, 'x': 1, 'y': 1, 'z': 1690113750}
DEBUG:root:[0232]: mul y x - {'w': 1, 'x': 1, 'y': 15, 'z': 1690113750}
DEBUG:root:[0233]: add z y - {'w': 1, 'x': 1, 'y': 15, 'z': 1690113750}
DEBUG:root:[0234]: inp w - {'w': 1, 'x': 1, 'y': 15, 'z': 1690113765}
DEBUG:root:[0235]: mul x 0 - {'w': 1, 'x': 1, 'y': 15, 'z': 1690113765}
DEBUG:root:[0236]: add x z - {'w': 1, 'x': 0, 'y': 15, 'z': 1690113765}
DEBUG:root:[0237]: mod x 26 - {'w': 1, 'x': 1690113765, 'y': 15, 'z': 1690113765}
DEBUG:root:[0238]: div z 26 - {'w': 1, 'x': 15, 'y': 15, 'z': 1690113765}
DEBUG:root:[0239]: add x -5 - {'w': 1, 'x': 15, 'y': 15, 'z': 65004375}
DEBUG:root:[0240]: eql x w - {'w': 1, 'x': 10, 'y': 15, 'z': 65004375}
DEBUG:root:[0241]: eql x 0 - {'w': 1, 'x': 0, 'y': 15, 'z': 65004375}
DEBUG:root:[0242]: mul y 0 - {'w': 1, 'x': 1, 'y': 15, 'z': 65004375}
DEBUG:root:[0243]: add y 25 - {'w': 1, 'x': 1, 'y': 0, 'z': 65004375}
DEBUG:root:[0244]: mul y x - {'w': 1, 'x': 1, 'y': 25, 'z': 65004375}
DEBUG:root:[0245]: add y 1 - {'w': 1, 'x': 1, 'y': 25, 'z': 65004375}
DEBUG:root:[0246]: mul z y - {'w': 1, 'x': 1, 'y': 26, 'z': 65004375}
DEBUG:root:[0247]: mul y 0 - {'w': 1, 'x': 1, 'y': 26, 'z': 1690113750}
DEBUG:root:[0248]: add y w - {'w': 1, 'x': 1, 'y': 0, 'z': 1690113750}
DEBUG:root:[0249]: add y 14 - {'w': 1, 'x': 1, 'y': 1, 'z': 1690113750}
DEBUG:root:[0250]: mul y x - {'w': 1, 'x': 1, 'y': 15, 'z': 1690113750}
DEBUG:root:[0251]: add z y - {'w': 1, 'x': 1, 'y': 15, 'z': 1690113750}
INFO:root:Invalid model number: (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1). alu.vars={'w': 1, 'x': 1, 'y': 15, 'z': 1690113765}
```
