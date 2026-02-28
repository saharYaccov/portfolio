"""
Board module: defines the grid shape (walkable cells) for each level.
All boards use a cell grid.  'True' = walkable, 'False' = wall / void.
"""

import numpy as np
import math


# ── helpers ──────────────────────────────────────────────────────────────────

def _full_square(size: int) -> np.ndarray:
    """All cells walkable – classic square board."""
    return np.ones((size, size), dtype=bool)


def _circle(size: int) -> np.ndarray:
    """Circular / oval board."""
    board = np.zeros((size, size), dtype=bool)
    cx = cy = size / 2
    rx = cx - 1
    ry = cy - 1
    for r in range(size):
        for c in range(size):
            if ((r - cy + 0.5) / ry) ** 2 + ((c - cx + 0.5) / rx) ** 2 <= 1.0:
                board[r][c] = True
    return board


def _cross(size: int) -> np.ndarray:
    """Plus / cross shaped board (Dalton-like)."""
    board = np.zeros((size, size), dtype=bool)
    third = size // 3
    two_third = 2 * third
    # horizontal bar
    board[third:two_third, :] = True
    # vertical bar
    board[:, third:two_third] = True
    return board


def _diamond(size: int) -> np.ndarray:
    """Diamond / rhombus board."""
    board = np.zeros((size, size), dtype=bool)
    cx = cy = size // 2
    for r in range(size):
        for c in range(size):
            if abs(r - cx) + abs(c - cy) <= cx:
                board[r][c] = True
    return board


def _hollow_square(size: int) -> np.ndarray:
    """Ring / frame board – walkable border, void inside."""
    board = np.zeros((size, size), dtype=bool)
    thick = max(2, size // 6)
    board[:thick, :] = True
    board[-thick:, :] = True
    board[:, :thick] = True
    board[:, -thick:] = True
    return board


def _zigzag(size: int) -> np.ndarray:
    """Maze-like zigzag corridors."""
    board = np.zeros((size, size), dtype=bool)
    lane = max(2, size // 8)
    rows_per_stripe = lane * 3

    for r in range(size):
        stripe = r // rows_per_stripe
        in_lane = (r % rows_per_stripe) < lane
        if in_lane:
            board[r, :] = True          # horizontal corridor
        else:
            # vertical opening at alternating ends
            if stripe % 2 == 0:
                board[r, size - lane:] = True
            else:
                board[r, :lane] = True
    return board


def _hourglass(size: int) -> np.ndarray:
    """Hourglass / bowtie shape."""
    board = np.zeros((size, size), dtype=bool)
    cx = size // 2
    cy = size // 2
    for r in range(size):
        half_w = int(abs(r - cy) / cy * cx) + 1
        c_start = max(0, cx - half_w)
        c_end   = min(size, cx + half_w + 1)
        board[r, c_start:c_end] = True
    return board


def _spiral_ring(size: int) -> np.ndarray:
    """
    Two concentric ring corridors joined by a gateway – looks like a
    stylised map / stadium.
    """
    board = np.zeros((size, size), dtype=bool)
    cx = cy = size / 2

    for r in range(size):
        for c in range(size):
            dist = math.hypot(r - cx + 0.5, c - cy + 0.5)
            outer = cx - 2
            inner1 = cx * 0.55
            inner2 = cx * 0.25
            if dist <= outer:
                if dist >= inner1:
                    board[r][c] = True          # outer ring corridor
                elif dist <= inner2:
                    board[r][c] = True          # inner circle island
    # gateway connectors (north and south)
    mid = size // 2
    gw = max(1, size // 12)
    board[0:size, mid - gw: mid + gw] = False   # clear spokes first
    board[: size // 2, mid - gw: mid + gw] = True
    board[size // 2:, mid - gw: mid + gw] = True
    return board


# ── Level catalogue ──────────────────────────────────────────────────────────
lvl=0
LEVEL_CONFIG = [
    # (label,            shape_fn,      grid_size, max_len,  description)
    ("Level 1",  _full_square,   20, 50,  "Classic Square"),
    ("Level 2",  _circle,        22, 40,  "Circle Arena"),
    ("Level 3",  _cross,         21, 30,  "Dalton Cross"),
    ("Level 4",  _diamond,       22, 40,  "Diamond Field"),
    ("Level 5",  _diamond,       22, 50,  "Diamond Field"),
    ("Level 6",  _hollow_square, 22, 40,  "Ring Track"),
    ("Level 7",  _zigzag,        24, 50,  "Zigzag Maze"),
    ("Level 8",  _hourglass,     22, 40,  "Hourglass"),
    ("Level 9",  _hourglass,     22, 30,  "Hourglass"),
    ("Level 10",  _spiral_ring,   26, 50,  "Spiral Ring"),
    ("Level 11",  _spiral_ring,   26, 40,  "Spiral Ring"),
    ("Level 12",  _spiral_ring,   26, 100,  "Spiral Ring"),
]


class Board:
    """Encapsulates the walkable grid for one level."""

    def __init__(self, level_index: int):
        idx = min(level_index, len(LEVEL_CONFIG) - 1)
        label, shape_fn, size, max_len, desc = LEVEL_CONFIG[idx]
        self.label       = label
        self.description = desc
        self.grid_size   = size
        self.max_len     = max_len
        self.grid: np.ndarray = shape_fn(size)   # bool array [row, col]

    def is_walkable(self, row: int, col: int) -> bool:
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            return bool(self.grid[row, col])
        return False

    def walkable_cells(self) -> list[tuple[int, int]]:
        rs, cs = np.where(self.grid)
        return list(zip(rs.tolist(), cs.tolist()))

    def total_cells(self) -> int:
        return int(self.grid.sum())
