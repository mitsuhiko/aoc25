"""Day 8: Minimum Spanning Tree with Union-Find

This puzzle involves connecting points in 3D space using a greedy approach based on
Euclidean distances. Given a set of junction boxes at various (x, y, z) coordinates,
the task is to progressively connect pairs of boxes starting with the closest pairs.
When two boxes are connected, they form a circuit, and boxes can transitively connect
through shared circuits. This is essentially Kruskal's algorithm for constructing a
minimum spanning forest.

Part 1 asks for the product of the three largest circuit sizes after making exactly
1000 connections. Part 2 requires continuing the connection process until all boxes
form a single circuit, then returning the product of the X coordinates of the final
pair that unified the graph. The solution uses a Union-Find (disjoint set) data
structure to efficiently track connected components and determine when merges occur.
"""

from functools import lru_cache


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        parent = self.parent
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(self, x, y):
        px = self.find(x)
        py = self.find(y)
        if px == py:
            return False

        rank = self.rank
        if rank[px] < rank[py]:
            px, py = py, px
        self.parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1
        return True


_IDX_BITS = 10
_IDX_MASK = (1 << _IDX_BITS) - 1
_EDGE_SHIFT = _IDX_BITS * 2


@lru_cache(maxsize=1)
def _precompute(input_text):
    xs = []
    ys = []
    zs = []
    for line in input_text.splitlines():
        line = line.strip()
        if not line:
            continue
        x_str, y_str, z_str = line.split(",")
        xs.append(int(x_str))
        ys.append(int(y_str))
        zs.append(int(z_str))

    n = len(xs)
    if n > (1 << _IDX_BITS):
        raise ValueError("Too many points for packed indices")

    edges = []
    append = edges.append
    for i in range(n - 1):
        xi = xs[i]
        yi = ys[i]
        zi = zs[i]
        base_i = i << _IDX_BITS
        for j in range(i + 1, n):
            dx = xi - xs[j]
            dy = yi - ys[j]
            dz = zi - zs[j]
            d2 = dx * dx + dy * dy + dz * dz
            append((d2 << _EDGE_SHIFT) | base_i | j)
    edges.sort()

    return xs, edges


def solve_part1(input_text):
    xs, edges = _precompute(input_text)
    n = len(xs)

    uf = UnionFind(n)
    for edge in edges[:1000]:
        i = (edge >> _IDX_BITS) & _IDX_MASK
        j = edge & _IDX_MASK
        uf.union(i, j)

    # Count circuit sizes
    circuit_sizes = [0] * n
    for i in range(n):
        root = uf.find(i)
        circuit_sizes[root] += 1

    # Get three largest
    sizes = sorted((x for x in circuit_sizes if x), reverse=True)
    return sizes[0] * sizes[1] * sizes[2]


def solve_part2(input_text):
    xs, edges = _precompute(input_text)
    n = len(xs)

    uf = UnionFind(n)
    num_components = n

    for edge in edges:
        i = (edge >> _IDX_BITS) & _IDX_MASK
        j = edge & _IDX_MASK
        if uf.union(i, j):
            num_components -= 1
            if num_components == 1:
                # This was the last connection that unified everything
                return xs[i] * xs[j]

    return None


if __name__ == "__main__":
    import sys

    input_file = sys.argv[1] if len(sys.argv) > 1 else "inputs/day08.txt"
    with open(input_file) as f:
        input_text = f.read()

    print(f"Part 1: {solve_part1(input_text)}")
    print(f"Part 2: {solve_part2(input_text)}")
