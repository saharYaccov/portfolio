"""
screens/title_screen.py
=======================
Opening screen for Freedom Force: The Reckoning.

Returns one of:
    "start"   – Space pressed  → start game
    "rules"   – R pressed      → go to rules screen
    None      – still on screen
"""

import pygame
import math
import os
from pathlib import Path


# ── palette ────────────────────────────────────────────────────────────────
C_BG        = (10,  12,  30)
C_STARS     = (200, 210, 255)
C_TITLE1    = (255, 220,  50)
C_TITLE2    = (255, 140,   0)
C_SUBTITLE  = (180, 230, 255)
C_HINT_KEY  = (255, 220,  50)
C_HINT_TEXT = (200, 200, 200)
C_FLASH     = (255, 255, 255)
C_DEVICE_BG = (25,  30,  60)
C_DEVICE_BD = (80, 120, 200)
C_DEVICE_HI = (255, 220,  50)
C_DEVICE_TX = (220, 220, 220)
C_PANEL_BG  = (15,  18,  45, 210)


class TitleScreen:
    """
    Handles the title / splash screen.

    Usage:
        ts = TitleScreen(screen, clock)
        while True:
            result = ts.update()
            ts.draw()
            if result:          # "start" or "rules"
                break
    """

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self.screen = screen
        self.clock  = clock
        self.W, self.H = screen.get_size()
        self.tick   = 0          # frame counter for animations
        self.result = None       # "start" | "rules" | None

        # device selection state
        # None = asking, "pc" = computer, "mobile" = phone
        self.device: str | None = None

        # difficulty selection state: "easy" | "middle" | "hard"
        self.difficulty: str = "easy"

        # music mute toggle (handled via pygame.mixer.music)
        self.music_muted: bool = False

        self._init_fonts()
        self._init_stars()
        self._build_device_rects()
        self._build_difficulty_rects()
        self._load_background()

    # ── init helpers ───────────────────────────────────────────────────────
    def _init_fonts(self):
        pygame.font.init()
        self.f_title    = pygame.font.SysFont("arialblack",          72, bold=True)
        self.f_subtitle = pygame.font.SysFont("couriernew",      22, bold=True)
        self.f_hint     = pygame.font.SysFont("couriernew",      26, bold=True)
        self.f_device   = pygame.font.SysFont("segoeui",         24, bold=True)
        self.f_device_s = pygame.font.SysFont("segoeui",         18)

    def _init_stars(self):
        import random
        rng = random.Random(42)
        self.stars = [
            (rng.randint(0, self.W), rng.randint(0, self.H),
             rng.choice([1, 1, 1, 2]), rng.random())
            for _ in range(160)
        ]

    def _build_device_rects(self):
        bw, bh = 200, 70
        cx = self.W // 2
        gap = 30
        self.rect_pc     = pygame.Rect(cx - bw - gap//2, self.H//2 + 30, bw, bh)
        self.rect_mobile = pygame.Rect(cx + gap//2,       self.H//2 + 30, bw, bh)

    def _build_difficulty_rects(self):
        bw, bh = 180, 54
        cx = self.W // 2
        base_y = self.H // 2 + 150
        gap = 20
        self.rect_easy   = pygame.Rect(cx - bw - gap, base_y, bw, bh)
        self.rect_mid    = pygame.Rect(cx - bw//2,    base_y, bw, bh)
        self.rect_hard   = pygame.Rect(cx + gap,      base_y, bw, bh)

        # music button (top-right)
        self.rect_music = pygame.Rect(self.W - 190, 20, 170, 40)

    def _load_background(self):
        """Load full-screen background image from assets, if available."""
        try:
            base_dir = Path(__file__).resolve().parents[2]
            assets_dir = base_dir / "assets"
            if not assets_dir.is_dir():
                self.bg_image = None
                return
            # look for a reasonable background file
            candidates = [
                "background.png",
                "background.jpg",
                "background.jpeg",
            ]
            img_path = None
            for name in candidates:
                p = assets_dir / name
                if p.is_file():
                    img_path = p
                    break
            if img_path is None:
                self.bg_image = None
                return
            img = pygame.image.load(str(img_path)).convert()
            self.bg_image = pygame.transform.scale(img, (self.W, self.H))
            print(f"[title] background image loaded from {img_path}")
        except Exception as e:
            print(f"[title] failed to load background: {e}")
            self.bg_image = None

    # ── public API ─────────────────────────────────────────────────────────
    def update(self) -> str | None:
        """Call once per frame. Returns "start", "rules", or None."""
        self.tick += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit

            # music toggle is always available on title screen
            self._handle_music_events(event)

            # ── device selection phase ────────────────────────────────────
            if self.device is None:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.rect_pc.collidepoint(event.pos):
                        self.device = "pc"
                    elif self.rect_mobile.collidepoint(event.pos):
                        self.device = "mobile"
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_1, pygame.K_KP1):
                        self.device = "pc"
                    elif event.key in (pygame.K_2, pygame.K_KP2):
                        self.device = "mobile"
                continue  # don't process game / difficulty keys until device chosen

            # ── main title phase ──────────────────────────────────────────
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.result = "start"
                elif event.key in (pygame.K_r, pygame.K_F1):
                    self.result = "rules"
                elif event.key == pygame.K_a:
                    self.result = "about"

                # difficulty shortcuts: E / M / H
                if event.key == pygame.K_e:
                    self.difficulty = "easy"
                elif event.key == pygame.K_m:
                    self.difficulty = "middle"
                elif event.key == pygame.K_h:
                    self.difficulty = "hard"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if self.rect_easy.collidepoint((mx, my)):
                    self.difficulty = "easy"
                elif self.rect_mid.collidepoint((mx, my)):
                    self.difficulty = "middle"
                elif self.rect_hard.collidepoint((mx, my)):
                    self.difficulty = "hard"

        return self.result

    def get_device(self) -> str:
        """Returns "pc" or "mobile" (defaults to "pc" if not chosen yet)."""
        return self.device or "pc"

    def get_difficulty(self) -> str:
        """Returns chosen difficulty: 'easy' | 'middle' | 'hard' (default easy)."""
        return self.difficulty or "easy"

    def draw(self):
        # background image (if available) + animated stars overlay
        if getattr(self, "bg_image", None) is not None:
            self.screen.blit(self.bg_image, (0, 0))
            # subtle darkening for text readability
            dim = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
            dim.fill((0, 0, 0, 90))
            self.screen.blit(dim, (0, 0))
        else:
            self.screen.fill(C_BG)

        self._draw_stars()

        if self.device is None:
            self._draw_device_prompt()
        else:
            self._draw_title()
            self._draw_hints()
            self._draw_difficulty_panel()

        self._draw_music_button()

        pygame.display.flip()
        self.clock.tick(60)

    # ── drawing helpers ────────────────────────────────────────────────────
    def _draw_stars(self):
        t = self.tick
        for x, y, size, phase in self.stars:
            alpha = int(140 + 115 * math.sin(t * 0.04 + phase * 6.28))
            col   = tuple(min(255, int(c * alpha / 255)) for c in C_STARS)
            pygame.draw.circle(self.screen, col, (x, y), size)

    def _draw_title(self):
        t   = self.tick
        cx  = self.W // 2

        # shadow + title text with colour shift
        ratio  = (math.sin(t * 0.03) + 1) / 2
        r      = int(C_TITLE1[0] + ratio * (C_TITLE2[0] - C_TITLE1[0]))
        g      = int(C_TITLE1[1] + ratio * (C_TITLE2[1] - C_TITLE1[1]))
        b      = int(C_TITLE1[2] + ratio * (C_TITLE2[2] - C_TITLE1[2]))
        col    = (r, g, b)

        line1  = self.f_title.render("F R E E D O M  F O R C E", True, col)
        line2  = self.f_title.render("T H E  R E C K O N I N G", True, col)

        # drop-shadow
        shadow_col = (3, 3, 0)
        s1 = self.f_title.render("FREEDOM FORCE", True, shadow_col)
        s2 = self.f_title.render("THE RECKONING", True, shadow_col)
        self.screen.blit(s1, s1.get_rect(center=(cx+4, self.H//4 + 4)))
        self.screen.blit(s2, s2.get_rect(center=(cx+4, self.H//4 + 80 + 4)))
        self.screen.blit(line1, line1.get_rect(center=(cx, self.H // 4)))
        self.screen.blit(line2, line2.get_rect(center=(cx, self.H // 4 + 80)))

        # subtitle
        sub = self.f_subtitle.render("— Side-scroll action platformer —", True, C_SUBTITLE)
        self.screen.blit(sub, sub.get_rect(center=(cx, self.H//4 + 155)))

    def _draw_hints(self):
        cx  = self.W // 2
        t   = self.tick
        mid = self.H // 2 + 30

        # semi-transparent panel
        panel = pygame.Surface((420, 175), pygame.SRCALPHA)
        panel.fill(C_PANEL_BG)
        self.screen.blit(panel, panel.get_rect(center=(cx, mid + 52)))

        # flashing SPACE hint
        flash = abs(math.sin(t * 0.05))
        fc    = tuple(int(a + flash * (b - a)) for a, b in zip(C_HINT_TEXT, C_FLASH))
        self._hint_line("[  SPACE  ]", " — Start Game",      cx, mid,       C_HINT_KEY, fc)
        self._hint_line("[   R     ]", " — Rules / Help",     cx, mid + 46,  C_HINT_KEY, C_HINT_TEXT)
        self._hint_line("[   A     ]", " — About Developer",  cx, mid + 92,  C_HINT_KEY, (160, 240, 180))

        # device badge
        dev_txt = "🖥  PC Mode" if self.device == "pc" else "📱  Mobile Mode"
        dev_surf = self.f_device_s.render(dev_txt, True, (120, 200, 120))
        self.screen.blit(dev_surf, dev_surf.get_rect(center=(cx, mid + 148)))

    def _hint_line(self, key_txt, desc_txt, cx, y, key_col, desc_col):
        key_surf  = self.f_hint.render(key_txt,  True, key_col)
        desc_surf = self.f_hint.render(desc_txt, True, desc_col)
        total_w   = key_surf.get_width() + desc_surf.get_width()
        x_start   = cx - total_w // 2
        self.screen.blit(key_surf,  (x_start, y))
        self.screen.blit(desc_surf, (x_start + key_surf.get_width(), y))

    def _draw_device_prompt(self):
        cx, cy = self.W // 2, self.H // 2
        t      = self.tick

        # title
        title = self.f_hint.render("Are you playing on PC or Mobile?", True, C_SUBTITLE)
        self.screen.blit(title, title.get_rect(center=(cx, cy - 60)))

        sub = self.f_device_s.render("Choose with mouse click  or  press  1 = PC   2 = Mobile",
                                     True, (150, 150, 180))
        self.screen.blit(sub, sub.get_rect(center=(cx, cy - 20)))

        mouse = pygame.mouse.get_pos()
        for rect, label, icon in [
            (self.rect_pc,     "PC / Computer", "🖥"),
            (self.rect_mobile, "Mobile / Phone", "📱"),
        ]:
            hover = rect.collidepoint(mouse)
            bg    = C_DEVICE_HI if hover else C_DEVICE_BG
            bd    = C_DEVICE_HI if hover else C_DEVICE_BD
            pygame.draw.rect(self.screen, bg, rect, border_radius=12)
            pygame.draw.rect(self.screen, bd, rect, 2, border_radius=12)

            icon_surf  = self.f_device.render(icon,  True, (255,255,255))
            label_surf = self.f_device.render(label, True, C_DEVICE_TX if not hover else (20,20,20))
            self.screen.blit(icon_surf,  icon_surf.get_rect(center=(rect.centerx, rect.centery - 12)))
            self.screen.blit(label_surf, label_surf.get_rect(center=(rect.centerx, rect.centery + 18)))

    def _draw_difficulty_panel(self):
        """Draw difficulty selection buttons under the main hints."""
        cx = self.W // 2

        title = self.f_device_s.render("Choose Difficulty", True, (210, 230, 255))
        self.screen.blit(title, title.get_rect(center=(cx, self.H//2 + 130)))

        def _draw_btn(rect, label, desc, is_active, color_base):
            bg_col = (40, 60, 110) if not is_active else (240, 210, 80)
            bd_col = (100, 140, 220) if not is_active else (160, 120, 40)
            pygame.draw.rect(self.screen, bg_col, rect, border_radius=10)
            pygame.draw.rect(self.screen, bd_col, rect, 2, border_radius=10)
            txt_col = (235, 235, 235) if not is_active else (25, 25, 25)
            label_surf = self.f_device.render(label, True, txt_col)
            desc_surf  = self.f_device_s.render(desc, True, txt_col)
            self.screen.blit(label_surf, label_surf.get_rect(center=(rect.centerx, rect.centery - 6)))
            self.screen.blit(desc_surf,  desc_surf.get_rect(center=(rect.centerx, rect.centery + 14)))

        _draw_btn(
            self.rect_easy,
            "EASY",
            "4 shooters",
            self.difficulty == "easy",
            (120, 200, 120),
        )
        _draw_btn(
            self.rect_mid,
            "MIDDLE",
            "8 shooters",
            self.difficulty == "middle",
            (240, 200, 120),
        )
        _draw_btn(
            self.rect_hard,
            "HARD",
            "12 shooters, faster fire",
            self.difficulty == "hard",
            (240, 140, 140),
        )

    def _handle_music_events(self, event):
        """Handle mute/unmute toggle from mouse or keyboard (title screen only)."""
        if not pygame.mixer.get_init():
            return

        toggle = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            toggle = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect_music.collidepoint(event.pos):
                toggle = True

        if not toggle:
            return

        self.music_muted = not self.music_muted
        try:
            if self.music_muted:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
        except Exception:
            # fail silently if mixer/music not ready
            pass

    def _draw_music_button(self):
        """Small mute/unmute toggle button in the top-right corner."""
        label = "Music: OFF (M)" if self.music_muted else "Music: ON (M)"
        bg    = (40, 40, 70) if not self.music_muted else (90, 30, 30)
        bd    = (120, 160, 255) if not self.music_muted else (220, 120, 120)
        pygame.draw.rect(self.screen, bg, self.rect_music, border_radius=10)
        pygame.draw.rect(self.screen, bd, self.rect_music, 2, border_radius=10)
        surf = self.f_device_s.render(label, True, (230, 230, 230))
        self.screen.blit(surf, surf.get_rect(center=self.rect_music.center))
