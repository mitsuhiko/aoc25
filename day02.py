"""
Advent of Code 2025 Day 2: Pattern Repetition Detection

This puzzle involves identifying numbers that consist of a repeating digit pattern.
Given a series of numeric ranges, the task is to find all numbers within those ranges
that can be formed by repeating a sequence of digits multiple times.

Part 1 focuses on numbers with exactly 2 repetitions: a number is invalid if it can
be expressed as a pattern repeated exactly twice (e.g., 11, 6464, 123123). The
algorithm generates candidates by iterating through possible pattern lengths, creating
all valid patterns (excluding those with leading zeros), and checking if the resulting
repeated number falls within each range.

Part 2 extends the criteria to numbers with 2 or more repetitions: any number that
can be formed by repeating a pattern at least twice is invalid (e.g., 111, 12341234,
1212121212). This requires checking multiple divisors of the number's digit length
to find all possible pattern lengths that evenly divide the total length. The solution
sums all unique invalid numbers found across all ranges.
"""


def generate_invalid_ids_part1_in_range(start, end):
    """Generate all Part 1 invalid IDs (exactly 2 repetitions) in range."""
    start_digits = len(str(start))
    end_digits = len(str(end))
    invalid_ids = set()

    for num_digits in range(start_digits, end_digits + 1):
        if num_digits % 2 == 0:  # Must be even for 2 repetitions
            pattern_len = num_digits // 2

            # Generate all patterns of this length
            pattern_min = 10 ** (pattern_len - 1)  # No leading zeros
            pattern_max = 10**pattern_len - 1

            for pattern in range(pattern_min, pattern_max + 1):
                invalid_num = int(str(pattern) * 2)
                if start <= invalid_num <= end:
                    invalid_ids.add(invalid_num)

    return invalid_ids


def solve_part1(input_text):
    """Find and sum all invalid IDs in the given ranges."""
    ranges = input_text.strip().split(",")
    total = 0

    for range_str in ranges:
        start, end = map(int, range_str.split("-"))
        invalid_ids = generate_invalid_ids_part1_in_range(start, end)
        total += sum(invalid_ids)

    return total


def generate_invalid_ids_in_range(start, end):
    """Generate all invalid IDs (2+ repetitions) in range."""
    start_digits = len(str(start))
    end_digits = len(str(end))
    invalid_ids = set()

    for num_digits in range(start_digits, end_digits + 1):
        for pattern_len in range(1, num_digits // 2 + 1):
            if num_digits % pattern_len == 0:
                repetitions = num_digits // pattern_len

                # Generate all patterns of this length
                pattern_min = 10 ** (pattern_len - 1) if pattern_len > 1 else 1
                pattern_max = 10**pattern_len - 1

                for pattern in range(pattern_min, pattern_max + 1):
                    pattern_str = str(pattern)
                    if len(pattern_str) != pattern_len:
                        continue

                    invalid_num = int(pattern_str * repetitions)
                    if start <= invalid_num <= end:
                        invalid_ids.add(invalid_num)

    return invalid_ids


def solve_part2(input_text):
    """Find and sum all invalid IDs using Part 2 rules (at least 2 repetitions)."""
    ranges = input_text.strip().split(",")
    total = 0

    for range_str in ranges:
        start, end = map(int, range_str.split("-"))
        invalid_ids = generate_invalid_ids_in_range(start, end)
        total += sum(invalid_ids)

    return total


if __name__ == "__main__":
    import sys

    input_file = sys.argv[1] if len(sys.argv) > 1 else "inputs/day02.txt"
    with open(input_file) as f:
        input_text = f.read()

    print(f"Part 1: {solve_part1(input_text)}")
    print(f"Part 2: {solve_part2(input_text)}")
