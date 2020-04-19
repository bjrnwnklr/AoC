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


'''
from heapq import heappop, heappush

##### my input #####
depth = 10689
target = (11, 722)

#### some sample input - should solve to 1087
#depth = 6969
#target = (9, 796)

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

# calculate the grid (regions) - for part 2, calculate +50 more
risk_level = 0
for c in range(target[0] + 50):
    for r in range(target[1] + 50):
        t = calc_type(c, r)
        if c <= target[0] and r <= target[1]: risk_level += t
        regions[(c, r)] = t

print(risk_level)

'''
As you leave, he hands you some tools: a torch and some climbing gear.
 You can't equip both tools at once, but you can choose to use neither.

Tools can only be used in certain regions:

- In rocky regions, you can use the climbing gear or the torch.
     You cannot use neither (you'll likely slip and fall).
- In wet regions, you can use the climbing gear or neither tool.
     You cannot use the torch (if it gets wet, you won't have a light source).
- In narrow regions, you can use the torch or neither tool. 
    You cannot use the climbing gear (it's too bulky to fit).

You start at 0,0 (the mouth of the cave) with the torch equipped and must reach the
target coordinates as quickly as possible. The regions with negative X or Y are solid
rock and cannot be traversed. The fastest route might involve entering regions beyond
the X or Y coordinate of the target.

You can move to an adjacent region (up, down, left, or right; never diagonally)
if your currently equipped tool allows you to enter that region.
Moving to an adjacent region takes one minute. (For example, if you have the
torch equipped, you can move between rocky and narrow regions, but cannot enter wet regions.)

You can change your currently equipped tool or put both away if your new equipment would be 
valid for your current region. Switching to using the climbing gear, torch, 
or neither always takes seven minutes, regardless of which tools you start with. 
(For example, if you are in a rocky region, you can switch from the torch to the 
climbing gear, but you cannot switch to neither.)

Finally, once you reach the target, you need the torch equipped before you can 
find him in the dark. The target is always in a rocky region, so if you arrive 
there with climbing gear equipped, you will need to spend seven minutes switching to your torch.


0 = rocky = neither (can't use neither in rocky)
1 = wet = torch (can't use torch in wet)
2 = narrow = climbing gear (can't use climbing gear in narrow)

'''

n_coords = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def dijkstra(grid, f, t):

    # q elements: (cost, vertex, path, tool equipped at vertex)
    q, seen = [(0, f, (), 1)], set()
    while q:
        (cost, v1, path, tool) = heappop(q)
        if (v1, tool) not in seen:
            #print('%d, %s, %d' % (cost, str(v1), tool))
            seen.add((v1, tool))
            path += ((cost, v1, tool), )
            ##### switch to torch at the end
            if v1 == t and tool == 1: return (cost, path)

            # generate cost for neighbours and 
            # add them to a list
            for n in n_coords:
                v_next = (v1[0] + n[0], v1[1] + n[1])
                if v_next in grid and (v_next, tool) not in seen:
                    t_next = tool
                    c = 1 # cost is at least 1 for moving (with the same tool)
                    # if we can move with current tool, do so
                    if grid[v_next] != t_next:
                        heappush(q, (cost + c, v_next, path, t_next))
                        #print('\t%s: pushed. Tool: %d, cost: %d' % (str(v_next), t_next, cost + c))
                    # try the other two tools as well
                    for i in range(1,3):
                        t_next = (tool + i) % 3
                        # try if we can switch to the next tool (need to check both next area and current area)
                        if grid[v_next] != t_next and grid[v1] != t_next:
                            c += 7
                            heappush(q, (cost + c, v_next, path, t_next))
                            #print('\t%s: pushed. Tool: %d, cost: %d' % (str(v_next), t_next, cost + c))

    return float("inf")


c, p = dijkstra(regions, mouth, target)
print(c)