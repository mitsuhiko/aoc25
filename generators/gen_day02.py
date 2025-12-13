#!/usr/bin/env python3
"""Generator for Day 02 puzzle inputs.

Day 02: Invalid ID Detection puzzle
- Input consists of comma-separated ranges in the format "start1-end1,start2-end2,..."
- Part 1: Find IDs that are patterns repeated exactly twice (e.g., 123123)
- Part 2: Find IDs that are patterns repeated at least twice (e.g., 123123, 1212, etc.)
"""

import random
import argparse


def generate_input(num_ranges=30, seed=None):
    """Generate a valid Day 02 input.

    Args:
        num_ranges: Number of ranges to generate
        seed: Random seed for reproducibility

    Returns:
        String containing the generated input (comma-separated ranges)
    """
    if seed is not None:
        random.seed(seed)

    ranges = []
    for _ in range(num_ranges):
        # Generate different types of ranges to make the puzzle interesting
        range_type = random.random()

        if range_type < 0.3:
            # Small ranges (single to few digits)
            start = random.randint(1, 100)
            end = random.randint(start, start + random.randint(10, 100))
        elif range_type < 0.6:
            # Medium ranges (4-6 digits)
            start = random.randint(1000, 999999)
            end = random.randint(start, start + random.randint(1000, 100000))
        elif range_type < 0.85:
            # Large ranges (7-9 digits)
            start = random.randint(1000000, 999999999)
            end = random.randint(start, start + random.randint(10000, 500000))
        else:
            # Very large ranges (10+ digits)
            start = random.randint(1000000000, 9999999999)
            end = random.randint(start, start + random.randint(10000, 1000000))

        ranges.append(f"{start}-{end}")

    return ",".join(ranges)


def main():
    parser = argparse.ArgumentParser(description="Generate Day 02 puzzle input")
    parser.add_argument(
        "-n",
        "--num-ranges",
        type=int,
        default=30,
        help="Number of ranges to generate (default: 30)",
    )
    parser.add_argument(
        "-s", "--seed", type=int, default=None, help="Random seed for reproducibility"
    )
    parser.add_argument(
        "-o", "--output", type=str, default=None, help="Output file (default: stdout)"
    )

    args = parser.parse_args()

    result = generate_input(num_ranges=args.num_ranges, seed=args.seed)

    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
        print(f"Generated input written to {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
