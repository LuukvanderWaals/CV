def check(p1, p2):
    while p1 and p2:
        i1, i2 = p1.pop(), p2.pop()
        if i1 == i2:
            continue
        if i1 == "]":
            return True
        if i2 == "]":
            return False
        if i1 == "[":
            p2 += ["]", i2]
            continue
        if i2 == "[":
            p1 += ["]", i1]
            continue
        if int(i1) < int(i2):
            return True
        if int(i2) < int(i1):
            return False

packets = open("input.txt", "r").read().split() + ["[[2]]", "[[6]]"]

for _ in range(len(packets)):
    for i in range(len(packets) - 1):
        if not check(*map(lambda x: list(x.replace("[", "[,").replace("]", ",]").replace(",,", ",").split(","))[::-1], packets[i:i + 2])):
            packets[i], packets[i + 1] = packets[i + 1], packets[i]

print((packets.index("[[2]]") + 1) * (packets.index("[[6]]") + 1))
