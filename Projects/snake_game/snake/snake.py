"""
snake/snake.py
──────────────
The Snake data structure.

The snake is stored as a deque of (row, col) tuples;
the front (index 0) is the head.
"""

from __future__ import annotations
from collections import deque
from typing import Optional


class Snake:
    """
    Manages snake body, growth, and collision detection.

    Attributes
    ----------
    body     : deque of (row, col), head first.
    alive    : False when a collision has ended the game.
    score    : number of targets eaten.
    """

    def __init__(self, start: tuple[int, int]):
        self.body:  deque[tuple[int, int]] = deque([start])
        self.alive: bool = True
        self.score: int  = 0
        self._grow: int  = 0   # pending growth segments

    # ── properties ───────────────────────────────────────────────────────────

    @property
    def head(self) -> tuple[int, int]:
        return self.body[0]

    @property
    def length(self) -> int:
        return len(self.body)

    # Set for O(1) membership checks (kept in sync with body deque)
    @property
    def body_set(self) -> frozenset[tuple[int, int]]:
        return frozenset(self.body)

    # ── actions ──────────────────────────────────────────────────────────────

    def move(
        self,
        new_head: tuple[int, int],
        ate_target: bool,
        walkable: set[tuple[int, int]],
    ) -> None:
        """
        Advance the snake one step to *new_head*.

        Parameters
        ----------
        new_head   : next cell (must already be validated by the AI).
        ate_target : if True, the snake grows.
        walkable   : board walkable set; collision is checked here.
        """
        if not self.alive:
            return

        # Collision with wall / void
        if new_head not in walkable:
            self.alive = False
            return

        # Collision with own body (tail excluded if not growing)
        body_without_tail = set(self.body)
        if self._grow == 0:
            body_without_tail.discard(self.body[-1])
        if new_head in body_without_tail:
            self.alive = False
            return

        self.body.appendleft(new_head)

        if ate_target:
            self.score += 1
            self._grow += 2          # eat = grow 2 extra segments for drama
        else:
            if self._grow > 0:
                self._grow -= 1      # absorb pending growth
            else:
                self.body.pop()      # normal advance

    def eat(self) -> None:
        """Called externally when the head is on the target."""
        # Growth is handled inside move() via ate_target flag.
        pass

    def occupied(self) -> set[tuple[int, int]]:
        """All cells occupied by the snake body (head included)."""
        return set(self.body)

    def reset(self, start: tuple[int, int]) -> None:
        """Reset snake to a single-cell state at *start*."""
        self.body  = deque([start])
        self.alive = True
        self._grow = 0
        # score is NOT reset between levels
