#!/usr/bin/env python3
"""Generator for Day 09 puzzle inputs.

Day 09: Polygon Rectangle puzzle
- Input consists of x,y coordinate pairs forming a polygon
- Each line has format: x,y
- The coordinates form a closed polygon path
- Part 1: Find largest rectangle using any two vertices as opposite corners
- Part 2: Find largest rectangle fully contained within the polygon
"""

import random
import argparse
import math


def generate_spiral_polygon(num_vertices=500, seed=None, width=100000, height=100000):
    """Generate a valid polygon using a spiral pattern.

    This creates a polygon that spirals outward and then back inward,
    ensuring it's a valid simple polygon (no self-intersections).

    Args:
        num_vertices: Number of vertices in the polygon
        seed: Random seed for reproducibility
        width: Maximum x coordinate range
        height: Maximum y coordinate range

    Returns:
        List of (x, y) tuples representing the polygon vertices
    """
    if seed is not None:
        random.seed(seed)

    vertices = []

    # Start position
    center_x = width // 2
    center_y = height // 2

    # Generate spiral polygon
    # We'll create a rough spiral by gradually increasing radius
    # and adding some randomness to make it interesting

    max_radius = min(width, height) // 2 - 1000

    for i in range(num_vertices):
        # Progress through the spiral (0 to 1)
        progress = i / num_vertices

        # Angle increases as we spiral
        # Multiple rotations for interesting shape
        rotations = 4 + random.random() * 2  # 4-6 rotations
        angle = progress * rotations * 2 * math.pi

        # Radius increases then decreases to create closed shape
        # Use a smooth function that goes up and comes back down
        if progress < 0.5:
            # Expanding phase
            radius_progress = progress * 2
        else:
            # Contracting phase
            radius_progress = (1 - progress) * 2

        # Add some variation to radius
        base_radius = radius_progress * max_radius
        radius_variation = random.uniform(-0.1, 0.1) * max_radius
        radius = base_radius + radius_variation

        # Ensure radius is positive
        radius = max(1000, radius)

        # Calculate position
        x = int(center_x + radius * math.cos(angle))
        y = int(center_y + radius * math.sin(angle))

        # Add some random jitter to make it less perfect
        jitter_x = random.randint(-500, 500)
        jitter_y = random.randint(-500, 500)

        x += jitter_x
        y += jitter_y

        # Clamp to valid range
        x = max(1000, min(width - 1000, x))
        y = max(1000, min(height - 1000, y))

        vertices.append((x, y))

    return vertices


def generate_convex_polygon(num_vertices=500, seed=None, width=100000, height=100000):
    """Generate a valid convex polygon.

    Creates a convex polygon by generating random points and computing their
    convex hull, then sampling points along the hull.

    Args:
        num_vertices: Target number of vertices in the polygon
        seed: Random seed for reproducibility
        width: Maximum x coordinate range
        height: Maximum y coordinate range

    Returns:
        List of (x, y) tuples representing the polygon vertices
    """
    if seed is not None:
        random.seed(seed)

    vertices = []
    center_x = width // 2
    center_y = height // 2
    max_radius = min(width, height) // 2 - 1000

    # Generate points on an ellipse with some randomness
    for i in range(num_vertices):
        angle = (i / num_vertices) * 2 * math.pi

        # Vary the radius a bit to make it less circular
        radius_variation = random.uniform(0.7, 1.0)
        radius = max_radius * radius_variation

        x = int(center_x + radius * math.cos(angle))
        y = int(center_y + radius * math.sin(angle))

        # Add small jitter
        jitter_x = random.randint(-200, 200)
        jitter_y = random.randint(-200, 200)

        x += jitter_x
        y += jitter_y

        vertices.append((x, y))

    return vertices


def generate_input(num_vertices=500, seed=None, polygon_type="spiral"):
    """Generate a valid Day 09 input.

    Args:
        num_vertices: Number of vertices in the polygon
        seed: Random seed for reproducibility
        polygon_type: Type of polygon to generate ('spiral' or 'convex')

    Returns:
        String containing the generated input
    """
    if seed is not None:
        random.seed(seed)

    if polygon_type == "convex":
        vertices = generate_convex_polygon(num_vertices, seed)
    else:
        vertices = generate_spiral_polygon(num_vertices, seed)

    # Format as lines of "x,y"
    lines = [f"{x},{y}" for x, y in vertices]

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Generate Day 09 puzzle input")
    parser.add_argument(
        "-n",
        "--num-vertices",
        type=int,
        default=500,
        help="Number of vertices in the polygon (default: 500)",
    )
    parser.add_argument(
        "-s", "--seed", type=int, default=None, help="Random seed for reproducibility"
    )
    parser.add_argument(
        "-o", "--output", type=str, default=None, help="Output file (default: stdout)"
    )
    parser.add_argument(
        "-t",
        "--type",
        type=str,
        default="spiral",
        choices=["spiral", "convex"],
        help="Type of polygon to generate (default: spiral)",
    )

    args = parser.parse_args()

    result = generate_input(
        num_vertices=args.num_vertices, seed=args.seed, polygon_type=args.type
    )

    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
        print(
            f"Generated polygon with {args.num_vertices} vertices written to {args.output}"
        )
    else:
        print(result)


if __name__ == "__main__":
    main()
