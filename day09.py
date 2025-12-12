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

    def point_inside_or_on_boundary(px, py):
        """Check if point is inside polygon or on boundary using ray casting"""
        # Check if on boundary first
        for y, x_min, x_max in h_edges:
            if py == y and x_min <= px <= x_max:
                return True
        for x, y_min, y_max in v_edges:
            if px == x and y_min <= py <= y_max:
                return True

        # Ray casting: count crossings going right
        crossings = 0
        for x, y_min, y_max in v_edges:
            if x > px and y_min < py < y_max:
                crossings += 1

        return crossings % 2 == 1

    def rectangle_valid(rx_min, rx_max, ry_min, ry_max):
        """Check if rectangle is entirely inside polygon"""
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

        # Check that no red tile is strictly inside the rectangle
        for rx, ry in red_tiles:
            if rx_min < rx < rx_max and ry_min < ry < ry_max:
                return False

        # Check if any boundary edge completely crosses through the rectangle
        # (i.e., the edge spans the full width/height and cuts the rectangle in two)

        # Horizontal edges that cross full width
        for y, x_min, x_max in h_edges:
            if ry_min < y < ry_max:  # Edge is in interior y-range
                if x_min <= rx_min and x_max >= rx_max:
                    # Edge spans full width - rectangle is cut in two
                    return False

        # Vertical edges that cross full height
        for x, y_min, y_max in v_edges:
            if rx_min < x < rx_max:  # Edge is in interior x-range
                if y_min <= ry_min and y_max >= ry_max:
                    # Edge spans full height - rectangle is cut in two
                    return False

        # Also check for edges that have endpoints strictly inside the rectangle
        # (meaning the boundary turns inside the rectangle)
        for y, x_min, x_max in h_edges:
            if ry_min < y < ry_max:  # Edge in interior y-range
                # Check if endpoints are strictly inside x-range
                if rx_min < x_min < rx_max or rx_min < x_max < rx_max:
                    return False

        for x, y_min, y_max in v_edges:
            if rx_min < x < rx_max:  # Edge in interior x-range
                if ry_min < y_min < ry_max or ry_min < y_max < ry_max:
                    return False

        return True

    # Find largest rectangle where both corners are red tiles and rectangle is valid
    max_area = 0
    for i in range(len(red_tiles)):
        for j in range(i + 1, len(red_tiles)):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[j]

            rx_min, rx_max = min(x1, x2), max(x1, x2)
            ry_min, ry_max = min(y1, y2), max(y1, y2)

            area = (rx_max - rx_min + 1) * (ry_max - ry_min + 1)
            if area <= max_area:
                continue  # Skip if can't beat current best

            if rectangle_valid(rx_min, rx_max, ry_min, ry_max):
                max_area = area

    return max_area


if __name__ == "__main__":
    with open("day09.txt") as f:
        input_text = f.read()

    print(f"Part 1: {solve_part1(input_text)}")
    print(f"Part 2: {solve_part2(input_text)}")
