f = open("input.txt", "r").read()
width = f.index("\n")
height = f.count("\n") + 1
f = f.replace("\n", "")
S = f.find("S")
E = f.find("E")
d = [-width, -1, 1, width]

heights = [0 if c == "S" else 25 if c == "E" else ord(c) - ord("a") for c in f]
# been = {S}
# paths = [(0, S)]

def find_path():
    while paths:
        length, pos = paths[0]
        del paths[0]
        for i in d:
            new_pos = pos + i
            if 0 <= new_pos < len(heights) and heights[new_pos] - heights[pos] <= 1 and new_pos not in been:
                if new_pos == E:
                    return length + 1
                paths.append((length + 1, new_pos))
                been.add(new_pos)

res = None
for i, height in enumerate(heights):
    if height == 0:
        been = {i}
        paths = [(0, i)]
    path = find_path()
    if res == None or (path != None and path < res):
        res = path

print(res)
