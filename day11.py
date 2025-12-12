from functools import cache


def parse_input(input_text):
    graph = {}
    for line in input_text.strip().split("\n"):
        if ":" not in line:
            continue
        src, dests = line.split(": ")
        graph[src] = dests.split()
    return graph


def solve_part1(input_text):
    graph = parse_input(input_text)

    @cache
    def count_paths(node):
        if node == "out":
            return 1
        if node not in graph:
            return 0
        return sum(count_paths(dest) for dest in graph[node])

    return count_paths("you")


def solve_part2(input_text):
    graph = parse_input(input_text)

    @cache
    def count_paths(node, visited_dac, visited_fft):
        if node == "dac":
            visited_dac = True
        if node == "fft":
            visited_fft = True

        if node == "out":
            return 1 if (visited_dac and visited_fft) else 0
        if node not in graph:
            return 0

        return sum(count_paths(dest, visited_dac, visited_fft) for dest in graph[node])

    return count_paths("svr", False, False)


if __name__ == "__main__":
    with open("inputs/day11.txt") as f:
        input_text = f.read()

    print(f"Part 1: {solve_part1(input_text)}")
    print(f"Part 2: {solve_part2(input_text)}")
