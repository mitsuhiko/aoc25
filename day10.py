import re
from fractions import Fraction
from math import gcd

# Pre-compile regex patterns for performance
TARGET_RE = re.compile(r"\[([.#]+)\]")
BUTTON_RE = re.compile(r"\(([0-9,]+)\)")
JOLTAGE_RE = re.compile(r"\{([0-9,]+)\}")


def parse_line(line):
    """Parse a machine line into target pattern and buttons."""
    # Extract target pattern [.##.#]
    target_match = TARGET_RE.search(line)
    if not target_match:
        return None
    target_str = target_match.group(1)
    n_lights = len(target_str)
    target = 0
    for i, c in enumerate(target_str):
        if c == "#":
            target |= 1 << i

    # Extract buttons (0,1,2) (3,4) etc
    buttons = []
    for match in BUTTON_RE.finditer(line):
        indices = [int(x) for x in match.group(1).split(",")]
        button_mask = 0
        for idx in indices:
            button_mask |= 1 << idx
        buttons.append(button_mask)

    # Extract joltage requirements {3,5,4,7}
    joltage_match = JOLTAGE_RE.search(line)
    joltage = []
    if joltage_match:
        joltage = [int(x) for x in joltage_match.group(1).split(",")]

    return target, buttons, n_lights, joltage


def min_presses(target, buttons):
    """Find minimum number of button presses to achieve target using Gaussian elimination over GF(2)."""
    n_buttons = len(buttons)
    if n_buttons == 0:
        return float("inf") if target != 0 else 0

    # Determine number of lights (bits in target)
    n_lights = max(
        target.bit_length(), max((b.bit_length() for b in buttons), default=0)
    )

    # Build matrix A where A[i][j] = 1 if button j toggles light i (over GF(2))
    # Augmented matrix [A | target] represented as list of integers (each row is a bitmask)
    # Format: each row i has bits 0..n_buttons-1 for A[i][j], and bit n_buttons for target[i]
    mat = []
    for i in range(n_lights):
        row = 0
        for j in range(n_buttons):
            if buttons[j] & (1 << i):
                row |= 1 << j
        # Add target bit
        if target & (1 << i):
            row |= 1 << n_buttons
        mat.append(row)

    # Gaussian elimination over GF(2)
    pivot_row = 0
    pivot_cols = []

    for col in range(n_buttons):
        # Find pivot in this column
        found = -1
        for row in range(pivot_row, n_lights):
            if mat[row] & (1 << col):
                found = row
                break

        if found == -1:
            continue

        # Swap rows
        mat[pivot_row], mat[found] = mat[found], mat[pivot_row]

        # Eliminate in other rows using XOR
        for row in range(n_lights):
            if row != pivot_row and (mat[row] & (1 << col)):
                mat[row] ^= mat[pivot_row]

        pivot_cols.append(col)
        pivot_row += 1
        if pivot_row >= n_lights:
            break

    # Check consistency: if any row has no variable bits but has target bit set
    for row in range(pivot_row, n_lights):
        # Check if target bit is set but all variable bits are 0
        if mat[row] & (1 << n_buttons):
            # Has target bit
            if (mat[row] & ((1 << n_buttons) - 1)) == 0:
                # But no variable bits
                return float("inf")

    # Also check pivot rows for consistency
    for row in range(pivot_row):
        if mat[row] == (1 << n_buttons):
            # Only target bit set, no variable bits
            return float("inf")

    # Identify free variables
    free_vars = [j for j in range(n_buttons) if j not in pivot_cols]
    n_free = len(free_vars)

    # If no free variables, unique solution
    if n_free == 0:
        total = 0
        for row in range(len(pivot_cols)):
            if mat[row] & (1 << n_buttons):
                total += 1
        return total

    # With free variables, need to minimize total number of 1s
    # Try all combinations of free variables (2^n_free possibilities)
    pivot_to_row = {col: i for i, col in enumerate(pivot_cols)}

    best = float("inf")
    for free_mask in range(1 << n_free):
        # Set free variables according to free_mask
        solution = 0
        for i, fv in enumerate(free_vars):
            if free_mask & (1 << i):
                solution |= 1 << fv

        # Compute pivot variables
        valid = True
        for pc in pivot_cols:
            row = pivot_to_row[pc]
            # x[pc] = mat[row][n_buttons] XOR sum of mat[row][fv] * x[fv] for free vars
            val = (mat[row] >> n_buttons) & 1
            for fv in free_vars:
                if (solution & (1 << fv)) and (mat[row] & (1 << fv)):
                    val ^= 1

            if val:
                solution |= 1 << pc

        # Count number of buttons pressed
        count = bin(solution).count("1")
        best = min(best, count)

    return best


def solve_part1(input_text):
    total = 0
    for line in input_text.strip().split("\n"):
        parsed = parse_line(line)
        if parsed is None:
            continue
        target, buttons, n_lights, joltage = parsed
        presses = min_presses(target, buttons)
        total += presses
    return total


