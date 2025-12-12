def solve_part1(input_text):
    lines = input_text.strip().split("\n")
    grid = [list(line) for line in lines]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Find starting position S
    start_col = None
    start_row = 0
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == "S":
                start_col = col
                start_row = row
                break
        if start_col is not None:
            break

    # Track beams as set of columns (beams always go down)
    beams = {start_col}
    split_count = 0

    for row in range(start_row + 1, rows):
        new_beams = set()
        for col in beams:
            if col < 0 or col >= cols:
                continue  # Beam exited the manifold

            if grid[row][col] == "^":
                # Beam hits splitter - count this split
                split_count += 1
                new_beams.add(col - 1)  # Left beam
                new_beams.add(col + 1)  # Right beam
            else:
                # Empty space - beam continues down
                new_beams.add(col)

        beams = new_beams

    return split_count


def solve_part2(input_text):
    lines = input_text.strip().split("\n")
    grid = [list(line) for line in lines]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Find starting position S
    start_col = None
    start_row = 0
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == "S":
                start_col = col
                start_row = row
                break
        if start_col is not None:
            break

    # Track timelines as dict of column -> count
    # Each timeline that hits a splitter branches into 2
    from collections import defaultdict

    timelines = defaultdict(int)
    timelines[start_col] = 1

    for row in range(start_row + 1, rows):
        new_timelines = defaultdict(int)
        for col, count in timelines.items():
            if col < 0 or col >= cols:
                continue  # Timeline exited the manifold

            if grid[row][col] == "^":
                # Splitter - each timeline splits into 2
                new_timelines[col - 1] += count
                new_timelines[col + 1] += count
            else:
                # Empty space - timeline continues
                new_timelines[col] += count

        timelines = new_timelines

    return sum(timelines.values())


if __name__ == "__main__":
    with open("day07.txt") as f:
        input_text = f.read()

    print(f"Part 1: {solve_part1(input_text)}")
    print(f"Part 2: {solve_part2(input_text)}")
