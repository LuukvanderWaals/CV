print(sum(ord(i.split()[1]) - ord("X") + 1 + (ord(i.split()[1]) - ord("X") - ord(i.split()[0]) + ord("A") + 1) % 3 * 3 for i in open("input.txt", "r").read().split("\n")))
