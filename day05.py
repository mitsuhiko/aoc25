"""Day 5: Range Membership and Coverage Problem

This puzzle involves working with inclusive numeric ranges and testing membership. The input
consists of two sections: a list of ranges (e.g., "3-5" represents IDs 3, 4, and 5) and a
list of individual IDs to test. Ranges can overlap, and an ID is considered valid if it
falls within any of the given ranges.

Part 1 asks how many IDs from the provided list fall within at least one range. This requires
efficient range lookup, implemented using range merging to consolidate overlapping ranges
followed by binary search for O(log n) membership testing.

Part 2 asks for the total count of all unique IDs covered by the ranges themselves, ignoring
the individual ID list. This is solved by merging overlapping ranges and summing the size of
each merged range.
"""


def parse_input(input_text):
    """Parse the input into ranges and ingredient IDs."""
    parts = input_text.strip().split("\n\n")

    ranges = []
    for line in parts[0].strip().split("\n"):
        start, end = map(int, line.split("-"))
        ranges.append((start, end))

    ids = [int(line) for line in parts[1].strip().split("\n")]

    return ranges, ids


def merge_ranges(ranges):
    """Merge overlapping ranges for efficient lookup."""
    if not ranges:
        return []

    sorted_ranges = sorted(ranges)
    merged = [sorted_ranges[0]]

    for start, end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end + 1:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))

    return merged


def is_fresh(merged_ranges, id_val):
    """Check if an ID falls within any merged range using binary search."""
    lo, hi = 0, len(merged_ranges) - 1

    while lo <= hi:
        mid = (lo + hi) // 2
        start, end = merged_ranges[mid]

        if start <= id_val <= end:
            return True
        elif id_val < start:
            hi = mid - 1
        else:
            lo = mid + 1

    return False


def solve_part1(input_text):
    ranges, ids = parse_input(input_text)
    merged = merge_ranges(ranges)

    count = sum(1 for id_val in ids if is_fresh(merged, id_val))
    return count


def solve_part2(input_text):
    ranges, _ = parse_input(input_text)
    merged = merge_ranges(ranges)

    # Count total unique IDs covered by merged ranges
    total = sum(end - start + 1 for start, end in merged)
    return total


if __name__ == "__main__":
    import sys

    input_file = sys.argv[1] if len(sys.argv) > 1 else "inputs/day05.txt"

    with open(input_file) as f:
        input_text = f.read()

    print(f"Part 1: {solve_part1(input_text)}")
    print(f"Part 2: {solve_part2(input_text)}")
