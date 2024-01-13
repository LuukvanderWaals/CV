grid = list(map(lambda x: list(map(int, x)), open("input.txt", "r").read().split("\n")))

max_score = 0
for y in range(1, len(grid) - 1):
    for x in range(1, len(grid[y]) - 1):
        score = 1

        i = x - 1
        while i > 0 and grid[y][i] < grid[y][x]:
            i -= 1
        score *= x - i

        i = x + 1
        while i < len(grid[y]) - 1 and grid[y][i] < grid[y][x]:
            i += 1
        score *= i - x

        i = y - 1
        while i > 0 and grid[i][x] < grid[y][x]:
            i -= 1
        score *= y - i

        i = y + 1
        while i < len(grid) - 1 and grid[i][x] < grid[y][x]:
            i += 1
        score *= i - y

        if score > max_score:
            max_score = score

print(max_score)
