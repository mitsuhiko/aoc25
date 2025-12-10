import re
from itertools import combinations


def parse_line(line):
    """Parse a machine line into target pattern and buttons."""
    # Extract target pattern [.##.#]
    target_match = re.search(r'\[([.#]+)\]', line)
    if not target_match:
        return None
    target_str = target_match.group(1)
    n_lights = len(target_str)
    target = 0
    for i, c in enumerate(target_str):
        if c == '#':
            target |= (1 << i)

    # Extract buttons (0,1,2) (3,4) etc
    buttons = []
    for match in re.finditer(r'\(([0-9,]+)\)', line):
        indices = [int(x) for x in match.group(1).split(',')]
        button_mask = 0
        for idx in indices:
            button_mask |= (1 << idx)
        buttons.append(button_mask)

    # Extract joltage requirements {3,5,4,7}
    joltage_match = re.search(r'\{([0-9,]+)\}', line)
    joltage = []
    if joltage_match:
        joltage = [int(x) for x in joltage_match.group(1).split(',')]

    return target, buttons, n_lights, joltage


def min_presses(target, buttons):
    """Find minimum number of button presses to achieve target."""
    n = len(buttons)

    # Try all subsets, starting from smallest
    for size in range(n + 1):
        for combo in combinations(range(n), size):
            result = 0
            for idx in combo:
                result ^= buttons[idx]
            if result == target:
                return size

    return float('inf')  # No solution found


def solve_part1(input_text):
    total = 0
    for line in input_text.strip().split('\n'):
        parsed = parse_line(line)
        if parsed is None:
            continue
        target, buttons, n_lights, joltage = parsed
        presses = min_presses(target, buttons)
        total += presses
    return total


