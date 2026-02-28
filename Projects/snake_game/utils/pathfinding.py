"""
utils/pathfinding.py
────────────────────
A* shortest-path finder adapted for the Snake grid.

The AI uses two heuristics together:
  1. A* to find the shortest safe path to the target.
  2. A flood-fill "reachability" check: after planning a move, verify the
     snake can still reach enough free space (avoids self-entrapment).

If no safe path exists the AI falls back to "survival mode":
choose the neighbour that maximises reachable free space.
"""

from __future__ import annotations
import heapq
from collections import deque
from typing import Optional


# ── A* ───────────────────────────────────────────────────────────────────────

def _heuristic(a: tuple[int, int], b: tuple[int, int]) -> int:
    """Manhattan distance heuristic."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(
    start:    tuple[int, int],
    goal:     tuple[int, int],
    occupied: set[tuple[int, int]],
    walkable: set[tuple[int, int]],
) -> list[tuple[int, int]]:
    """
    A* from *start* to *goal*.

    Parameters
    ----------
    start    : (row, col) of snake head.
    goal     : (row, col) of target.
    occupied : cells blocked by the snake body (excluding head).
    walkable : all cells that are part of the board.

    Returns
    -------
    List of (row, col) positions from start (exclusive) to goal (inclusive).
    Empty list if no path found.
    """
    DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    open_heap: list[tuple[int, int, tuple[int, int]]] = []
    # (f, g, pos)
    heapq.heappush(open_heap, (0 + _heuristic(start, goal), 0, start))

    came_from: dict[tuple[int, int], Optional[tuple[int, int]]] = {start: None}
    g_score:   dict[tuple[int, int], int]                        = {start: 0}

    while open_heap:
        f, g, current = heapq.heappop(open_heap)

        if current == goal:
            # reconstruct
            path = []
            node: Optional[tuple[int, int]] = current
            while node != start:
                path.append(node)
                node = came_from[node]
            path.reverse()
            return path

        if g > g_score.get(current, float("inf")):
            continue  # stale entry

        for dr, dc in DIRS:
            nb = (current[0] + dr, current[1] + dc)
            if nb not in walkable:
                continue
            if nb in occupied and nb != goal:
                continue
            tentative_g = g + 1
            if tentative_g < g_score.get(nb, float("inf")):
                g_score[nb] = tentative_g
                came_from[nb] = current
                f_new = tentative_g + _heuristic(nb, goal)
                heapq.heappush(open_heap, (f_new, tentative_g, nb))

    return []   # no path


# ── Flood-fill reachability ───────────────────────────────────────────────────

def flood_fill_count(
    origin:   tuple[int, int],
    blocked:  set[tuple[int, int]],
    walkable: set[tuple[int, int]],
) -> int:
    """
    BFS from *origin*; return the number of reachable free cells.
    Used to ensure the AI doesn't trap itself.
    """
    DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visited: set[tuple[int, int]] = {origin}
    queue   = deque([origin])
    count   = 0

    while queue:
        r, c = queue.popleft()
        count += 1
        for dr, dc in DIRS:
            nb = (r + dr, c + dc)
            if nb in walkable and nb not in blocked and nb not in visited:
                visited.add(nb)
                queue.append(nb)

    return count
