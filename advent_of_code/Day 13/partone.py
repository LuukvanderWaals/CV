res = 0

for i, packets in enumerate(open("input.txt", "r").read().split("\n\n")):
    p1, p2 = map(lambda x: list(x.replace("[", "[,").replace("]", ",]").replace(",,", ",").split(","))[::-1], packets.split("\n"))
    while p1 and p2:
        i1, i2 = p1.pop(), p2.pop()
        if i1 == i2:
            continue
        if i1 == "]":
            res += i + 1
            break
        if i2 == "]":
            break
        if i1 == "[":
            p2 += ["]", i2]
            continue
        if i2 == "[":
            p1 += ["]", i1]
            continue
        if int(i1) < int(i2):
            res += i + 1
            break
        if int(i2) < int(i1):
            break

print(res)
