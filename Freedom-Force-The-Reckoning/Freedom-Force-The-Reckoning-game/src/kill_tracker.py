"""
kill_tracker.py — Freedom Force: The Reckoning
===============================================
Tracks every enemy elimination and keeps the window title bar
always up-to-date with the last killed enemy name.

Usage:
    from kill_tracker import KillTracker
    kt = KillTracker()

    # when an enemy dies:
    kt.record_kill("Enemy Image 3")

    # when a bomb is activated:
    kt.record_bomb("Halo Bomb")

    # each frame, call to get the current HUD text:
    last = kt.last_kill      # e.g. "Enemy Image 3"
    count = kt.total_kills
"""

import pygame


GAME_TITLE = "Freedom Force – The Reckoning"


class KillTracker:
    """
    Single source of truth for kill events.
    - Updates pygame window caption immediately on every kill/bomb.
    - Stores the last killed enemy name for permanent HUD display.
    - Keeps a running total.
    """

    def __init__(self):
        self.last_kill:   str = ""      # name of last eliminated enemy
        self.total_kills: int = 0       # running total this session
        self._last_bomb:  str = ""      # name of last activated bomb

    # ── public API ──────────────────────────────────────────────────────────

    def record_kill(self, enemy_name: str) -> None:
        """Call whenever an enemy is destroyed. Updates title bar immediately."""
        self.last_kill    = enemy_name
        self.total_kills += 1
        self._refresh_caption()

    def record_bomb(self, bomb_name: str) -> None:
        """Call when player activates a bomb. Updates title bar immediately."""
        self._last_bomb = bomb_name
        pygame.display.set_caption(f"{bomb_name} Activated – {GAME_TITLE}")

    def reset(self) -> None:
        """Reset for a new game session."""
        self.last_kill   = ""
        self.total_kills = 0
        self._last_bomb  = ""
        pygame.display.set_caption(GAME_TITLE)

    # ── internal ────────────────────────────────────────────────────────────

    def _refresh_caption(self) -> None:
        """Set caption to show last killed enemy (bomb caption takes priority briefly)."""
        if self.last_kill:
            pygame.display.set_caption(
                f"Eliminated: {self.last_kill}  |  Kills: {self.total_kills}  –  {GAME_TITLE}"
            )
