def parse_problems(input_text):
    """Parse the worksheet into a list of (numbers, operator) tuples."""
    lines = input_text.rstrip('\n').split('\n')

    # Pad all lines to the same length
    max_len = max(len(line) for line in lines)
    lines = [line.ljust(max_len) for line in lines]

    # Transpose to get columns
    cols = list(zip(*lines))

    # Find separator columns (all spaces)
    problems = []
    current_cols = []

    for col in cols:
        if all(c == ' ' for c in col):
            if current_cols:
                problems.append(current_cols)
                current_cols = []
        else:
            current_cols.append(col)

    if current_cols:
        problems.append(current_cols)

    # Parse each problem
    result = []
    for prob_cols in problems:
        # Transpose back to rows
        rows = [''.join(row) for row in zip(*prob_cols)]

        # Last row is operator, rest are numbers
        operator = rows[-1].strip()
        numbers = []
        for row in rows[:-1]:
            num_str = row.strip()
            if num_str:
                numbers.append(int(num_str))

        result.append((numbers, operator))

    return result


def solve_part1(input_text):
    problems = parse_problems(input_text)

    total = 0
    for numbers, op in problems:
        if op == '+':
            result = sum(numbers)
        else:  # op == '*'
            result = 1
            for n in numbers:
                result *= n
        total += result

    return total


def parse_problems_part2(input_text):
    """Parse worksheet for Part 2: numbers are read column-wise (vertically)."""
    lines = input_text.rstrip('\n').split('\n')

    # Pad all lines to the same length
    max_len = max(len(line) for line in lines)
    lines = [line.ljust(max_len) for line in lines]

    # Transpose to get columns
    cols = list(zip(*lines))

    # Find separator columns (all spaces) to identify problem regions
    problems = []
    current_cols = []

    for col in cols:
        if all(c == ' ' for c in col):
            if current_cols:
                problems.append(current_cols)
                current_cols = []
        else:
            current_cols.append(col)

    if current_cols:
        problems.append(current_cols)

    # Parse each problem - read columns as numbers (top-to-bottom = MSD to LSD)
    result = []
    for prob_cols in problems:
        # Find operator from the operator row (last char of each column)
        operator = None
        for col in prob_cols:
            if col[-1] in '+*':
                operator = col[-1]
                break

        # Each column (excluding operator row) forms a number
        numbers = []
        for col in prob_cols:
            # Take all rows except the last (operator row)
            digits = ''.join(col[:-1]).replace(' ', '')
            if digits:
                numbers.append(int(digits))

        result.append((numbers, operator))

    return result


def solve_part2(input_text):
    problems = parse_problems_part2(input_text)

    total = 0
    for numbers, op in problems:
        if op == '+':
            result = sum(numbers)
        else:  # op == '*'
            result = 1
            for n in numbers:
                result *= n
        total += result

    return total


if __name__ == "__main__":
    with open("day06.txt") as f:
        input_text = f.read()

    print(f"Part 1: {solve_part1(input_text)}")
    print(f"Part 2: {solve_part2(input_text)}")
