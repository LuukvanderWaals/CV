print(sum((ord(i.split()[1]) - ord("X")) * 3 + (ord(i.split()[1]) - ord("X") + ord(i.split()[0]) - ord("A") + 2) % 3 + 1 for i in open("input.txt", "r").read().split("\n")))
