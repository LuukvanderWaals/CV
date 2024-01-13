s = set()
max_y = 0

for i in open("input.txt", "r").read().split("\n"):
    i = map(lambda x: map(int, x.split(",")), i.split(" -> "))
    x, y = i.__next__()
    s.add((x, y))
    for new_x, new_y in i:
        while True:
            if x != new_x:
                x += (new_x - x) / abs(new_x - x)
            elif y != new_y:
                y += (new_y - y) / abs(new_y - y)
            else:
                break
            s.add((x, y))
            max_y = max(y + 1, max_y)

count = 0

while True:
    x, y = 500, 0
    while y < max_y:
        if (x, y + 1) not in s:
            y += 1
        elif (x - 1, y + 1) not in s:
            y += 1
            x -= 1
        elif (x + 1, y + 1) not in s:
            y += 1
            x += 1
        else:
            break

    s.add((x, y))
    count += 1

    if (x, y) == (500, 0):
        break

print(count)
