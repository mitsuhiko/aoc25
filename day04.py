"""
Day 4: Accessibility Analysis on a Grid

This puzzle involves analyzing a 2D grid containing objects (marked with '@') and
determining which objects are accessible based on their local neighborhood density.
An object is accessible if it has fewer than 4 adjacent objects in the 8 surrounding
positions (including diagonals). Part 1 requires counting how many objects are
initially accessible in the given grid configuration.

Part 2 extends this to a cascading removal simulation. After identifying and removing
all accessible objects, the grid state changes, potentially making previously
inaccessible objects now accessible. This process repeats iteratively until no more
objects can be removed. The challenge is to compute the total number of objects that
can be removed through this iterative process. This is similar to cellular automaton
concepts where the state of cells depends on their neighbors and evolves over discrete
time steps.
"""


def solve_part1(input_text):
    grid = input_text.strip().split("\n")
    rows = len(grid)
    cols = len(grid[0])

    # 8 directions for adjacent cells
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "@":
                # Count adjacent rolls
                adjacent_rolls = 0
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "@":
                        adjacent_rolls += 1
                # Forklift can access if fewer than 4 adjacent rolls
                if adjacent_rolls < 4:
                    count += 1

    return count


def solve_part2(input_text):
    grid = [list(line) for line in input_text.strip().split("\n")]
    rows = len(grid)
    cols = len(grid[0])

    # 8 directions for adjacent cells
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    total_removed = 0

    while True:
        # Find all rolls that can be accessed
        to_remove = []
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "@":
                    # Count adjacent rolls
                    adjacent_rolls = 0
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "@":
                            adjacent_rolls += 1
                    # Forklift can access if fewer than 4 adjacent rolls
                    if adjacent_rolls < 4:
                        to_remove.append((r, c))

        if not to_remove:
            break

        # Remove all accessible rolls
        for r, c in to_remove:
            grid[r][c] = "."
        total_removed += len(to_remove)

    return total_removed


if __name__ == "__main__":
    import sys

    input_file = sys.argv[1] if len(sys.argv) > 1 else "inputs/day04.txt"
    with open(input_file) as f:
        input_text = f.read()

    print(f"Part 1: {solve_part1(input_text)}")
    print(f"Part 2: {solve_part2(input_text)}")
