res = 0

f = open("input.txt", "r").read().split("\n")

for i in range(0, len(f), 3):
    s = map(set, f[i:i + 3])
    l = list(set.intersection(*s))[0]
    if l.islower():
        res += ord(l) - ord("a") + 1
    else:
        res += ord(l) - ord("A") + 27

print(res)
