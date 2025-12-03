def solve_part1(input_text):
    total = 0
    for line in input_text.strip().split('\n'):
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
    for line in input_text.strip().split('\n'):
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

        joltage = int(''.join(result))
        total += joltage
    return total

if __name__ == "__main__":
    with open("day03.txt") as f:
        input_text = f.read()

    print(f"Part 1: {solve_part1(input_text)}")
    print(f"Part 2: {solve_part2(input_text)}")
