"""Day 1: Circular Dial Rotation Simulation

This puzzle involves simulating rotations on a circular dial numbered 0-99. The dial
starts at position 50 and responds to a sequence of rotation instructions. Each
instruction specifies a direction (L for left/decreasing or R for right/increasing)
and a distance to rotate. Rotations wrap around modulo 100, so moving left from 0
reaches 99, and moving right from 99 reaches 0.

Part 1 counts how many times the dial lands on position 0 after completing each
rotation instruction. Part 2 extends this by counting all instances where the dial
passes through position 0 during a rotation, not just the final position. This
requires calculating how many complete cycles of 100 the dial makes during each
rotation, accounting for the starting position and direction of movement.
"""


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
    import sys

    input_file = sys.argv[1] if len(sys.argv) > 1 else "inputs/day01.txt"
    with open(input_file) as f:
        input_text = f.read()

    print(f"Part 1: {solve_part1(input_text)}")
    print(f"Part 2: {solve_part2(input_text)}")
