RANGE = 4000000

s = list()
for i in open("input.txt", "r").readlines():
    i = i.split(" ")
    i = list(map(lambda x: int(x[2:-1]), (i[2], i[3], i[8], i[9])))
    s.append((i[0], i[1], abs(i[0] - i[2]) + abs(i[1] - i[3])))

for y in range(RANGE + 1):
    r = []
    for i in s:
        i = (i[0] - i[2] + abs(i[1] - y), i[0] + i[2] - abs(i[1] - y))
        if i[0] <= i[1]:
            r.append(i)
    r.sort()
    x = -1
    for i in r:
        while i[0] > x + 1:
            print((x + 1) * RANGE + y)
            x += 1
        x = max(x, i[1])
