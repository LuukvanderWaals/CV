valves = {}
total = 0
for i in open("input.txt", "r").readlines():
    i = i.split(" ")
    valves[i[1]] = (int(i[4][5:-1]), [])
    for j in i[9:]:
        valves[i[1]][1].append(j[:-1])

paths = [("AA", "AA", set(), 0, {"AA"}, 30)]


def heuristic(opened, minutes):
    closed = sorted(valves[i][0] for i in set(valves.keys()) - opened)
    h = sum(valves[i][0] for i in opened) * minutes
    minutes -= 1
    while minutes > 0 and closed:
        h += (closed.pop() + closed.pop()) * minutes
        minutes -= 2
    return h


min_minutes = 30
while True:
    you, elephant, opened, pressure, been, minutes = max(paths, key = lambda x: x[2] + heuristic(x[1], x[4]))
    paths.remove((you, elephant, opened, pressure, been, minutes))
    pressure += sum(valves[i][0] for i in opened)
    minutes -= 1
    if minutes == 0:
        print(pressure)
        break
    if minutes < min_minutes:
        print(minutes)
        min_minutes = minutes
    for i in valves[valve][1]:
        if i not in been:
            paths.append((i, opened, pressure, been.union({valve}), minutes))
    if valves[valve][0] != 0 and valve not in opened:
        paths.append((valve, opened.union({valve}), pressure, {valve}, minutes))
        # paths.append((valve, opened.union({valve}), pressure + sum(valves[i][0] for i in opened) * minutes, {valve}, 0))
