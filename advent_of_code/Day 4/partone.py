res = 0

for i in open("input.txt", "r").read().split("\n"):
    i1, i2 = map(lambda x: list(map(int, x.split("-"))), i.split(","))
    i1, i2 = set(range(i1[0], i1[1] + 1)), set(range(i2[0], i2[1] + 1))
    res += not (i1 - i2) or not (i2 - i1)


print(res)
