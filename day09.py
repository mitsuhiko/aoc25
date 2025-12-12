def solve_part1(input_text):
    # Parse coordinates
    red_tiles = []
    for line in input_text.strip().split("\n"):
        x, y = map(int, line.split(","))
        red_tiles.append((x, y))

    # Find largest rectangle area using any two red tiles as opposite corners
    max_area = 0
    n = len(red_tiles)
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[j]
            # Area includes boundary tiles, so +1 for each dimension
            area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            if area > max_area:
                max_area = area

    return max_area


def solve_part2(input_text):
    from collections import defaultdict
    import bisect
    from functools import lru_cache

    # Parse coordinates
    red_tiles = []
    for line in input_text.strip().split("\n"):
        x, y = map(int, line.split(","))
        red_tiles.append((x, y))

    n = len(red_tiles)
    red_set = set(red_tiles)

    # Build edge segments (both horizontal and vertical)
    h_edges = []  # (y, x_min, x_max) for horizontal edges
    v_edges = []  # (x, y_min, y_max) for vertical edges

    for i in range(n):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[(i + 1) % n]
        if y1 == y2:  # Horizontal edge
            h_edges.append((y1, min(x1, x2), max(x1, x2)))
        else:  # Vertical edge
            v_edges.append((x1, min(y1, y2), max(y1, y2)))

    # Build spatial indices for edges
    h_edges_by_y = defaultdict(list)
    for y, x_min, x_max in h_edges:
        h_edges_by_y[y].append((x_min, x_max))

    v_edges_by_x = defaultdict(list)
    for x, y_min, y_max in v_edges:
        v_edges_by_x[x].append((y_min, y_max))

    # Pre-sort vertical edge x-coordinates for efficient ray casting
    sorted_v_x = sorted(v_edges_by_x.keys())

    @lru_cache(maxsize=50000)
    def point_inside_or_on_boundary(px, py):
        """Check if point is inside polygon or on boundary using ray casting"""
        # Check if on boundary first - use spatial indices
        if py in h_edges_by_y:
            for x_min, x_max in h_edges_by_y[py]:
                if x_min <= px <= x_max:
                    return True

        if px in v_edges_by_x:
            for y_min, y_max in v_edges_by_x[px]:
                if y_min <= py <= y_max:
                    return True

        # Ray casting: count crossings going right - use sorted list with binary search
        crossings = 0
        # Use binary search to find first x > px
        start_idx = bisect.bisect_right(sorted_v_x, px)
        for i in range(start_idx, len(sorted_v_x)):
            x = sorted_v_x[i]
            for y_min, y_max in v_edges_by_x[x]:
                if y_min < py < y_max:
                    crossings += 1

        return crossings % 2 == 1

    def rectangle_valid(rx_min, rx_max, ry_min, ry_max):
        """Check if rectangle is entirely inside polygon"""
        # Check that no red tile is strictly inside the rectangle FIRST
        # This is a fast check that can reject many candidates early
        for rx, ry in red_tiles:
            if rx_min < rx < rx_max and ry_min < ry < ry_max:
                return False

        # Check all 4 geometric corners are inside or on boundary
        corners = [
            (rx_min, ry_min),
            (rx_min, ry_max),
            (rx_max, ry_min),
            (rx_max, ry_max),
        ]
        for cx, cy in corners:
            if not point_inside_or_on_boundary(cx, cy):
                return False

        # Check if any boundary edge completely crosses through the rectangle
        # (i.e., the edge spans the full width/height and cuts the rectangle in two)

        # Horizontal edges that cross full width - use spatial index
        for y in range(ry_min + 1, ry_max):
            if y in h_edges_by_y:
                for x_min, x_max in h_edges_by_y[y]:
                    if x_min <= rx_min and x_max >= rx_max:
                        # Edge spans full width - rectangle is cut in two
                        return False

        # Vertical edges that cross full height - use spatial index
        for x in range(rx_min + 1, rx_max):
            if x in v_edges_by_x:
                for y_min, y_max in v_edges_by_x[x]:
                    if y_min <= ry_min and y_max >= ry_max:
                        # Edge spans full height - rectangle is cut in two
                        return False

        # Also check for edges that have endpoints strictly inside the rectangle
        # (meaning the boundary turns inside the rectangle)
        for y in range(ry_min + 1, ry_max):
            if y in h_edges_by_y:
                for x_min, x_max in h_edges_by_y[y]:
                    # Check if endpoints are strictly inside x-range
                    if rx_min < x_min < rx_max or rx_min < x_max < rx_max:
                        return False

        for x in range(rx_min + 1, rx_max):
            if x in v_edges_by_x:
                for y_min, y_max in v_edges_by_x[x]:
                    if ry_min < y_min < ry_max or ry_min < y_max < ry_max:
                        return False

        return True

    # Generate all pairs with their areas and sort by area descending
    pairs_with_area = []
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[j]
            rx_min, rx_max = min(x1, x2), max(x1, x2)
            ry_min, ry_max = min(y1, y2), max(y1, y2)
            area = (rx_max - rx_min + 1) * (ry_max - ry_min + 1)
            pairs_with_area.append((area, rx_min, rx_max, ry_min, ry_max))

    # Sort by area descending - largest first
    pairs_with_area.sort(reverse=True)

    # Find largest valid rectangle
    max_area = 0
    for area, rx_min, rx_max, ry_min, ry_max in pairs_with_area:
        # Early termination: all remaining rectangles are smaller
        if area <= max_area:
            break

        if rectangle_valid(rx_min, rx_max, ry_min, ry_max):
            # Since we're processing largest first, the first valid one is the answer
            return area

    return max_area


if __name__ == "__main__":
    with open("inputs/day09.txt") as f:
        input_text = f.read()

    print(f"Part 1: {solve_part1(input_text)}")
    print(f"Part 2: {solve_part2(input_text)}")