def min_joltage_presses(buttons, joltage, n_counters):
    """Find minimum button presses to achieve target joltage values.

    Uses Gaussian elimination to find the solution space,
    then searches for minimum L1-norm solution.
    """
    n_buttons = len(buttons)
    n = n_counters
    m = n_buttons

    def lcm(a, b):
        return a // gcd(a, b) * b

    def var_upper_bound(button_mask):
        bound = None
        for i in range(n):
            if button_mask & (1 << i):
                bound = joltage[i] if bound is None else min(bound, joltage[i])
        return 0 if bound is None else bound

    # Augmented matrix [A | b] as Fractions for exact elimination.
    mat = []
    for i in range(n):
        row = [Fraction(1 if (buttons[j] & (1 << i)) else 0) for j in range(m)]
        row.append(Fraction(joltage[i]))
        mat.append(row)

    # Reduced row echelon form (RREF) over Q.
    pivot_row = 0
    pivot_cols = []
    for col in range(m):
        found = None
        for row in range(pivot_row, n):
            if mat[row][col] != 0:
                found = row
                break
        if found is None:
            continue

        if found != pivot_row:
            mat[pivot_row], mat[found] = mat[found], mat[pivot_row]

        piv = mat[pivot_row][col]
        if piv != 1:
            inv = 1 / piv
            prow = mat[pivot_row]
            for c in range(col, m + 1):
                prow[c] *= inv

        prow = mat[pivot_row]
        for row in range(n):
            if row == pivot_row:
                continue
            factor = mat[row][col]
            if factor == 0:
                continue
            trow = mat[row]
            for c in range(col, m + 1):
                trow[c] -= factor * prow[c]

        pivot_cols.append(col)
        pivot_row += 1
        if pivot_row >= n:
            break

    # Consistency check: 0 == nonzero.
    for row in range(pivot_row, n):
        if all(mat[row][c] == 0 for c in range(m)) and mat[row][m] != 0:
            return float("inf")

    pivot_col_set = set(pivot_cols)
    free_cols = [j for j in range(m) if j not in pivot_col_set]
    n_free = len(free_cols)

    if n_free == 0:
        total = 0
        for r, pc in enumerate(pivot_cols):
            val = mat[r][m]
            if val.denominator != 1 or val.numerator < 0:
                return float("inf")
            total += val.numerator
        return total

    # Enumerate free variables within tight bounds derived from A x = b.
    free_info = [(var_upper_bound(buttons[col]), col) for col in free_cols]
    free_info.sort(key=lambda x: x[0])
    free_bounds = [b for b, _ in free_info]
    free_cols = [c for _, c in free_info]

    # Precompute pivot-variable equations in integer form:
    # x_pivot = const - sum(coeff_i * free_i)
    equations = []
    for r in range(len(pivot_cols)):
        const = mat[r][m]
        coeffs = [mat[r][c] for c in free_cols]
        denom = const.denominator
        for coef in coeffs:
            denom = lcm(denom, coef.denominator)

        const_scaled = const.numerator * (denom // const.denominator)
        coeffs_scaled = tuple(
            coef.numerator * (denom // coef.denominator) for coef in coeffs
        )
        equations.append((denom, const_scaled, coeffs_scaled))

    best = float("inf")

    def try_update(total):
        nonlocal best
        if total is not None and total < best:
            best = total

    if n_free == 1:
        (ub0,) = free_bounds

        def eval_total(x0):
            if x0 >= best:
                return None
            total = x0
            for denom, const_scaled, (a0,) in equations:
                rhs = const_scaled - a0 * x0
                if rhs < 0 or rhs % denom:
                    return None
                total += rhs // denom
                if total >= best:
                    return None
            return total

        for x0 in range(ub0 + 1):
            if x0 >= best:
                break
            try_update(eval_total(x0))

    elif n_free == 2:
        ub0, ub1 = free_bounds

        def eval_total(x0, x1):
            if x0 + x1 >= best:
                return None
            total = x0 + x1
            for denom, const_scaled, (a0, a1) in equations:
                rhs = const_scaled - a0 * x0 - a1 * x1
                if rhs < 0 or rhs % denom:
                    return None
                total += rhs // denom
                if total >= best:
                    return None
            return total

        for x0 in range(ub0 + 1):
            if x0 >= best:
                break
            for x1 in range(ub1 + 1):
                if x0 + x1 >= best:
                    break
                try_update(eval_total(x0, x1))

    elif n_free == 3:
        ub0, ub1, ub2 = free_bounds

        def eval_total(x0, x1, x2):
            if x0 + x1 + x2 >= best:
                return None
            total = x0 + x1 + x2
            for denom, const_scaled, (a0, a1, a2) in equations:
                rhs = const_scaled - a0 * x0 - a1 * x1 - a2 * x2
                if rhs < 0 or rhs % denom:
                    return None
                total += rhs // denom
                if total >= best:
                    return None
            return total

        for x0 in range(ub0 + 1):
            if x0 >= best:
                break
            for x1 in range(ub1 + 1):
                s01 = x0 + x1
                if s01 >= best:
                    break
                for x2 in range(ub2 + 1):
                    if s01 + x2 >= best:
                        break
                    try_update(eval_total(x0, x1, x2))

    else:
        free_vals = [0] * n_free

        def dfs(i, sum_free):
            nonlocal best
            if sum_free >= best:
                return
            if i == n_free:
                total = sum_free
                for denom, const_scaled, coeffs_scaled in equations:
                    rhs = const_scaled
                    for coef, val in zip(coeffs_scaled, free_vals):
                        rhs -= coef * val
                    if rhs < 0 or rhs % denom:
                        return
                    total += rhs // denom
                    if total >= best:
                        return
                best = total
                return

            ub = free_bounds[i]
            for v in range(ub + 1):
                if sum_free + v >= best:
                    break
                free_vals[i] = v
                dfs(i + 1, sum_free + v)

        dfs(0, 0)

    return best


def solve_part2(input_text):
    total = 0
    for line in input_text.strip().split("\n"):
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
    with open("inputs/day10.txt") as f:
        input_text = f.read()

    print(f"Part 1: {solve_part1(input_text)}")
    print(f"Part 2: {solve_part2(input_text)}")
