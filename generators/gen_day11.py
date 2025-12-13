#!/usr/bin/env python3
"""Generator for Day 11 puzzle inputs.

Day 11: Graph path counting puzzle
- Input consists of directed graph edges in DAG format
- Format: node: dest1 dest2 dest3 ...
- Part 1 counts paths from "you" to "out"
- Part 2 counts paths from "svr" to "out" that visit both "dac" and "fft"
"""

import random
import argparse


def generate_node_name(used_names, special_names):
    """Generate a unique 3-letter node name."""
    while True:
        name = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=3))
        if name not in used_names and name not in special_names:
            used_names.add(name)
            return name


def generate_input(num_nodes=100, avg_degree=3, seed=None):
    """Generate a valid Day 11 input.

    Args:
        num_nodes: Number of nodes to generate (excluding special nodes)
        avg_degree: Average number of outgoing edges per node
        seed: Random seed for reproducibility

    Returns:
        String containing the generated input
    """
    if seed is not None:
        random.seed(seed)

    # Special nodes required by the puzzle
    special_nodes = {"you", "out", "svr", "dac", "fft"}
    used_names = set(special_nodes)

    # Generate regular node names
    regular_nodes = []
    for _ in range(num_nodes):
        regular_nodes.append(generate_node_name(used_names, special_nodes))

    # Assign levels to each node for DAG construction
    # Higher level nodes can only point to same or lower level nodes
    node_levels = {}

    # Level assignment (higher = closer to start, lower = closer to out)
    node_levels["out"] = 0  # Sink - lowest level
    node_levels["fft"] = random.randint(3, 5)
    node_levels["dac"] = random.randint(3, 5)
    node_levels["svr"] = random.randint(8, 10)
    node_levels["you"] = random.randint(8, 10)

    # Assign levels to regular nodes
    random.shuffle(regular_nodes)
    for i, node in enumerate(regular_nodes):
        # Distribute nodes across levels 1-9
        node_levels[node] = 1 + (i * 9) // len(regular_nodes)

    # Build graph ensuring it's a DAG
    graph = {}

    # For each node, connect to nodes at same or lower level
    all_nodes = ["you", "svr", "dac", "fft"] + regular_nodes

    for node in all_nodes:
        if node == "out":
            continue  # 'out' is the sink, no outgoing edges

        node_level = node_levels[node]

        # Find candidate targets (same level or lower, excluding self)
        candidates = [n for n in all_nodes if node_levels[n] < node_level and n != node]

        if not candidates:
            # If no lower-level candidates, must connect to 'out'
            graph[node] = ["out"]
        else:
            # Choose random targets
            num_edges = random.randint(1, min(avg_degree + 2, len(candidates)))
            targets = random.sample(candidates, num_edges)

            # Special node connection rules to ensure puzzle solvability
            if node == "you":
                # Ensure 'you' has a path to 'out'
                if "out" not in targets and random.random() < 0.3:
                    targets.append("out")
            elif node == "svr":
                # Ensure 'svr' can reach 'dac' (for part 2)
                if "dac" not in targets and random.random() < 0.8:
                    targets.append("dac")
            elif node == "dac":
                # Ensure 'dac' can reach 'fft' (for part 2)
                if "fft" not in targets and random.random() < 0.8:
                    targets.append("fft")
            elif node == "fft":
                # Ensure 'fft' can reach 'out' (for part 2)
                if "out" not in targets and random.random() < 0.7:
                    targets.append("out")

            # Ensure every node has at least some path toward 'out'
            if random.random() < 0.2 and "out" not in targets:
                targets.append("out")

            graph[node] = targets

    # Shuffle node order for output
    output_nodes = list(graph.keys())
    random.shuffle(output_nodes)

    # Format output
    lines = []
    for node in output_nodes:
        destinations = " ".join(graph[node])
        lines.append(f"{node}: {destinations}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate Day 11 puzzle input")
    parser.add_argument(
        "-n",
        "--num-nodes",
        type=int,
        default=100,
        help="Number of nodes to generate (default: 100)",
    )
    parser.add_argument(
        "-s", "--seed", type=int, default=None, help="Random seed for reproducibility"
    )
    parser.add_argument(
        "-o", "--output", type=str, default=None, help="Output file (default: stdout)"
    )

    args = parser.parse_args()

    result = generate_input(num_nodes=args.num_nodes, seed=args.seed)

    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
        print(f"Generated input written to {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
