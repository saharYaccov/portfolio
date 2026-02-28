"""
utils/target.py
───────────────
Helpers for placing the target randomly on an empty walkable cell.

Rule: the target must not land directly behind the snake's head
(i.e. in the opposite direction of travel).  If the only free cells
are behind the snake, the target is shifted 7 cells sideways
(left first, then right) until a non-behind walkable cell is found.
If no shift works the closest free cell is used as a last resort.
"""

import random
from typing import Collection


def _direction(body: list[tuple[int, int]]) -> tuple[int, int]:
    """
    Return the current movement direction (dr, dc) of the snake.
    Computed as head minus second segment.
    Returns (0, 0) if the snake has only one cell (no direction yet).
    """
    if len(body) < 2:
        return (0, 0)
    hr, hc = body[0]
    pr, pc = body[1]
    return (hr - pr, hc - pc)


def _behind_cell(head: tuple[int, int], direction: tuple[int, int]) -> tuple[int, int]:
    """The cell directly behind the head (opposite of travel direction)."""
    dr, dc = direction
    return (head[0] - dr, head[1] - dc)


def _shift_sideways(
    cell:     tuple[int, int],
    direction: tuple[int, int],
    walkable:  set[tuple[int, int]],
    occupied:  set[tuple[int, int]],
    steps:     int = 7,
) -> tuple[int, int] | None:
    """
    Try to move *cell* sideways (perpendicular to direction) by up to
    *steps* cells.  Returns the first free walkable cell found, or None.

    Perpendicular directions:
      if moving vertically  (dr!=0) → shift left/right (dc ±1)
      if moving horizontally (dc!=0) → shift up/down   (dr ±1)
    """
    dr, dc = direction

    if dr != 0:          # moving up or down  → sideways = left / right
        perp_options = [(0, -1), (0, 1)]
    elif dc != 0:        # moving left or right → sideways = up / down
        perp_options = [(-1, 0), (1, 0)]
    else:                # no direction known
        perp_options = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    for pdr, pdc in perp_options:
        r, c = cell
        for _ in range(steps):
            r += pdr
            c += pdc
            candidate = (r, c)
            if candidate in walkable and candidate not in occupied:
                return candidate

    return None


def _weighted_choice(
    cells:  list[tuple[int, int]],
    head:   tuple[int, int],
    bias:   float = 2.5,
) -> tuple[int, int]:
    """
    Choose a cell from *cells* with probability inversely proportional
    to its Manhattan distance from *head*.

    weight = 1 / (distance + 1) ** bias

    A higher *bias* makes close cells much more likely.
    bias=0 → pure random, bias=1 → mild preference, bias=2.5 → strong pull.
    """
    weights = []
    for r, c in cells:
        dist = abs(r - head[0]) + abs(c - head[1])
        weights.append(1.0 / (dist + 1) ** bias)

    return random.choices(cells, weights=weights, k=1)[0]


def place_target(
    walkable: Collection[tuple[int, int]],
    occupied: Collection[tuple[int, int]],
    body:     list[tuple[int, int]] | None = None,
) -> tuple[int, int] | None:
    """
    Pick a random walkable cell that is not occupied by the snake,
    avoiding the cell directly behind the snake's head.

    Parameters
    ----------
    walkable : all board cells that are part of the playfield.
    occupied : cells currently taken by the snake body.
    body     : snake body list (head-first).  Pass None if unknown
               (e.g. at level start before first move).

    Returns
    -------
    A (row, col) tuple for the new target, or None if the board is full.
    """
    occupied_set = set(occupied)
    walkable_set = set(walkable)
    free = [cell for cell in walkable_set if cell not in occupied_set]

    if not free:
        return None

    # If no body info → plain random placement
    if not body or len(body) < 2:
        return random.choice(free)

    direction  = _direction(body)
    head       = body[0]
    behind     = _behind_cell(head, direction)

    # Prefer cells that are NOT directly behind the head
    preferred = [cell for cell in free if cell != behind]

    if preferred:
        chosen = _weighted_choice(preferred, head)
    else:
        # All free cells are the behind cell — shift sideways
        chosen = _shift_sideways(behind, direction, walkable_set, occupied_set)
        if chosen is None:
            chosen = random.choice(free)   # absolute last resort

    # If chosen cell ended up being behind anyway, attempt a sideways shift
    if chosen == behind:
        shifted = _shift_sideways(chosen, direction, walkable_set, occupied_set)
        if shifted is not None:
            chosen = shifted

    return chosen