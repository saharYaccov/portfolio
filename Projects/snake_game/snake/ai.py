"""
snake/ai.py
───────────
AI controller using A* pathfinding + flood-fill safety,
enhanced with Logistic Regression learning from past games.

Strategy (per tick)
────────────────────
0. [ML ASSIST] If the model is trained, use its direction ranking to bias
   the move selection — prefer ML-suggested safe moves when A* is uncertain.
1. If a corner override is active → navigate to that corner via A*.
2. A* to target with flood-fill safety check.
3. Tail-chase fallback if direct path would trap the snake.
4. Pure survival (max free space) as last resort.
   When multiple directions tie for best space, ML ranking breaks the tie.

Corner override (hidden keys in main.py)
─────────────────────────────────────────
  A → top-left corner      L → top-right corner
  Z → bottom-left corner   . → bottom-right corner

Call  ai.set_corner(corner_cell)  to activate.
The override clears automatically once the snake reaches the corner.
"""

from __future__ import annotations

import random
from typing import Optional

from utils.pathfinding import astar, flood_fill_count
from snake.ml_model import SnakeMLModel, extract_features, DIRECTIONS, DIR_DELTAS

DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
safe_snk = 3 # bigger - more safe

class SnakeAI:

    def __init__(self, ml_model: Optional[SnakeMLModel] = None):
        self.path:             list[tuple[int, int]] = []
        self.danger_mode:      bool  = False
        self._corner_target:   Optional[tuple[int, int]] = None
        self.ml_model:         Optional[SnakeMLModel] = ml_model
        self._prev_dir:        tuple[int, int] = (0, 1)  # default: right

    # ── corner override ───────────────────────────────────────────────────────

    def set_corner(self, corner: tuple[int, int]):
        self._corner_target = corner

    def clear_corner(self):
        self._corner_target = None

    # ── helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def _behind(body: list[tuple[int, int]]) -> Optional[tuple[int, int]]:
        return body[1] if len(body) >= 2 else None

    def _safe_move_toward(
        self,
        head:      tuple[int, int],
        goal:      tuple[int, int],
        occupied:  set[tuple[int, int]],
        body_tail: tuple[int, int],
        walkable:  set[tuple[int, int]],
        body_len:  int,
        neck:      Optional[tuple[int, int]] = None,
    ) -> tuple[Optional[tuple[int, int]], list[tuple[int, int]]]:
        path = astar(head, goal, (occupied - {body_tail}) - {head}, walkable)
        if path:
            next_cell = path[0]
            if next_cell == neck:
                return None, []
            free = flood_fill_count(
                next_cell, (occupied - {body_tail}) - {next_cell}, walkable)
            if free >= safe_snk*body_len // 2 + 1 and random.randint(1,7000)>200:
                return next_cell, path
        return None, []

    def _ml_preferred_dirs(
        self,
        head:     tuple[int, int],
        body:     list[tuple[int, int]],
        target:   tuple[int, int],
        walkable: set[tuple[int, int]],
        board_size: int,
    ) -> Optional[list[tuple[int, int]]]:
        if self.ml_model is None or not self.ml_model.trained:
            return None
        features = extract_features(head, body, target, walkable,
                                     self._prev_dir, board_size)
        return self.ml_model.predict_direction(features)

    # ── public API ────────────────────────────────────────────────────────────

    def compute_next_move(
        self,
        head:       tuple[int, int],
        target:     tuple[int, int],
        body:       list[tuple[int, int]],
        walkable:   set[tuple[int, int]],
        board_size: int = 20,
    ) -> Optional[tuple[int, int]]:

        occupied  = set(body)
        body_tail = body[-1]
        neck      = self._behind(body)

        ml_dirs = self._ml_preferred_dirs(head, body, target, walkable, board_size)

        # ── 1. Corner override ────────────────────────────────────────────────
        if self._corner_target is not None:
            if head == self._corner_target:
                self._corner_target = None
            else:
                cell, path = self._safe_move_toward(
                    head, self._corner_target,
                    occupied, body_tail, walkable, len(body), neck)
                if cell is not None:
                    self.path, self.danger_mode = path, False
                    self._update_dir(head, cell)
                    return cell

        # ── 2. A* toward target ───────────────────────────────────────────────
        cell, path = self._safe_move_toward(
            head, target, occupied, body_tail, walkable, len(body), neck)
        if cell is not None:
            self.path, self.danger_mode = path, False
            self._update_dir(head, cell)
            return cell

        # ── 3. Tail-chase fallback ────────────────────────────────────────────
        tail_path = astar(head, body_tail, occupied - {head, body_tail}, walkable)
        if tail_path and tail_path[0] != neck:
            self.path, self.danger_mode = tail_path, True
            self._update_dir(head, tail_path[0])
            return tail_path[0]

        # ── 4. Survival: max free space  (ML breaks ties) ────────────────────
        self.path        = []
        self.danger_mode = True
        candidates: list[tuple] = []

        for dr, dc in DIRS:
            nb = (head[0] + dr, head[1] + dc)
            if nb == neck or nb not in walkable:
                continue
            if nb in occupied and nb != body_tail:
                continue
            space   = flood_fill_count(
                nb, (occupied - {body_tail}) - {nb}, walkable)
            ml_rank = ml_dirs.index((dr, dc)) if ml_dirs and (dr, dc) in ml_dirs else 99
            candidates.append((space, ml_rank, nb))

        if candidates:
            candidates.sort(key=lambda x: (-x[0], x[1]))
            best_cell = candidates[0][2]
            self._update_dir(head, best_cell)
            return best_cell

        return None

    def _update_dir(self, head: tuple[int, int], next_cell: tuple[int, int]):
        self._prev_dir = (next_cell[0] - head[0], next_cell[1] - head[1])
