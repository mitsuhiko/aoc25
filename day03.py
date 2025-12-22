"""Day 3: Maximum Subsequence Selection

This puzzle involves selecting digits from sequences to maximize numeric values.
Each line of input represents a sequence of single-digit numbers (1-9).

Part 1 requires selecting exactly 2 digits from each sequence (maintaining their
relative order) to form the largest possible 2-digit number. The solution uses
a brute-force approach, checking all pairs of positions (i, j) where i < j,
computing the resulting 2-digit number, and finding the maximum.

Part 2 extends this to selecting exactly 12 digits from each sequence to form
the largest possible 12-digit number. This is solved using a greedy algorithm:
at each position in the result, select the largest available digit from the
remaining valid range, ensuring enough digits remain to complete the selection.
The algorithm maintains a sliding window constraint - for each of the 12 positions
being filled, it identifies the rightmost position from which a digit can be
selected while still leaving enough digits for the remaining positions.
"""


def solve_part1(input_text):
    total = 0
    for line in input_text.strip().split("\n"):
        # Find maximum two-digit number by selecting any two digits in order
        max_joltage = 0
        for i in range(len(line)):
            for j in range(i + 1, len(line)):
                joltage = int(line[i]) * 10 + int(line[j])
                max_joltage = max(max_joltage, joltage)
        total += max_joltage
    return total


def solve_part2(input_text):
    total = 0
    for line in input_text.strip().split("\n"):
        # Select 12 digits to maximize the 12-digit number
        # Greedy: at each position, pick the largest digit available
        n = len(line)
        result = []
        start = 0
        remaining = 12

        while remaining > 0:
            # Can pick from start to (n - remaining) inclusive
            end = n - remaining
            # Find max digit in range [start, end]
            best_idx = start
            for i in range(start, end + 1):
                if line[i] > line[best_idx]:
                    best_idx = i
            result.append(line[best_idx])
            start = best_idx + 1
            remaining -= 1

        joltage = int("".join(result))
        total += joltage
    return total


if __name__ == "__main__":
    import sys

    input_file = sys.argv[1] if len(sys.argv) > 1 else "inputs/day03.txt"
    with open(input_file) as f:
        input_text = f.read()

    print(f"Part 1: {solve_part1(input_text)}")
    print(f"Part 2: {solve_part2(input_text)}")
