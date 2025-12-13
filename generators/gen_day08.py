#!/usr/bin/env python3
"""Generator for Day 08 puzzle inputs.

Day 08: 3D Point Clustering
- Input consists of lines with three comma-separated integers (x,y,z coordinates)
- Points represent locations in 3D space
- Part 1: Find product of sizes of 3 largest clusters using 1000 closest edges
- Part 2: Find product of X coordinates of last two points connected for full connectivity
"""

import random
import argparse


def generate_input(num_points=1000, seed=None, coord_range=100000):
    """Generate a valid Day 08 input.

    Args:
        num_points: Number of 3D points to generate
        seed: Random seed for reproducibility
        coord_range: Maximum value for coordinates (0 to coord_range)

    Returns:
        String containing the generated input
    """
    if seed is not None:
        random.seed(seed)

    lines = []
    for _ in range(num_points):
        x = random.randint(0, coord_range)
        y = random.randint(0, coord_range)
        z = random.randint(0, coord_range)
        lines.append(f"{x},{y},{z}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate Day 08 puzzle input")
    parser.add_argument(
        "-n",
        "--num-points",
        type=int,
        default=1000,
        help="Number of 3D points to generate (default: 1000)",
    )
    parser.add_argument(
        "-s", "--seed", type=int, default=None, help="Random seed for reproducibility"
    )
    parser.add_argument(
        "-o", "--output", type=str, default=None, help="Output file (default: stdout)"
    )
    parser.add_argument(
        "--coord-range",
        type=int,
        default=100000,
        help="Maximum coordinate value (default: 100000)",
    )

    args = parser.parse_args()

    result = generate_input(
        num_points=args.num_points, seed=args.seed, coord_range=args.coord_range
    )

    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
            f.write("\n")
        print(f"Generated {args.num_points} points and wrote to {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
