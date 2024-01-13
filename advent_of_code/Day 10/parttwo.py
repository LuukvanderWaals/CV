X = 1
cycle = 0
screen = []

res = 0
for i in open("input.txt", "r").read().split("\n"):
    for _ in range(1 if i == "noop" else 2):
        if cycle % 40 == 0:
            screen.append("")
        screen[-1] += "#" if abs(cycle % 40 - X) <= 1 else "."
        cycle += 1


    if i != "noop":
        X += int(i.split()[1])

# print(screen)
print("\n".join(screen))
