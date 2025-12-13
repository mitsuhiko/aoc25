#!/usr/bin/env python3
"""Generator for Day 05 puzzle inputs.

Day 05: Range and ID puzzle
- Input has two sections separated by a blank line
- First section: ranges in format "start-end" (where start <= end)
- Second section: individual ingredient IDs (integers)
- Part 1: Count how many IDs fall within the merged ranges
- Part 2: Count total unique IDs covered by merged ranges
"""

import random
import argparse


def generate_input(
    num_ranges=187, num_ids=1000, seed=None, max_value=600_000_000_000_000
):
    """Generate a valid Day 05 input.

    Args:
        num_ranges: Number of ranges to generate
        num_ids: Number of ingredient IDs to generate
        seed: Random seed for reproducibility
        max_value: Maximum value for range endpoints and IDs

    Returns:
        String containing the generated input
    """
    if seed is not None:
        random.seed(seed)

    # Generate ranges
    ranges = []
    for _ in range(num_ranges):
        # Generate start and end points
        start = random.randint(1, max_value)
        # End can be equal to start (single value range) or larger
        # Mix of single-value ranges and larger ranges
        if random.random() < 0.1:
            # 10% chance of single-value range
            end = start
        else:
            # Range of varying sizes
            range_size = random.randint(1, max_value // 100)
            end = min(start + range_size, max_value)

        ranges.append(f"{start}-{end}")

    # Generate IDs
    # Mix of IDs that fall within ranges and IDs that don't
    ids = []
    for _ in range(num_ids):
        ids.append(str(random.randint(1, max_value)))

    # Format output
    ranges_section = "\n".join(ranges)
    ids_section = "\n".join(ids)

    return f"{ranges_section}\n\n{ids_section}"


def main():
    parser = argparse.ArgumentParser(description="Generate Day 05 puzzle input")
    parser.add_argument(
        "-n",
        "--num-ranges",
        type=int,
        default=187,
        help="Number of ranges (default: 187)",
    )
    parser.add_argument(
        "--num-ids",
        type=int,
        default=1000,
        help="Number of ingredient IDs (default: 1000)",
    )
    parser.add_argument(
        "-s", "--seed", type=int, default=None, help="Random seed for reproducibility"
    )
    parser.add_argument(
        "-o", "--output", type=str, default=None, help="Output file (default: stdout)"
    )

    args = parser.parse_args()

    result = generate_input(
        num_ranges=args.num_ranges, num_ids=args.num_ids, seed=args.seed
    )

    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
        print(f"Generated input written to {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
