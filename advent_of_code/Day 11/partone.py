def mul(x):
    return x[0] * x[1]

class Monkey:
    def __init__(self, text):
        text = text.split("\n")
        self.items = list(map(int, text[1][18:].split(", ")))
        self.op = sum if text[2][23] == "+" else mul
        self.n = "old" if text[2][25:] == "old" else int(text[2][25:])
        self.test = int(text[3][21:])
        self.true = int(text[4][29:])
        self.false = int(text[5][30:])
        self.active = 0

    def turn(self, r):
        self.active += len(self.items)
        for item in self.items:
            n = item if self.n == "old" else int(self.n)
            item = self.op((item, n)) // 3
            monkeys[self.true if item % self.test == 0 else self.false].items.append(item)
        self.items = []

monkeys = [Monkey(i) for i in open("input.txt", "r").read().split("\n\n")]

for r in range(20):
    for monkey in range(len(monkeys)):
        monkeys[monkey].turn(r)

print(mul(sorted(monkey.active for monkey in monkeys)[-2:]))

