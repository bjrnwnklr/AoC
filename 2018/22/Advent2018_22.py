'''
depth: 10689
target: 11,722


- The region at 0,0 (the mouth of the cave) has a geologic index of 0.
- The region at the coordinates of the target has a geologic index of 0.
- If the region's Y coordinate is 0, the geologic index is its X coordinate times 16807.
- If the region's X coordinate is 0, the geologic index is its Y coordinate times 48271.
- Otherwise, the region's geologic index is the result of multiplying the erosion levels
     of the regions at X-1,Y and X,Y-1.
- A region's erosion level is its geologic index plus the cave system's depth, all modulo 20183. Then:

If the erosion level modulo 3 is 0, the region's type is rocky.
If the erosion level modulo 3 is 1, the region's type is wet.
If the erosion level modulo 3 is 2, the region's type is narrow.

Before you go in, you should determine the risk level of the area.
For the rectangle that has a top-left corner of region 0,0 and a bottom-right corner 
of the region containing the target, add up the risk level of each individual region:
0 for rocky regions, 1 for wet regions, and 2 for narrow regions.

--- part 2
In rocky regions, you can use the climbing gear or the torch. You cannot use neither (you'll likely slip and fall).
In wet regions, you can use the climbing gear or neither tool. You cannot use the torch (if it gets wet, you won't have a light source).
In narrow regions, you can use the torch or neither tool. You cannot use the climbing gear (it's too bulky to fit).

Moving to an adjacent region takes 1 minute.
Switching gear takes 7 minutes.

'''


depth = 10689
target = (11, 722)
#depth = 510
#target = (10, 10)
mouth = (0, 0)
erosion_dict = dict()
regions = dict()

def calc_erosion(x, y):
    if (x, y) in erosion_dict:
        return erosion_dict[(x, y)]
    geo_idx = 0
    if (x, y) == mouth:
        geo_idx = 0
    elif (x, y) == target:
        geo_idx = 0
    elif x == 0:
        geo_idx = y * 48271
    elif y == 0:
        geo_idx = x * 16807
    else:
        geo_idx = (calc_erosion(x-1, y) * calc_erosion(x, y-1))
    e = (geo_idx + depth) % 20183
    erosion_dict[(x, y)] = e
    return e

# calculate type
def calc_type(x, y):
    t = calc_erosion(x, y) % 3
    return t

# calculate the grid (regions)
risk_level = 0
for c in range(target[0] + 20):
    for r in range(target[1] + 20):
        #risk_level += calc_type(c, r)
        regions[(c, r)] = calc_type(c, r)

# print(risk_level)

