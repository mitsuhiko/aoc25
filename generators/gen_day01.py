#!/usr/bin/env python3
"""Generator for Day 01 puzzle inputs.

Day 01: Dial puzzle
- Input consists of lines with 'L' or 'R' followed by a positive integer
- The dial starts at position 50 on a 0-99 scale
- L moves counter-clockwise (subtracts), R moves clockwise (adds)
- Position wraps around modulo 100
"""

import random
import argparse


def generate_input(num_lines=4000, seed=None):
    """Generate a valid Day 01 input.

    Args:
        num_lines: Number of instruction lines to generate
        seed: Random seed for reproducibility

    Returns:
        String containing the generated input
    """
    if seed is not None:
        random.seed(seed)

    lines = []
    for _ in range(num_lines):
        direction = random.choice(["L", "R"])
        # Mix of small and large numbers, similar to real input
        if random.random() < 0.7:
            # Small numbers (1-99)
            distance = random.randint(1, 99)
        else:
            # Larger numbers (100-1000)
            distance = random.randint(100, 1000)
        lines.append(f"{direction}{distance}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate Day 01 puzzle input")
    parser.add_argument(
        "-n",
        "--num-lines",
        type=int,
        default=4000,
        help="Number of instruction lines (default: 4000)",
    )
    parser.add_argument(
        "-s", "--seed", type=int, default=None, help="Random seed for reproducibility"
    )
    parser.add_argument(
        "-o", "--output", type=str, default=None, help="Output file (default: stdout)"
    )

    args = parser.parse_args()

    result = generate_input(num_lines=args.num_lines, seed=args.seed)

    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
        print(f"Generated input written to {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
