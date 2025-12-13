#!/usr/bin/env python3
"""Generator for Day 07 puzzle inputs.

Day 07: Beam Splitter puzzle
- Input is a grid where beams travel downward from a starting position 'S'
- '.' represents empty space (beam continues down)
- '^' represents a splitter (beam splits left and right)
- Part 1: Count how many splits occur
- Part 2: Count total number of timelines (each split doubles timelines)

The splitter pattern forms a Christmas tree shape using Rule 90 cellular
automaton (Sierpinski triangle pattern).
"""

import random
import argparse


def generate_input(rows=143, cols=141, row_spacing=2, seed=None, noise=0.0):
    """Generate a valid Day 07 input with Christmas tree pattern.

    Args:
        rows: Number of rows in the grid (default: 143)
        cols: Number of columns in the grid (should be odd for symmetry, default: 141)
        row_spacing: Empty rows between splitter rows (default: 2)
        seed: Random seed for reproducibility
        noise: Probability of flipping a splitter (0.0 = perfect tree, default: 0.0)

    Returns:
        String containing the generated input
    """
    if seed is not None:
        random.seed(seed)

    # Ensure odd number of columns for proper centering
    if cols % 2 == 0:
        cols += 1

    # Create grid filled with dots
    grid = [["." for _ in range(cols)] for _ in range(rows)]

    # Place 'S' at the top row, centered
    center = cols // 2
    grid[0][center] = "S"

    # Use Rule 90 cellular automaton to generate Sierpinski triangle pattern
    # Rule 90: new[i] = old[i-1] XOR old[i+1]
    # This creates the classic Christmas tree / Sierpinski triangle shape

    # Initialize CA state - single cell on at center
    state = [0] * cols
    state[center] = 1

    splitter_row = 2  # First splitter row
    while splitter_row < rows:
        # Place splitters based on current CA state
        for col in range(cols):
            if state[col] == 1:
                # Apply noise if configured
                if noise > 0 and random.random() < noise:
                    continue  # Skip this splitter
                grid[splitter_row][col] = "^"

        # Compute next CA state using Rule 90 (XOR of neighbors)
        new_state = [0] * cols
        for i in range(cols):
            left = state[i - 1] if i > 0 else 0
            right = state[i + 1] if i < cols - 1 else 0
            new_state[i] = left ^ right
        state = new_state

        # Move to next splitter row
        splitter_row += row_spacing

    # Convert grid to string
    lines = ["".join(row) for row in grid]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Generate Day 07 puzzle input")
    parser.add_argument(
        "-n", "--rows", type=int, default=143, help="Number of rows (default: 143)"
    )
    parser.add_argument(
        "--cols",
        type=int,
        default=141,
        help="Number of columns, should be odd (default: 141)",
    )
    parser.add_argument(
        "--spacing",
        type=int,
        default=2,
        help="Empty rows between splitter rows (default: 2)",
    )
    parser.add_argument(
        "--noise",
        type=float,
        default=0.0,
        help="Probability of removing splitters for variation (default: 0.0)",
    )
    parser.add_argument(
        "-s", "--seed", type=int, default=None, help="Random seed for reproducibility"
    )
    parser.add_argument(
        "-o", "--output", type=str, default=None, help="Output file (default: stdout)"
    )

    args = parser.parse_args()

    result = generate_input(
        rows=args.rows,
        cols=args.cols,
        row_spacing=args.spacing,
        seed=args.seed,
        noise=args.noise,
    )

    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
        print(f"Generated input written to {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
