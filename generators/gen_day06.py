#!/usr/bin/env python3
"""Generator for Day 06 puzzle inputs.

Day 06: Arithmetic worksheet puzzle
- Input is a character grid where each vertical "problem" consists of:
  - 4 numbers written top-to-bottom (one character per row)
  - 1 operator in the last row
- Problems are separated by columns of all spaces
- Both Part 1 and Part 2 work by transposing and grouping columns
"""

import random
import argparse


def generate_input(num_problems=200, seed=None):
    """Generate a valid Day 06 input.

    Args:
        num_problems: Number of arithmetic problems (vertical columns)
        seed: Random seed for reproducibility

    Returns:
        String containing the generated input
    """
    if seed is not None:
        random.seed(seed)

    # We have 5 rows total: 4 number rows + 1 operator row
    num_rows = 5

    # Build the grid column by column
    # Each problem is a group of character columns
    char_columns = []

    for prob_idx in range(num_problems):
        # Generate 4 numbers for this problem
        numbers = []
        for row_idx in range(4):
            # Favor smaller numbers but include some larger ones
            if random.random() < 0.7:
                num = random.randint(1, 99)
            else:
                num = random.randint(100, 9999)
            numbers.append(num)

        # For the FIRST problem ONLY: ensure the first number is the longest
        # This prevents leading spaces on the first line (which would be stripped)
        if prob_idx == 0:
            max_len = max(len(str(n)) for n in numbers)
            if len(str(numbers[0])) < max_len:
                # Make first number the longest by regenerating it
                if max_len == 1:
                    numbers[0] = random.randint(1, 9)
                elif max_len == 2:
                    numbers[0] = random.randint(10, 99)
                elif max_len == 3:
                    numbers[0] = random.randint(100, 999)
                else:  # max_len >= 4
                    numbers[0] = random.randint(1000, 9999)

        operator = random.choice(["+", "*"])

        # Find the width needed for this problem (max digits among the 4 numbers)
        max_width = max(len(str(num)) for num in numbers)

        # Create character columns for this problem
        # Each number gets right-aligned within max_width columns
        for col_offset in range(max_width):
            column = []
            for row_idx in range(4):
                num_str = str(numbers[row_idx]).rjust(max_width)
                column.append(num_str[col_offset])
            # Add operator character (left-aligned in the problem width)
            op_str = operator.ljust(max_width)
            column.append(op_str[col_offset])

            char_columns.append(column)

        # Add separator column (all spaces) between problems
        char_columns.append([" "] * num_rows)

    # Remove the trailing separator column
    if char_columns and all(c == " " for c in char_columns[-1]):
        char_columns.pop()

    # Transpose columns to rows
    rows = []
    for row_idx in range(num_rows):
        row_chars = [col[row_idx] for col in char_columns]
        rows.append("".join(row_chars))

    # Do NOT pad rows to the same length - just join them
    return "\n".join(rows)


def main():
    parser = argparse.ArgumentParser(description="Generate Day 06 puzzle input")
    parser.add_argument(
        "-n",
        "--num-problems",
        type=int,
        default=200,
        help="Number of arithmetic problems (default: 200)",
    )
    parser.add_argument(
        "-s", "--seed", type=int, default=None, help="Random seed for reproducibility"
    )
    parser.add_argument(
        "-o", "--output", type=str, default=None, help="Output file (default: stdout)"
    )

    args = parser.parse_args()

    result = generate_input(num_problems=args.num_problems, seed=args.seed)

    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
        print(f"Generated input written to {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
