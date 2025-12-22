# Advent of Slop 2025

This repository is 100% vibe coded. I don't have time for the calendar this
year, but I am still curious how the agent does. So far this all has been done
exclusively by Claude Code.

This references the web-browser skill
[from my skills repo](https://github.com/mitsuhiko/agent-commands/).

## Solutions

These are LLM generated descriptions of the tasks and their solutions.

### Day 01: Secret Entrance

**Task.** Simulate a circular safe dial with positions `0..99`, starting at
`50`. Each input line is a rotation like `L68`/`R8` (left decreases, right
increases, wrapping mod 100). Part 1 asks how often the dial *ends a rotation*
on `0`. Part 2 asks how often the dial *ever points at* `0` on any click during
a rotation (including the final click), which can include multiple passes for
distances `>= 100`.

**Solution (day01.py).**
- Part 1 is a direct simulation: update
  `position = (position ± distance) % 100` per line and increment a counter
  when `position == 0`.
- Part 2 avoids simulating every click. For each rotation it computes the first
  click index at which the dial reaches `0` (if any) from the current position
  and direction (`position` steps when turning left; `100 - position` when
  turning right). If that first hit is within the rotation distance, it adds
  `1 + (distance - first_hit) // 100` to account for further full loops. If the
  rotation starts at `0`, the dial returns to `0` once per full 100 clicks, so
  it adds `distance // 100`.

**Tradeoffs.** Part 2 is `O(lines)` instead of `O(sum(distance))`, which
matters for large distances (the prompt explicitly mentions values like
`R1000`). The arithmetic counting is slightly more error-prone than step
simulation, but keeps runtime bounded and predictable.

**Input generator (generators/gen_day01.py).** Produces a configurable number
of random `L`/`R` lines; ~70% of distances are in `1..99` and ~30% are in
`100..1000`, with an optional seed for reproducibility.

### Day 02: Gift Shop

**Task.** The input is a single comma-separated line of numeric ranges like
`start-end`. An ID is “invalid” if its decimal representation is made from a
smaller digit sequence repeated:
- Part 1: exactly twice (e.g. `6464`, `123123`).
- Part 2: at least twice (e.g. `111`, `123123123`).
For each range, find all invalid IDs inside it and add them up.

**Solution (day02.py).**
- Instead of scanning every number in a range, it generates invalid candidates
  by digit-length: pick a total length `num_digits`, pick a pattern length
  `pattern_len` that divides it, enumerate all patterns of that length (no
  leading zeros), repeat the pattern the needed number of times, and keep the
  resulting number if it falls within `[start, end]`.
- Part 1 is the special case where `num_digits` must be even and
  `pattern_len = num_digits / 2`.
- Each range is handled independently; a `set` is used to avoid counting the
  same number twice within a range (e.g. if multiple factorizations could
  produce the same repeated string).

**Tradeoffs.** This shifts work from “size of the ranges” to “number of
repeat-pattern candidates”. That makes huge ranges feasible, but it can still
get expensive for large digit counts because it enumerates all possible
patterns of each eligible length.

**Input generator (generators/gen_day02.py).** Builds `num_ranges` random
ranges of varying magnitudes (small `1..100`, medium up to ~6 digits, large up
to ~9 digits, and sometimes 10+ digits). It does not attempt to avoid overlaps;
ranges are emitted in the generated order, comma-separated on one line.

### Day 03: Lobby

**Task.** Each input line is a “bank” of single-digit joltages in fixed order.
You must choose digits (without reordering) to form the largest possible
number:
- Part 1: pick exactly 2 digits to form the maximum 2-digit value.
- Part 2: pick exactly 12 digits to form the maximum 12-digit value.
Sum the per-line maxima.

**Solution (day03.py).**
- Part 1 brute-forces all ordered pairs `(i, j)` with `i < j` and takes the
  best `10*digit[i] + digit[j]`.
- Part 2 uses the standard greedy “maximum subsequence of length `k`” approach:
  for each output position, scan the allowed window `[start, n-remaining]` and
  pick the largest digit, then continue after it. This maximizes the result
  lexicographically, which also maximizes its numeric value.

**Tradeoffs.** The Part 2 greedy method is linear in the input size times the
number of selected digits (`O(n * 12)` per line here) and avoids combinatorial
search; it’s correct because earlier digits dominate later digits in a
fixed-length decimal number. Part 1’s `O(n²)` per line is simple but would be
the first thing to optimize if line lengths were much larger.

**Input generator (generators/gen_day03.py).** Emits `num_lines` random digit
strings of length `line_length` (default 100) and enforces `line_length >= 12`
so Part 2 is always possible.

### Day 04: Printing Department

**Task.** The input is a grid of `@` (paper rolls) and `.` (empty). A roll is
“forklift-accessible” if it has fewer than 4 neighboring rolls among the 8
adjacent cells (including diagonals).
- Part 1: count rolls that are accessible in the initial grid.
- Part 2: repeatedly remove all currently accessible rolls, then re-evaluate
  accessibility, until nothing more can be removed; report the total removed.

**Solution (day04.py).**
- Part 1 scans every `@` and counts its 8 neighbors to test the `< 4` rule.
- Part 2 simulates the cascade with a loop: each round re-scans the whole grid,
  collects all accessible rolls, removes them all at once (turning `@` into
  `.`), and accumulates how many were removed.

**Tradeoffs.** The implementation is straightforward but re-checks the entire
grid each round, so it can do a lot of repeated work on large grids. A more
optimized approach would maintain a queue of “candidates whose neighbor count
changed” and update only affected cells after removals.

**Input generator (generators/gen_day04.py).** Creates a square grid (default
`140x140`) by filling each cell with `@` with probability ~0.65 (otherwise
`.`), with an optional seed.

### Day 05: Cafeteria

**Task.** The input has two sections separated by a blank line:
- A list of inclusive “fresh ID” ranges (`start-end`), which may overlap.
- A list of available ingredient IDs (one per line).
Part 1 counts how many listed IDs fall into *any* range. Part 2 ignores the ID
list and asks how many distinct integer IDs are covered by the union of the
ranges.

**Solution (day05.py).**
- Parses both sections, sorts the ranges, and merges overlaps (and directly
  adjacent ranges) into a disjoint, ordered list.
- Part 1 checks each ID with a binary search over the merged ranges (`O(log R)`
  per ID).
- Part 2 sums `end - start + 1` over the merged ranges to compute the size of
  the union.

**Tradeoffs.** Merging ranges up front makes membership tests and union-size
computation fast and simple. The implementation uses a manual binary search
(rather than e.g. `bisect`) but otherwise keeps the approach minimal and
robust.

**Input generator (generators/gen_day05.py).** Creates random ranges over a
very large ID space (default up to `600_000_000_000_000`), including ~10%
single-value ranges, and then emits a list of random IDs from the same space.

### Day 06: Trash Compactor

**Task.** The input is an ASCII “worksheet” containing many arithmetic problems
laid out horizontally. Each problem is a block of columns separated by a full
column of spaces. Each block has several numbers and an operator (`+` or `*`)
on the bottom row.
- Part 1: interpret each *row* (above the operator) as one integer (ignoring
  alignment spaces), apply the operator across the numbers in the block, and
  sum the per-block results.
- Part 2: reinterpret the same grid so that each *column* (above the operator)
  forms a number by reading digits top-to-bottom; apply the operator and sum
  again.

**Solution (day06.py).**
- Both parts start by normalizing line lengths, transposing the grid into
  columns, and splitting on all-space columns to isolate each problem block.
- Part 1 transposes each block back into rows; the last row is the operator and
  each preceding row (after `strip`) is parsed as an integer.
- Part 2 keeps the block in column form; it finds the operator by looking for
  `+`/`*` in the last character of any column, and parses each column’s digits
  (excluding spaces and the operator row) into an integer.

**Tradeoffs.** The transpose/split approach is compact and avoids ad-hoc
coordinate math, but it does require padding the whole grid and creating
transposed copies. For these input sizes that’s a good readability/performance
trade.

**Input generator (generators/gen_day06.py).** Builds a fixed 5-row grid (4
number rows + 1 operator row) by constructing each problem as a set of
character columns wide enough for the largest number in that problem (numbers
are right-aligned; the operator is placed in the bottom row), and inserts a
single all-space separator column between problems.

### Day 07: Laboratories

**Task.** A beam enters the top of a grid at `S` and moves downward. Empty
cells (`.`) let beams pass. A splitter (`^`) stops an incoming beam and emits
two new beams from the immediately-adjacent left and right cells, which then
continue downward. Beams can overlap/merge when they occupy the same cell.
- Part 1: count how many splitter events occur as the beam pattern propagates
  downward.
- Part 2: interpret splits as branching “timelines” for a single particle;
  count the total number of timelines after all possible paths have finished,
  accounting for timelines that converge to the same position.

**Solution (day07.py).**
- Finds the `S` coordinate, then simulates row-by-row.
- Part 1 tracks the set of active beam columns at the current row. When a
  column hits `^`, it increments `split_count` once and replaces that beam with
  beams at `col-1` and `col+1`. Using a `set` naturally merges overlapping
  beams.
- Part 2 tracks a mapping `column -> timeline_count`. At a splitter, each
  incoming timeline count is duplicated to left and right; when multiple
  timelines reach the same column, their counts add.

**Tradeoffs.** This is a compact “sweep-line” simulation
(`O(rows * active_columns)`) that avoids per-cell flood fills and, for Part 2,
avoids exponential blow-up by aggregating timelines by column each row.

**Input generator (generators/gen_day07.py).** Generates a symmetric splitter
pattern using Rule 90 (Sierpinski triangle / “Christmas tree”) with `S`
centered on the top row, placing `^` every `row_spacing` rows. An optional
`noise` parameter randomly removes some splitters to vary the shape.

### Day 08: Playground

**Task.** Given `N` junction boxes as `(x,y,z)` points, repeatedly connect
pairs in order of increasing Euclidean distance. Connections create “circuits”
(connected components); connecting two boxes already in the same circuit does
nothing.
- Part 1: after making the 1000 shortest pair-connections, multiply the sizes
  of the 3 largest circuits.
- Part 2: continue until everything is in one circuit; report the product of
  the `x` coordinates of the final connection that unified the last two
  components.

**Solution (day08.py).**
- Precomputes all `N(N-1)/2` pairwise squared distances `d²`, packs
  `(d², i, j)` into a single integer for speed/memory locality, sorts the edge
  list once, and reuses it for both parts via an `lru_cache`.
- Uses a Union-Find (disjoint set) structure to maintain components while
  iterating edges in sorted order.
- Part 1 unions only the first 1000 edges (even if some unions are no-ops),
  then counts component sizes and multiplies the top three.
- Part 2 runs through edges until the component count reaches 1; the last
  successful union’s endpoints determine the returned `xs[i] * xs[j]`.

**Tradeoffs.** Computing and sorting all pairwise edges is `O(N² log N)` and
memory-heavy, but with `N=1000` it’s still practical and keeps the
implementation close to Kruskal’s algorithm. Packing edges and caching the
precomputation are micro-optimizations to keep Python overhead down.

**Input generator (generators/gen_day08.py).** Generates `num_points` random
integer coordinates uniformly within `[0, coord_range]` for each axis
(defaults: 1000 points, range 0–100000).

### Day 09: Movie Theater

**Task.** The input lists coordinates of “red tiles” on a grid. You can pick
two red tiles as opposite corners of an axis-aligned rectangle; the rectangle’s
area counts tiles, so width/height are `|dx|+1` and `|dy|+1`.
- Part 1: maximize rectangle area over all red-tile pairs.
- Part 2: red tiles form a closed loop (consecutive points connected by green
  tiles, and the interior is green). The rectangle still needs red corners, but
  every other tile in the rectangle must be red or green, i.e. the rectangle
  must lie completely within the loop.

**Solution (day09.py).**
- Part 1 brute-forces all pairs of red tiles and tracks the maximum
  `(abs(x2-x1)+1) * (abs(y2-y1)+1)`.
- Part 2 treats the loop as a polygon built from consecutive points and tries
  rectangles induced by all red-tile pairs, largest-first:
  - Builds horizontal edges for consecutive pairs with equal `y`; otherwise it
    treats the pair as a vertical edge at `x1`.
  - Sorts all candidate rectangles by area descending and validates each with a
    few geometric checks: (a) no red vertex lies strictly inside the rectangle
    (2D range count via a Fenwick tree of sorted lists), (b) all four geometric
    corners are inside or on the polygon boundary (ray casting with
    memoization), and (c) no polygon edge “cuts” through the rectangle’s
    interior.
  - Returns the first valid rectangle (which is then maximal by area because of
    the descending search order).

**Tradeoffs.** Part 2 is much more complex than Part 1: it’s still `O(n²)`
candidates, but tries to make the per-candidate checks cheaper with indexing
and caching, and it short-circuits by checking larger rectangles first. The
polygon handling is written for axis-aligned segments; if consecutive points
are not aligned, the “else: vertical edge” interpretation is a simplification
rather than a general polygon segment.

**Input generator (generators/gen_day09.py).** Generates either a “spiral” or
“convex” polygon-like point sequence by sampling around the center with
trigonometric functions plus random jitter, clamping to a bounding box; it
outputs `num_vertices` lines of `x,y`.

### Day 10: Factory

**Task.** Each line describes a machine with:
- A target indicator pattern like `[.##.]` (lights start all-off).
- A list of buttons like `(0,3,4)` describing which indices a press affects.
- Part 1: in “light mode”, each press toggles the listed lights; find the
  fewest total presses to reach the target.
- Part 2: in “joltage mode”, ignore the light pattern; counters start at 0 and
  each press increments the listed counters by 1; find the fewest total presses
  to reach the target vector in `{...}`.
Sum the minimums across all machines.

**Solution (day10.py).**
- Part 1 models toggling as a linear system over GF(2) (`A x = b` mod 2). It
  performs Gaussian elimination with bitmasks to find a solution space, then
  enumerates all assignments of the free variables and picks the one with
  minimum Hamming weight (which corresponds to minimum press count because
  extra even presses are never helpful).
- Part 2 models increments as an integer linear system (`A x = b` over the
  rationals with the constraint `x >= 0` and integer). It reduces the system to
  RREF using exact `Fraction`s, then searches over bounded integer assignments
  of the free variables and derives pivot variables from the resulting
  equations, keeping the minimum `sum(x)`. For small numbers of free variables
  it uses nested loops; otherwise it uses a pruned DFS.

**Tradeoffs.** The approach is algebraically direct and exact (no floating
point), but the “minimize presses” step is exponential in the number of free
variables. The input generator constrains machine sizes to keep the
free-variable search tractable.

**Input generator (generators/gen_day10.py).** For each machine it randomly
chooses a light count, generates random buttons (each toggling 1–8 indices),
then creates a reachable target by XOR-ing the masks of a few randomly
“pressed” buttons. For Part 2 it generates a reachable joltage target by
sampling random nonnegative press counts for each button and computing the
implied counter totals; it also limits the number of buttons relative to
counters to avoid too many free variables.

### Day 11: Reactor

**Task.** The input describes a directed graph as adjacency lists
(`node: dest1 dest2 ...`).
- Part 1: count all distinct directed paths from `you` to `out`.
- Part 2: count all distinct directed paths from `svr` to `out` that visit both
  `dac` and `fft` (in any order).

**Solution (day11.py).**
- Parses the graph into a `dict[str, list[str]]`.
- Part 1 uses a memoized DFS: `paths(node) = sum(paths(child))`, with
  `paths(out) = 1` as the base case.
- Part 2 extends the memoization state to include two booleans (`visited_dac`,
  `visited_fft`), updating them when those nodes are reached, and only counting
  a path when it ends at `out` with both flags set.

**Tradeoffs.** This is linear in the size of the graph times the number of
memoization states, and relies on the graph being acyclic (or at least not
having cycles reachable from the start) so that “number of paths” is finite.

**Input generator (generators/gen_day11.py).** Assigns nodes to “levels” and
primarily chooses edges to lower-level nodes (to avoid cycles), then injects
special nodes (`you`, `svr`, `dac`, `fft`, `out`) and may force extra edges
toward `dac`, `fft`, and `out` to make Part 2-style paths likely.

### Day 12: Christmas Tree Farm

**Task.** The input defines a set of polyomino “present shapes” (`#` cells on a
small grid) and many rectangular regions `WxH: c0 c1 ...` listing how many
pieces of each shape must fit into that region. Pieces can be rotated/flipped
and must not overlap.
- Part 1: count how many regions can fit their required pieces.
- Part 2: narrative “free star”.

**Solution (day12.py).**
- The file contains general-purpose helpers for normalizing shapes, generating
  all 8 orientations, and even a backtracking packing solver.
- For the provided input, `solve_part1` does not run a packing search: it only
  checks the necessary area condition `sum(piece_area * count) <= W*H` and
  counts regions that pass. `solve_part2` returns a fixed “free star” message.

**Tradeoffs.** Area checking is extremely fast but is not sufficient to prove
packability in general (polyomino packing is NP-complete). This solution relies
on an input property (or generator design) where “area fits” implies “fits”.

**Input generator (generators/gen_day12.py).** Randomly generates `num_shapes`
polyominoes of size 4–6 via a random-growth process, then emits `num_regions`
random rectangles (35–50 each side) and piece-count vectors chosen so that ~70%
of regions have total requested area below the region area and ~30% exceed it.

## Note on Inputs and Explanations

The inputs in this repository are all generated by Claude Code as well and the
generators are included.  The description of the quizes are created by Claude Code
and the summarized explanations in the README are also produced by Claude Code
from the inputs, the generator, the code.

The official policies of Advent of Code ask that people do not share their
inputs. I strongly disagree with this policy. It does not prevent someone from
replicating anything anyways (as demonstrated by this repository) but it makes
it harder for people to independently run code far in the future when AOC no
longer exists.

## License

This repository does not contain any human generated code at all. As such it
cannot be copyrighted and should be seen as content in the public domain. To
the extend it is possible or necessary to license it, it should be considered
to be licensed under the Apache License 2.0.
