f = open("input.txt", "r").read().split("\n")
crates = list(map(lambda x: list(filter(lambda x: x != " ", x))[::-1], zip(*map(lambda x: list(x[1::4]) + [" "] * (int(f[f.index("") - 1].split()[-1]) - len(x) // 4 - 1), f[:f.index("") - 1]))))

for i in f[f.index("") + 1:]:
    i = list(map(int, i.split()[1::2]))
    crates[i[2] - 1] += crates[i[1] - 1][-i[0]:]
    crates[i[1] - 1] = crates[i[1] - 1][:-i[0]]

for i in crates:
    print(i[-1], end="")
print()
