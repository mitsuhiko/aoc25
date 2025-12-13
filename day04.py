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
