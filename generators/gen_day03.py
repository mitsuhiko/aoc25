#!/usr/bin/env python3
"""Generator for Day 03 puzzle inputs.

Day 03: Joltage puzzle
- Input consists of lines containing digits (0-9)
- Part 1: Find maximum two-digit number by selecting any two digits in order
- Part 2: Select 12 digits to maximize the 12-digit number (greedy approach)
- Each line must have at least 12 digits for Part 2 to work
"""

import random
import argparse


def generate_input(num_lines=200, line_length=100, seed=None):
    """Generate a valid Day 03 input.

    Args:
        num_lines: Number of lines to generate
        line_length: Length of each line (number of digits)
        seed: Random seed for reproducibility

    Returns:
        String containing the generated input
    """
    if seed is not None:
        random.seed(seed)

    if line_length < 12:
        raise ValueError("line_length must be at least 12 for Part 2 to work")

    lines = []
    for _ in range(num_lines):
        # Generate a line of random digits
        digits = [str(random.randint(0, 9)) for _ in range(line_length)]
        lines.append("".join(digits))

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate Day 03 puzzle input")
    parser.add_argument(
        "-n",
        "--num-lines",
        type=int,
        default=200,
        help="Number of lines to generate (default: 200)",
    )
    parser.add_argument(
        "--line-length",
        type=int,
        default=100,
        help="Length of each line in digits (default: 100, min: 12)",
    )
    parser.add_argument(
        "-s", "--seed", type=int, default=None, help="Random seed for reproducibility"
    )
    parser.add_argument(
        "-o", "--output", type=str, default=None, help="Output file (default: stdout)"
    )

    args = parser.parse_args()

    result = generate_input(
        num_lines=args.num_lines, line_length=args.line_length, seed=args.seed
    )

    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
            f.write("\n")
        print(f"Generated input written to {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
