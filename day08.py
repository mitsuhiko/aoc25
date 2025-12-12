import math
from collections import defaultdict


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True


def solve_part1(input_text):
    lines = [line.strip() for line in input_text.strip().split("\n") if line.strip()]
    points = []
    for line in lines:
        x, y, z = map(int, line.split(","))
        points.append((x, y, z))

    n = len(points)

    # Calculate all pairwise distances
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            dz = points[i][2] - points[j][2]
            dist = math.sqrt(dx * dx + dy * dy + dz * dz)
            distances.append((dist, i, j))

    # Sort by distance
    distances.sort()

    # Connect 1000 closest pairs
    uf = UnionFind(n)
    for _, i, j in distances[:1000]:
        uf.union(i, j)

    # Count circuit sizes
    circuit_sizes = defaultdict(int)
    for i in range(n):
        root = uf.find(i)
        circuit_sizes[root] += 1

    # Get three largest
    sizes = sorted(circuit_sizes.values(), reverse=True)
    return sizes[0] * sizes[1] * sizes[2]


def solve_part2(input_text):
    lines = [line.strip() for line in input_text.strip().split("\n") if line.strip()]
    points = []
    for line in lines:
        x, y, z = map(int, line.split(","))
        points.append((x, y, z))

    n = len(points)

    # Calculate all pairwise distances
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            dz = points[i][2] - points[j][2]
            dist = math.sqrt(dx * dx + dy * dy + dz * dz)
            distances.append((dist, i, j))

    # Sort by distance
    distances.sort()

    # Connect pairs until all in one circuit
    uf = UnionFind(n)
    num_components = n

    for _, i, j in distances:
        if uf.union(i, j):
            num_components -= 1
            if num_components == 1:
                # This was the last connection that unified everything
                return points[i][0] * points[j][0]

    return None


if __name__ == "__main__":
    with open("inputs/day08.txt") as f:
        input_text = f.read()

    print(f"Part 1: {solve_part1(input_text)}")
    print(f"Part 2: {solve_part2(input_text)}")
