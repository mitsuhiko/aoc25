#!/usr/bin/env python3
"""Generator for Day 12 puzzle inputs.

Day 12: Polyomino packing puzzle
- Input consists of shape definitions followed by region specifications
- Shapes are polyominoes drawn with '#' characters
- Each region specifies dimensions (WxH) and required counts of each shape
- Part 1 checks if regions have sufficient area for the required pieces
"""

import random
import argparse


def generate_random_polyomino(size, rng):
    """Generate a random polyomino of given size.

    Args:
        size: Number of cells in the polyomino
        rng: Random number generator

    Returns:
        Set of (x, y) coordinates representing the polyomino
    """
    if size == 1:
        return {(0, 0)}

    # Start with a single cell
    cells = {(0, 0)}

    # Add cells one at a time
    for _ in range(size - 1):
        # Find all neighbors of current cells
        neighbors = set()
        for x, y in cells:
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                neighbor = (x + dx, y + dy)
                if neighbor not in cells:
                    neighbors.add(neighbor)

        # Pick a random neighbor to add
        if neighbors:
            cells.add(rng.choice(list(neighbors)))

    # Normalize to start at (0, 0)
    min_x = min(x for x, y in cells)
    min_y = min(y for x, y in cells)
    return {(x - min_x, y - min_y) for x, y in cells}


def polyomino_to_string(cells):
    """Convert a polyomino to a string representation.

    Args:
        cells: Set of (x, y) coordinates

    Returns:
        Multi-line string with '#' for cells and '.' for empty spaces
    """
    if not cells:
        return ""

    max_x = max(x for x, y in cells)
    max_y = max(y for x, y in cells)

    lines = []
    for y in range(max_y + 1):
        line = ""
        for x in range(max_x + 1):
            line += "#" if (x, y) in cells else "."
        lines.append(line)

    return "\n".join(lines)


def generate_input(num_shapes=6, num_regions=1000, seed=None):
    """Generate a valid Day 12 input.

    Args:
        num_shapes: Number of distinct polyomino shapes to generate
        num_regions: Number of regions to generate
        seed: Random seed for reproducibility

    Returns:
        String containing the generated input
    """
    rng = random.Random(seed)

    # Generate shapes with sizes 4-6 cells (typical polyominoes)
    shapes = []
    shape_sizes = []

    for i in range(num_shapes):
        size = rng.randint(4, 6)
        polyomino = generate_random_polyomino(size, rng)
        shapes.append(polyomino)
        shape_sizes.append(size)

    # Build output
    lines = []

    # Output shape definitions
    for i, shape in enumerate(shapes):
        lines.append(f"{i}:")
        lines.append(polyomino_to_string(shape))
        lines.append("")  # Empty line after each shape

    # Generate regions
    for _ in range(num_regions):
        # Random dimensions (35-50 for width and height)
        width = rng.randint(35, 50)
        height = rng.randint(35, 50)

        # Generate random piece counts
        # Make it so about 70% are valid (have enough area)
        total_area = width * height

        if rng.random() < 0.7:
            # Valid region - use about 60-95% of available area
            target_area = int(total_area * rng.uniform(0.6, 0.95))
        else:
            # Invalid region - use more than available area
            target_area = int(total_area * rng.uniform(1.05, 1.3))

        # Distribute target area among shapes
        counts = [0] * num_shapes
        remaining_area = target_area

        for i in range(num_shapes):
            if remaining_area > 0:
                # Randomly assign pieces
                max_pieces = remaining_area // shape_sizes[i]
                if max_pieces > 0:
                    pieces = rng.randint(0, min(max_pieces, 80))
                    counts[i] = pieces
                    remaining_area -= pieces * shape_sizes[i]

        # Format: "WxH: count0 count1 count2 ..."
        counts_str = " ".join(str(c) for c in counts)
        lines.append(f"{width}x{height}: {counts_str}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate Day 12 puzzle input")
    parser.add_argument(
        "-n",
        "--num-shapes",
        type=int,
        default=6,
        help="Number of polyomino shapes (default: 6)",
    )
    parser.add_argument(
        "-r",
        "--num-regions",
        type=int,
        default=1000,
        help="Number of regions (default: 1000)",
    )
    parser.add_argument(
        "-s", "--seed", type=int, default=None, help="Random seed for reproducibility"
    )
    parser.add_argument(
        "-o", "--output", type=str, default=None, help="Output file (default: stdout)"
    )

    args = parser.parse_args()

    result = generate_input(
        num_shapes=args.num_shapes, num_regions=args.num_regions, seed=args.seed
    )

    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
        print(f"Generated input written to {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
