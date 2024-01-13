res = 0

for i in open("input.txt", "r").read().split("\n"):
    i = list(map(int, i.replace(",", "-").split("-")))
    res += i[0] <= i[3] and i[1] >= i[2]

print(res)
