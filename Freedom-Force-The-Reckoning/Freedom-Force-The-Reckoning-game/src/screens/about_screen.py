"""
screens/about_screen.py — Freedom Force: The Reckoning
=======================================================
About screen shown when player presses A on the title screen.

Returns:
    "back"  — ESC / B pressed  → return to title
    None    — still showing
"""

import pygame
import math

BG      = (6,   8,  22)
STARS   = (180, 200, 255)
GOLD    = (255, 215,  50)
ORANGE  = (255, 160,  40)
WHITE   = (255, 255, 255)
CYAN    = ( 80, 220, 255)
GREEN   = ( 80, 220, 110)
LBLUE   = (140, 190, 255)
PANEL   = ( 12,  16,  44, 220)
BORDER  = ( 70, 110, 200, 220)

DEV = {
    "name":     "Sahar Yaccov",
    "email":    "saharyaccov@gmail.com",
    "github":   "https://github.com/saharYaccov",
    "linkedin": "https://www.linkedin.com/in/sahar-haim-yaccov/",
    "skills":   ["Data Science", "Data Analysis", "Business Intelligence (BI)" , "Machine Learning" ],
    "seeking": "Currently seeking job opportunities in Data Science, Data Analysis, Business Intelligence (BI), as well as Machine Learning and data-driven projects."
}


class AboutScreen:

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock  = clock
        self.W, self.H = screen.get_size()
        self.tick   = 0
        self.result = None

        pygame.font.init()
        self.f_title = pygame.font.SysFont("arialblack", 46, bold=True)
        self.f_name  = pygame.font.SysFont("arialblack", 30, bold=True)
        self.f_label = pygame.font.SysFont("consolas",   18, bold=True)
        self.f_value = pygame.font.SysFont("consolas",   18)
        self.f_skill = pygame.font.SysFont("consolas",   17, bold=True)
        self.f_seek  = pygame.font.SysFont("consolas",   17)
        self.f_hint  = pygame.font.SysFont("consolas",   20, bold=True)

        import random
        rng = random.Random(77)
        self.stars = [
            (rng.randint(0, self.W), rng.randint(0, self.H),
             rng.choice([1, 1, 2]), rng.random())
            for _ in range(130)
        ]

    def update(self):
        self.tick += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_b,
                                 pygame.K_BACKSPACE, pygame.K_RETURN,
                                 pygame.K_SPACE):
                    self.result = "back"
        return self.result

    def draw(self):
        self.screen.fill(BG)
        self._draw_stars()
        self._draw_panel()
        self._draw_hint()
        pygame.display.flip()
        self.clock.tick(60)

    def _draw_stars(self):
        t = self.tick
        for x, y, size, phase in self.stars:
            a   = int(90 + 80 * math.sin(t * 0.04 + phase * 6.28))
            col = tuple(min(255, int(c * a / 255)) for c in STARS)
            pygame.draw.circle(self.screen, col, (x, y), size)

    def _draw_panel(self):
        cx = self.W // 2
        t  = self.tick

        ratio = (math.sin(t * 0.035) + 1) / 2
        tc = (
            int(GOLD[0] + ratio * (ORANGE[0] - GOLD[0])),
            int(GOLD[1] + ratio * (ORANGE[1] - GOLD[1])),
            int(GOLD[2] + ratio * (ORANGE[2] - GOLD[2])),
        )
        title = self.f_title.render("About the Developer", True, tc)
        self.screen.blit(title, title.get_rect(center=(cx, 62)))
        pygame.draw.line(self.screen, (50, 80, 170), (cx - 340, 98), (cx + 340, 98), 2)

        pw, ph = 720, 470
        px = cx - pw // 2
        py = 112
        card = pygame.Surface((pw, ph), pygame.SRCALPHA)
        card.fill(PANEL)
        pygame.draw.rect(card, BORDER, (0, 0, pw, ph), 2, border_radius=16)
        self.screen.blit(card, (px, py))

        name_s = self.f_name.render(DEV["name"], True, GOLD)
        self.screen.blit(name_s, name_s.get_rect(center=(cx, py + 38)))
        pygame.draw.line(self.screen, (45, 70, 130),
                         (px + 30, py + 66), (px + pw - 30, py + 66), 1)

        iy = py + 84
        for label, value, vcol in [
            ("Email",    DEV["email"],    CYAN),
            ("GitHub",   DEV["github"],   LBLUE),
            ("LinkedIn", DEV["linkedin"], LBLUE),
        ]:
            lbl_s = self.f_label.render(f"{label}:", True, WHITE)
            val_s = self.f_value.render(value,        True, vcol)
            total = lbl_s.get_width() + 12 + val_s.get_width()
            sx    = cx - total // 2
            self.screen.blit(lbl_s, (sx, iy))
            self.screen.blit(val_s, (sx + lbl_s.get_width() + 12, iy))
            iy += 34

        pygame.draw.line(self.screen, (45, 70, 130),
                         (px + 30, iy + 6), (px + pw - 30, iy + 6), 1)
        iy += 22

        # skills chips — 2 per row, custom order
        skills_order = [
            "Data Science", "Machine Learning",
            "Data Analysis", "Python",
            "Business Intelligence (BI)", "SQL"
        ]

        lbl_s = self.f_label.render("Skills:", True, WHITE)
        self.screen.blit(lbl_s, (cx - lbl_s.get_width() // 2, iy))
        iy += 28  # רווח מעל השורה הראשונה של הסקילים

        chip_per_row = 2
        chip_x_start = cx - 200  # adjust to center
        chip_x = chip_x_start
        chip_y = iy
        count = 0

        for skill in skills_order:
            chip_s = self.f_skill.render(skill, True, BG)
            cw = chip_s.get_width() + 20
            ch = chip_s.get_height() + 8
            bg = pygame.Surface((cw, ch), pygame.SRCALPHA)
            bg.fill((70, 180, 255, 210))
            pygame.draw.rect(bg, (160, 230, 255, 230), (0, 0, cw, ch), 1, border_radius=8)
            self.screen.blit(bg, (chip_x, chip_y))
            self.screen.blit(chip_s, (chip_x + 10, chip_y + 2))

            count += 1
            if count % chip_per_row == 0:
                chip_x = chip_x_start
                chip_y += ch + 10  # רווח בין שורות
            else:
                chip_x += cw + 10

        iy = chip_y + ch + 10  # עדכון iy לשורה שמתחת ל-skills

        # seeking — word-wrap
        words, line, lines = DEV["seeking"].split(), "", []
        for w in words:
            test = (line + " " + w).strip()
            if self.f_seek.size(test)[0] <= pw - 60:
                line = test
            else:
                lines.append(line); line = w
        if line:
            lines.append(line)
        for ln in lines:
            s = self.f_seek.render(ln, True, GREEN)
            self.screen.blit(s, s.get_rect(center=(cx, iy)))
            iy += 26

    def _draw_hint(self):
        t     = self.tick
        pulse = abs(math.sin(t * 0.05))
        grey  = int(100 + pulse * 140)
        hint  = self.f_hint.render(
            "[ ESC / B / ENTER ]  —  Back to Main Menu", True, (grey, grey, grey))
        self.screen.blit(hint, hint.get_rect(center=(self.W // 2, self.H - 36)))
