def check_row(row):
    min_height = -1
    for i, height in enumerate(row):
        if height > min_height:
            yield i
            if height == 9:
                return
            min_height = height

def check_grid(grid):
    pos = []
    for i, row in enumerate(grid):
        x = list(check_row(row))
        pos += zip(x, [i] * len(x))
    return pos


grid = list(map(lambda x: list(map(int, x)), open("input.txt", "r").read().split("\n")))

visible = set()
visible = visible.union(set(check_grid(grid))) \
                 .union(set(map(lambda x: (len(grid[x[1]]) - 1 - x[0], x[1]), check_grid(map(lambda x: x[::-1], grid))))) \
                 .union(set(map(lambda x: (x[1], x[0]), check_grid(zip(*grid))))) \
                 .union(set(map(lambda x: (x[1], len(grid[x[1]]) - 1 - x[0]), check_grid(map(lambda x: x[::-1], zip(*grid))))))

print(len(visible))
