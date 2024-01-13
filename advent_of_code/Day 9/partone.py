h = [0, 0]
t = [0, 0]
s = set()

for i in open("input.txt", "r").read().split("\n"):
    d, n = i.split()
    for _ in range(int(n)):
        if d == "L":
            h[0] -= 1
        elif d == "R":
            h[0] += 1
        elif d == "U":
            h[1] -= 1
        elif d == "D":
            h[1] += 1

        if abs(h[0] - t[0]) > 1 or abs(h[1] - t[1]) > 1:
            dx = h[0] - t[0]
            if dx != 0:
                t[0] += dx / abs(dx)
            dy = h[1] - t[1]
            if dy != 0:
                t[1] += dy / abs(dy)

        s.add(tuple(t))

print(len(s))
