f = open("input.txt", "r").read()

for i in range(len(f) - 3):
    if len(set(f[i:i + 4])) == 4:
        break

print(i + 4)
