# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is an Advent of Code 2025 repository. Note that 2025 has **12 days of puzzles** (not the traditional 25 days).

## Repository Structure

Each day follows a consistent pattern:
- `dayXX.py` - Python solution file (e.g., `day01.py`, `day02.py`, ..., `day12.py`)
- `dayXX.txt` - Puzzle input file (e.g., `day01.txt`, `day02.txt`, ..., `day12.txt`)

## Running Solutions

To run a solution:
```bash
python3 dayXX.py
```

This will print both Part 1 and Part 2 results.

## Code Structure

Each day's Python file follows this pattern:

```python
def solve_part1(input_text):
    # Part 1 solution
    return result

def solve_part2(input_text):
    # Part 2 solution
    return result

if __name__ == "__main__":
    with open("dayXX.txt") as f:
        input_text = f.read()

    print(f"Part 1: {solve_part1(input_text)}")
    print(f"Part 2: {solve_part2(input_text)}")
```

## Fetching Puzzle Inputs

Inputs are user-specific and require authentication. Use the `web-browser` skill to fetch them:

1. Launch the skill: `skill: "web-browser"`
2. Start Chrome: `./tools/start.js`
3. Navigate to the input URL: `./tools/nav.js https://adventofcode.com/2025/day/X/input`
4. Extract the text content: `./tools/eval.js 'document.body.innerText'`
5. Save to file using bash redirection or the Write tool

Example workflow:
```bash
cd /Users/mitsuhiko/.claude/skills/web-browser && ./tools/start.js
# Wait a moment for Chrome to start
cd /Users/mitsuhiko/.claude/skills/web-browser && ./tools/nav.js https://adventofcode.com/2025/day/2/input
cd /Users/mitsuhiko/.claude/skills/web-browser && ./tools/eval.js 'document.body.innerText' > /Users/mitsuhiko/Development/aoc25/day02.txt
```

Note: The user's session cookies are needed to fetch inputs, so the web-browser approach is required rather than simple curl commands.

## Puzzle URLs

- Main calendar: https://adventofcode.com/2025
- Day N problem: https://adventofcode.com/2025/day/N
- Day N input: https://adventofcode.com/2025/day/N/input

## Important Notes

- This year has only 12 days of puzzles (days 1-12)
- Inputs are personalized per user and cannot be shared
- Each puzzle has two parts (Part 1 and Part 2)
- Part 2 typically unlocks after completing Part 1
