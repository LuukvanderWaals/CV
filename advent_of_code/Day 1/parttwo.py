print(sum(sorted(sum(map(int, i.split())) for i in open("input.txt", "r").read().split("\n\n"))[-3:]))
