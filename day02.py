def is_invalid_id(num):
    """
    Check if a number is an invalid ID.
    Invalid IDs are made of some sequence of digits repeated twice.
    E.g., 11 (1+1), 6464 (64+64), 123123 (123+123)
    """
    s = str(num)
    # Must have even length to be split in half
    if len(s) % 2 != 0:
        return False

    # Split in half and check if both halves are equal
    mid = len(s) // 2
    first_half = s[:mid]
    second_half = s[mid:]

    # Check if they match and no leading zeros (except for "0" itself)
    if first_half == second_half and (first_half[0] != '0' or first_half == '0'):
        return True
    return False


def solve_part1(input_text):
    """Find and sum all invalid IDs in the given ranges."""
    ranges = input_text.strip().split(',')
    total = 0

    for range_str in ranges:
        start, end = map(int, range_str.split('-'))
        for num in range(start, end + 1):
            if is_invalid_id(num):
                total += num

    return total


def is_invalid_id_part2(num):
    """
    Check if a number is an invalid ID for Part 2.
    Invalid IDs are made of some sequence of digits repeated at least twice.
    E.g., 11 (1 twice), 111 (1 three times), 565656 (56 three times), 824824824 (824 three times)
    """
    s = str(num)
    length = len(s)

    # Try all possible pattern lengths from 1 to length//2
    # (we need at least 2 repetitions)
    for pattern_len in range(1, length // 2 + 1):
        # Check if the length is divisible by pattern length
        if length % pattern_len == 0:
            pattern = s[:pattern_len]
            # Check if no leading zeros (except for "0" itself)
            if pattern[0] == '0' and pattern != '0':
                continue
            # Check if the entire string is this pattern repeated
            num_repetitions = length // pattern_len
            if pattern * num_repetitions == s:
                return True

    return False


def solve_part2(input_text):
    """Find and sum all invalid IDs using Part 2 rules (at least 2 repetitions)."""
    ranges = input_text.strip().split(',')
    total = 0

    for range_str in ranges:
        start, end = map(int, range_str.split('-'))
        for num in range(start, end + 1):
            if is_invalid_id_part2(num):
                total += num

    return total


if __name__ == "__main__":
    with open("day02.txt") as f:
        input_text = f.read()

    print(f"Part 1: {solve_part1(input_text)}")
    print(f"Part 2: {solve_part2(input_text)}")
