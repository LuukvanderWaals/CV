X = 1
cycle = 0
c = 20

res = 0
for i in open("input.txt", "r").read().split("\n"):
    if i == "noop":
        cycle += 1
    else:
        cycle += 2
        X += int(i.split()[1])

    if c - cycle <= 2:
        res += c * X
        c += 40

print(res)
