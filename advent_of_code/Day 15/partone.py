s = set()

for i in open("input.txt", "r").readlines():
    i = i.split(" ")
    x, y, bx, by = map(lambda x: int(x[2:-1]), (i[2], i[3], i[8], i[9]))

    d = abs(x - bx) + abs(y - by)
    s = s.union(set(range(x - d + abs(y - 2000000), x + d - abs(y - 2000000) + 1)))
    if by == 2000000:
        s.remove(bx)

print(len(s))