def min_joltage_presses(buttons, joltage, n_counters):
    """Find minimum button presses to achieve target joltage values.

    Uses Gaussian elimination to find the solution space, then searches
    for minimum L1-norm solution.
    """
    from fractions import Fraction

    n_buttons = len(buttons)

    # Build matrix A where A[i][j] = 1 if button j affects counter i
    A = [[Fraction(0)] * n_buttons for _ in range(n_counters)]
    for j, button_mask in enumerate(buttons):
        for i in range(n_counters):
            if button_mask & (1 << i):
                A[i][j] = Fraction(1)

    b = [Fraction(v) for v in joltage[:n_counters]]

    # Augmented matrix [A | b]
    mat = [row[:] + [b[i]] for i, row in enumerate(A)]
    n, m = n_counters, n_buttons

    # Gaussian elimination to row echelon form
    pivot_row = 0
    pivot_cols = []
    for col in range(m):
        # Find pivot in this column
        found = -1
        for row in range(pivot_row, n):
            if mat[row][col] != 0:
                found = row
                break
        if found == -1:
            continue

        # Swap rows
        mat[pivot_row], mat[found] = mat[found], mat[pivot_row]

        # Normalize pivot row
        piv = mat[pivot_row][col]
        for c in range(col, m + 1):
            mat[pivot_row][c] /= piv

        # Eliminate in other rows
        for row in range(n):
            if row != pivot_row and mat[row][col] != 0:
                factor = mat[row][col]
                for c in range(col, m + 1):
                    mat[row][c] -= factor * mat[pivot_row][c]

        pivot_cols.append(col)
        pivot_row += 1
        if pivot_row >= n:
            break

    # Check consistency
    for row in range(pivot_row, n):
        if mat[row][m] != 0:
            return float('inf')  # Inconsistent

    # Identify free variables
    free_vars = [j for j in range(m) if j not in pivot_cols]
    n_free = len(free_vars)

    # If no free variables, unique solution
    if n_free == 0:
        x = [Fraction(0)] * m
        for i, col in enumerate(pivot_cols):
            x[col] = mat[i][m]
        # Check non-negative integer
        total = 0
        for val in x:
            if val < 0 or val.denominator != 1:
                return float('inf')
            total += int(val)
        return total

    # With free variables, solve the optimization problem
    # x[pivot_col] = mat[row][m] - sum(mat[row][fv] * x[fv]) for free vars fv
    # Objective: min sum(x) = sum(x[fv]) + sum(x[pivot_col])
    #          = sum(x[fv]) + sum(mat[row][m] - sum(mat[row][fv] * x[fv]))
    #          = sum(mat[row][m]) + sum(x[fv] * (1 - sum_over_rows(mat[row][fv])))

    pivot_to_row = {col: i for i, col in enumerate(pivot_cols)}

    # Compute objective coefficients for free variables
    # coef[j] = 1 - sum over pivot rows of mat[row][fv_j]
    obj_coef = []
    for fv in free_vars:
        col_sum = sum(mat[pivot_to_row[pc]][fv] for pc in pivot_cols)
        obj_coef.append(1 - col_sum)

    base_cost = sum(mat[pivot_to_row[pc]][m] for pc in pivot_cols)

    # Constraints: for each pivot col, x[pc] = mat[row][m] - sum(mat[row][fv] * x[fv]) >= 0
    # i.e., sum(mat[row][fv] * x[fv]) <= mat[row][m]

    # For small n_free, enumerate intelligently
    # For each free var, find valid range considering all constraints
    best = [float('inf')]

    def eval_solution(free_vals):
        x = [Fraction(0)] * m
        for i, fv in enumerate(free_vars):
            x[fv] = Fraction(free_vals[i])

        total = Fraction(0)
        for i, fv in enumerate(free_vars):
            total += free_vals[i]

        for col in pivot_cols:
            row = pivot_to_row[col]
            val = mat[row][m]
            for fv in free_vars:
                val -= mat[row][fv] * x[fv]
            if val < 0 or val.denominator != 1:
                return None
            total += int(val)

        return int(total) if total.denominator == 1 else None

    # Use linear programming insight:
    # If obj_coef[j] > 0, prefer x[fv_j] = 0
    # If obj_coef[j] < 0, prefer x[fv_j] as large as possible
    # If obj_coef[j] = 0, x[fv_j] doesn't affect objective

    # Start with heuristic solution
    heuristic_vals = []
    for i, fv in enumerate(free_vars):
        if obj_coef[i] >= 0:
            heuristic_vals.append(0)
        else:
            # Find max valid value for this free var given current vals
            max_v = 0
            for col in pivot_cols:
                row = pivot_to_row[col]
                if mat[row][fv] > 0:
                    # constraint: mat[row][m] - mat[row][fv] * x[fv] - other_terms >= 0
                    other = sum(mat[row][free_vars[j]] * heuristic_vals[j]
                               for j in range(i) if mat[row][free_vars[j]] != 0)
                    avail = mat[row][m] - other
                    if avail >= 0:
                        max_here = int(avail / mat[row][fv])
                        if max_v == 0:
                            max_v = max_here
                        else:
                            max_v = min(max_v, max_here)
            heuristic_vals.append(max_v)

    result = eval_solution(heuristic_vals)
    if result is not None:
        best[0] = result

    # For small n_free, do exhaustive search
    # Use max joltage as a safe bound for each free variable
    if n_free <= 5:
        max_fv = max(joltage) + 1

        from itertools import product
        for vals in product(range(max_fv), repeat=n_free):
            result = eval_solution(list(vals))
            if result is not None and result < best[0]:
                best[0] = result

    return best[0]


def solve_part2(input_text):
    total = 0
    for line in input_text.strip().split('\n'):
        parsed = parse_line(line)
        if parsed is None:
            continue
        target, buttons, n_lights, joltage = parsed
        if not joltage:
            continue
        n_counters = len(joltage)
        presses = min_joltage_presses(buttons, joltage, n_counters)
        total += presses
    return total


if __name__ == "__main__":
    with open("day10.txt") as f:
        input_text = f.read()

    print(f"Part 1: {solve_part1(input_text)}")
    print(f"Part 2: {solve_part2(input_text)}")
