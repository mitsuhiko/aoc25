def solve_part1(input_text):
    lines = input_text.strip().split("\n")

    position = 50  # dial starts at 50
    count_zeros = 0

    for line in lines:
        direction = line[0]  # 'L' or 'R'
        distance = int(line[1:])

        if direction == "L":
            position = (position - distance) % 100
        else:  # R
            position = (position + distance) % 100

        if position == 0:
            count_zeros += 1

    return count_zeros


def solve_part2(input_text):
    lines = input_text.strip().split("\n")

    position = 50  # dial starts at 50
    count_zeros = 0

    for line in lines:
        direction = line[0]  # 'L' or 'R'
        distance = int(line[1:])

        # Count zeros during this rotation (including landing on 0)
        if direction == "L":
            # Going left: first zero hit at step = position (if position > 0)
            # Then every 100 steps after
            if position > 0:
                if position <= distance:
                    count_zeros += (distance - position) // 100 + 1
            else:  # position == 0
                count_zeros += distance // 100
            position = (position - distance) % 100
        else:  # R
            # Going right: first zero hit at step = 100 - position (if position > 0)
            # Then every 100 steps after
            if position > 0:
                first_zero = 100 - position
                if first_zero <= distance:
                    count_zeros += (distance - first_zero) // 100 + 1
            else:  # position == 0
                count_zeros += distance // 100
            position = (position + distance) % 100

    return count_zeros


if __name__ == "__main__":
    with open("day01.txt") as f:
        input_text = f.read()

    print(f"Part 1: {solve_part1(input_text)}")
    print(f"Part 2: {solve_part2(input_text)}")
