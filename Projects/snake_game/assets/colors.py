"""
Color definitions and theme management for the Snake game.
Supports dark and light modes with adaptive snake coloring.
"""

# ── Dark Mode Palette ────────────────────────────────────────────────────────
DARK = {
    "background":    (10,  12,  20),
    "board":         (18,  22,  36),
    "board_border":  (40,  50,  80),
    "snake_head":    (255, 255, 255),
    "snake_body":    (200, 220, 255),
    "snake_outline": (120, 150, 220),
    "target":        (255,  80,  80),
    "target_glow":   (255, 120, 120),
    "path_trail":    (60, 120, 200),      # faint AI path
    "text":          (220, 230, 255),
    "text_dim":      (100, 120, 160),
    "hud_bg":        (14,  18,  30),
    "countdown":     (255, 200,  60),
    "level_up":      (60, 255, 160),
    "grid":          (22,  28,  45),
    "wall":          (30,  38,  60),
    "mode_btn":      (40,  52,  85),
    "mode_btn_text": (180, 200, 255),
}

# ── Light Mode Palette ───────────────────────────────────────────────────────
LIGHT = {
    "background":    (240, 242, 250),
    "board":         (255, 255, 255),
    "board_border":  (180, 190, 215),
    "snake_head":    (10,  10,  10),
    "snake_body":    (40,  50,  80),
    "snake_outline": (100, 120, 180),
    "target":        (220,  40,  40),
    "target_glow":   (255,  80,  80),
    "path_trail":    (100, 160, 255),
    "text":          (20,  30,  60),
    "text_dim":      (120, 130, 160),
    "hud_bg":        (225, 228, 242),
    "countdown":     (200, 120,   0),
    "level_up":      (0,  160,  80),
    "grid":          (230, 232, 245),
    "wall":          (200, 205, 225),
    "mode_btn":      (200, 210, 235),
    "mode_btn_text": (30,  40,  80),
}


def get_theme(dark_mode: bool) -> dict:
    """Return the active color theme."""
    return DARK if dark_mode else LIGHT
