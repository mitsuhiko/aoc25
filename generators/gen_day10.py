#!/usr/bin/env python3
"""Generator for Day 10 puzzle inputs.

Day 10: Button/Light puzzle
- Each line represents a machine with:
  - A target pattern [.##.#] where . is off and # is on
  - Button configurations (2,3,4,6) with indices of lights each button toggles
  - Optional joltage requirements {41,56,34} for part 2
"""

import random
import argparse


def generate_machine(num_lights, num_buttons, num_counters, seed_offset=0, rng=None):
    """Generate a single machine configuration.

    Args:
        num_lights: Number of lights in the pattern
        num_buttons: Number of buttons available
        num_counters: Number of joltage counters (0 for part 1 only)
        seed_offset: Offset for randomization
        rng: Random number generator to use

    Returns:
        String representing one machine line
    """
    if rng is None:
        rng = random.Random()

    # Generate buttons first - each button toggles 1-8 lights
    buttons = []
    button_masks = []
    for _ in range(num_buttons):
        num_toggles = rng.randint(1, min(8, num_lights))
        indices = sorted(rng.sample(range(num_lights), num_toggles))

        # Calculate button mask
        mask = 0
        for idx in indices:
            mask |= 1 << idx
        button_masks.append(mask)

        if len(indices) == 1:
            buttons.append(f"({indices[0]})")
        else:
            buttons.append(f"({','.join(map(str, indices))})")

    # Generate a solvable target by simulating random button presses
    # This ensures the target is reachable
    target_mask = 0
    num_presses = rng.randint(1, min(5, num_buttons))  # Use 1-5 random button presses
    for _ in range(num_presses):
        button_idx = rng.randint(0, num_buttons - 1)
        target_mask ^= button_masks[button_idx]

    # Convert mask to target string
    target = []
    for i in range(num_lights):
        target.append("#" if (target_mask & (1 << i)) else ".")
    target_str = "[" + "".join(target) + "]"

    # Generate joltage requirements if needed
    joltage_str = ""
    if num_counters > 0:
        # Generate solvable joltage values by simulating actual button presses
        # Pick random press counts for each button, then compute resulting joltages
        button_presses = [rng.randint(0, 15) for _ in range(num_buttons)]

        # Compute joltage for each counter: sum of presses for buttons that affect it
        joltages = []
        for counter_idx in range(num_counters):
            total = 0
            for btn_idx, presses in enumerate(button_presses):
                # Check if button affects this counter
                if button_masks[btn_idx] & (1 << counter_idx):
                    total += presses
            joltages.append(str(total))
        joltage_str = " {" + ",".join(joltages) + "}"

    return target_str + " " + " ".join(buttons) + joltage_str


def generate_input(num_machines=166, seed=None):
    """Generate a valid Day 10 input.

    Args:
        num_machines: Number of machines to generate
        seed: Random seed for reproducibility

    Returns:
        String containing the generated input
    """
    if seed is not None:
        random.seed(seed)

    rng = random.Random(seed)

    lines = []
    for i in range(num_machines):
        # Vary the complexity of machines
        num_lights = rng.randint(4, 10)

        # About 80% of machines have joltage requirements (for part 2)
        if rng.random() < 0.8:
            # Number of counters must be <= num_lights (solver checks bit positions)
            num_counters = rng.randint(max(3, num_lights - 2), num_lights)
            # Limit buttons to at most num_counters + 2 to avoid exponential search
            # (too many free variables in Gaussian elimination causes infinite loops)
            num_buttons = rng.randint(3, min(12, num_counters + 2))
        else:
            num_counters = 0
            num_buttons = rng.randint(3, 12)

        machine = generate_machine(num_lights, num_buttons, num_counters, i, rng)
        lines.append(machine)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate Day 10 puzzle input")
    parser.add_argument(
        "-n",
        "--num-machines",
        type=int,
        default=166,
        help="Number of machines to generate (default: 166)",
    )
    parser.add_argument(
        "-s", "--seed", type=int, default=None, help="Random seed for reproducibility"
    )
    parser.add_argument(
        "-o", "--output", type=str, default=None, help="Output file (default: stdout)"
    )

    args = parser.parse_args()

    result = generate_input(num_machines=args.num_machines, seed=args.seed)

    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
            f.write("\n")
        print(f"Generated input written to {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
