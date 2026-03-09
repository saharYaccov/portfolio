"""
asset_loader.py
---------------
Handles loading, caching, and fallback generation of all game assets.
Supports dynamic loading of enemy sprites from folders.
"""

import pygame
import os
import random
from pathlib import Path


# ── Player sprite dimensions ──────────────────────────────────────────────────
# Must be smaller than TILE (48 px) so the character fits between platforms.
# Change these two values to resize the player character globally.
PLAYER_W = 36    # pixels wide  (< TILE)
PLAYER_H = 44    # pixels tall  (< TILE * 1.1 for one-tile-gap clearance)

# ── Colour palette used for procedurally-generated placeholder sprites ────────
PLACEHOLDER_COLOURS = {
    "player_bb":     (80,  140, 220),
    "player_trump":  (255, 200,  50),
    "enemy":         (220,  60,  60),
    "boss":          (160,   0, 200),
    "antibomb":      (255,  50,  50),
    "energy_sphere": (100, 255, 180),
    "b2_bomb":       (50,   50,  50),
    "arrow_bomb":    (200, 120,   0),
    "halo_bomb":     (0,   200, 255),
    "door":          (180, 140,  80),
}


def _make_placeholder(width: int, height: int, colour: tuple,
                       label: str = "") -> pygame.Surface:
    """Return a simple coloured rectangle with an optional text label."""
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    surf.fill(colour)
    pygame.draw.rect(surf, (255, 255, 255), surf.get_rect(), 2)
    if label:
        font = pygame.font.SysFont(None, max(12, height // 4))
        text = font.render(label[:8], True, (255, 255, 255))
        surf.blit(text, (4, height // 2 - text.get_height() // 2))
    return surf


def _load_or_placeholder(path: str, width: int, height: int,
                          colour_key: str) -> pygame.Surface:
    """Load an image from *path*; fall back to a coloured placeholder."""
    if os.path.isfile(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, (width, height))
        except Exception:
            pass
    return _make_placeholder(width, height,
                              PLACEHOLDER_COLOURS.get(colour_key, (128, 128, 128)),
                              colour_key)


class AssetLoader:
    """
    Central repository for all game assets.

    Usage
    -----
    loader = AssetLoader(base_dir=".")
    loader.load_all()
    surf = loader.get("player_bb")
    """

    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self._cache: dict[str, pygame.Surface] = {}
        self._enemy_sprites: list[pygame.Surface] = []

    # ── public interface ──────────────────────────────────────────────────────

    def load_all(self) -> None:
        """Pre-load every asset the game needs."""
        self._load_player_sprites()
        self._load_enemy_sprites()
        self._load_boss_sprites()
        self._load_powerup_sprites()
        self._load_ui_sprites()

    def get(self, key: str) -> pygame.Surface:
        """Return the cached surface for *key* (raises KeyError if missing)."""
        return self._cache[key]

    def get_enemy_sprites(self) -> list[pygame.Surface]:
        """Return the list of loaded enemy sprites."""
        return self._enemy_sprites

    def get_random_enemy_sprite(self) -> pygame.Surface:
        """Return one randomly chosen enemy sprite."""
        if not self._enemy_sprites:
            return _make_placeholder(48, 48, PLACEHOLDER_COLOURS["enemy"], "enemy")
        return random.choice(self._enemy_sprites)

    # ── private loaders ───────────────────────────────────────────────────────

    def _cache_surface(self, key: str, surf: pygame.Surface) -> None:
        self._cache[key] = surf

    def _load_player_sprites(self) -> None:
        chars_dir = self.base_dir / "current_ok_boys"
        # Player must be smaller than TILE (48) so it fits between platforms.
        # 36 wide × 44 tall gives comfortable clearance on both axes.
        for state in ("bb", "trump"):
            loaded = False
            for ext in (".png", ".jpg", ".jpeg", ".gif", ".bmp"):
                p = chars_dir / f"{state}{ext}"
                if p.is_file():
                    try:
                        img = pygame.image.load(str(p)).convert_alpha()
                        self._cache_surface(f"player_{state}",
                                            pygame.transform.scale(img, (PLAYER_W, PLAYER_H)))
                        loaded = True
                        break
                    except Exception:
                        pass
            if not loaded:
                self._cache_surface(
                    f"player_{state}",
                    _make_placeholder(PLAYER_W, PLAYER_H,
                                      PLACEHOLDER_COLOURS[f"player_{state}"],
                                      state))

    def _load_enemy_sprites(self) -> None:
        enemy_dir = self.base_dir / "current_enemy"
        sprites: list[pygame.Surface] = []
        self._enemy_names: dict[int, str] = {}   # id(surf) → filename stem
        if enemy_dir.is_dir():
            for fp in sorted(enemy_dir.iterdir()):
                if fp.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif", ".bmp"):
                    try:
                        img  = pygame.image.load(str(fp)).convert_alpha()
                        surf = pygame.transform.scale(img, (48, 48))
                        self._enemy_names[id(surf)] = fp.stem
                        sprites.append(surf)
                    except Exception:
                        pass
        if not sprites:
            surf = _make_placeholder(48, 48, PLACEHOLDER_COLOURS["enemy"], "enemy")
            self._enemy_names[id(surf)] = "enemy"
            sprites.append(surf)
        self._enemy_sprites = sprites

    def get_enemy_sprite_name(self, sprite: "pygame.Surface") -> str:
        return self._enemy_names.get(id(sprite), "enemy")

    def _load_boss_sprites(self) -> None:
        boss_dir = self.base_dir / "final_enemy_iran"
        loaded = False
        print(f"[asset_loader] looking for boss in: {boss_dir}")
        if boss_dir.is_dir():
            for fp in sorted(boss_dir.iterdir()):
                print(f"[asset_loader] found file: {fp}")
                if fp.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif", ".bmp"):
                    try:
                        img = pygame.image.load(str(fp)).convert_alpha()
                        self._cache_surface("boss",
                                            pygame.transform.scale(img, (120, 120)))
                        loaded = True
                        print(f"[asset_loader] boss loaded OK from {fp}")
                        break
                    except Exception as e:
                        print(f"[asset_loader] ERROR loading {fp}: {e}")
        if not loaded:
            print("[asset_loader] boss NOT loaded — using placeholder")
            self._cache_surface("boss",
                                 _make_placeholder(120, 120,
                                                   PLACEHOLDER_COLOURS["boss"],
                                                   "BOSS"))

    def _load_powerup_sprites(self) -> None:
        specs = {
            "antibomb":      (32, 32),
            "energy_sphere": (28, 28),
            "b2_bomb":       (40, 32),
            "arrow_bomb":    (36, 36),
            "halo_bomb":     (36, 36),
        }
        pu_dir = self.base_dir / "assets" / "powerups"
        for key, (w, h) in specs.items():
            p = pu_dir / f"{key}.png"
            self._cache_surface(key, _load_or_placeholder(str(p), w, h, key))

    def _load_ui_sprites(self) -> None:
        ui_dir = self.base_dir / "assets" / "ui"
        door_p = ui_dir / "door.png"
        self._cache_surface("door",
                             _load_or_placeholder(str(door_p), 48, 72, "door"))