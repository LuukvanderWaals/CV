f = open("input.txt", "r").read()

for i in range(len(f) - 13):
    if len(set(f[i:i + 14])) == 14:
        break

print(i + 14)
