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
    with open("inputs/day02.txt") as f:
        input_text = f.read()

    print(f"Part 1: {solve_part1(input_text)}")
    print(f"Part 2: {solve_part2(input_text)}")
