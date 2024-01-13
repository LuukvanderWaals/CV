res = 0

for i in open("input.txt", "r").read().split("\n"):
    s = int(len(i) / 2)
    i1, i2 = set(i[:s]), set(i[s:])
    l = list(i1.intersection(i2))[0]
    if l.islower():
        res += ord(l) - ord("a") + 1
    else:
        res += ord(l) - ord("A") + 27

print(res)
