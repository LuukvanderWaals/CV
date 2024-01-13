rope = [[0, 0] for _ in range(10)]
s = set()

for i in open("input.txt", "r").read().split("\n"):
    d, n = i.split()
    for _ in range(int(n)):
        if d == "L":
            rope[0][0] -= 1
        elif d == "R":
            rope[0][0] += 1
        elif d == "U":
            rope[0][1] -= 1
        elif d == "D":
            rope[0][1] += 1

        for t in range(len(rope) - 1):
            if abs(rope[t][0] - rope[t + 1][0]) > 1 or abs(rope[t][1] - rope[t + 1][1]) > 1:
                dx = rope[t][0] - rope[t + 1][0]
                if dx != 0:
                    rope[t + 1][0] += int(dx / abs(dx))
                dy = rope[t][1] - rope[t + 1][1]
                if dy != 0:
                    rope[t + 1][1] += int(dy / abs(dy))
        print(rope[-1])
        s.add(tuple(rope[-1]))
    print()

print(len(s))
