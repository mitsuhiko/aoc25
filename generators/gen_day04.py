#!/usr/bin/env python3
"""Generator for Day 04 puzzle inputs.

Day 04: Paper Roll puzzle
- Input consists of a grid with '@' symbols representing paper rolls
- The grid contains rolls that may be accessible or blocked by adjacent rolls
- A roll is accessible if it has fewer than 4 adjacent rolls (8-directional)
"""

import random
import argparse


def generate_input(grid_size=140, seed=None):
    """Generate a valid Day 04 input.

    Args:
        grid_size: Size of the square grid (default: 140 for ~140x140 grid)
        seed: Random seed for reproducibility

    Returns:
        String containing the generated input
    """
    if seed is not None:
        random.seed(seed)

    # Create a grid with a reasonable density of @ symbols
    # Real input has ~65% density
    density = 0.65

    grid = []
    for _ in range(grid_size):
        row = []
        for _ in range(grid_size):
            if random.random() < density:
                row.append("@")
            else:
                row.append(".")
        grid.append("".join(row))

    return "\n".join(grid)


def main():
    parser = argparse.ArgumentParser(description="Generate Day 04 puzzle input")
    parser.add_argument(
        "-n", "--size", type=int, default=140, help="Grid size (default: 140)"
    )
    parser.add_argument(
        "-s", "--seed", type=int, default=None, help="Random seed for reproducibility"
    )
    parser.add_argument(
        "-o", "--output", type=str, default=None, help="Output file (default: stdout)"
    )

    args = parser.parse_args()

    result = generate_input(grid_size=args.size, seed=args.seed)

    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
        print(f"Generated input written to {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
