"""
screens/rules_screen.py  — Fixed version
- Hebrew RTL rendering (manual bidi reversal + per-word layout)
- Larger, cleaner fonts — no overlapping
- Fixed color bug (all values clamped 0-255)
- Language toggle with [ L ] key or mouse
- Backspace / ESC / Back button → return "back"
"""

import pygame
import math
import unicodedata

# ── palette ────────────────────────────────────────────────────────────────
C_BG        = (10,  12,  30)
C_PANEL     = (18,  22,  52)
C_BORDER    = (80, 120, 200)
C_TITLE     = (255, 220,  50)
C_SECTION   = (100, 200, 255)
C_KEY_BG    = (35,  40,  80)
C_KEY_BD    = (120, 160, 220)
C_KEY_TX    = (255, 220,  50)
C_DESC_TX   = (210, 215, 235)
C_NOTE_TX   = (170, 210, 170)
C_NOTE_STAR = (255, 180,  50)
C_BACK_BG   = (35,  40,  80)
C_BACK_BD   = (80, 120, 200)
C_BACK_HI   = (255, 220,  50)
C_LANG_BG   = (25,  30,  60)
C_LANG_BD   = (80, 120, 200)
C_LANG_HI   = (255, 220,  50)
C_LANG_TX   = (200, 200, 200)


# ── RTL helper ─────────────────────────────────────────────────────────────
def _is_hebrew(ch):
    try:
        name = unicodedata.name(ch, '')
        return 'HEBREW' in name
    except Exception:
        return False

def _fix_rtl(text: str) -> str:
    """
    Reverse Hebrew text so pygame renders it correctly left-to-right visually.
    Keeps Latin/digit segments in their original order within the reversal.
    """
    if not any(_is_hebrew(c) for c in text):
        return text

    # Split into Hebrew and non-Hebrew segments, reverse the whole list
    segments = []
    current  = ''
    current_is_heb = None
    for ch in text:
        is_heb = _is_hebrew(ch) or ch in ' –-/().,!?:0123456789'
        if current_is_heb is None:
            current_is_heb = is_heb
        if is_heb == current_is_heb:
            current += ch
        else:
            segments.append(current)
            current = ch
            current_is_heb = is_heb
    if current:
        segments.append(current)

    segments.reverse()
    return ''.join(segments)


def _wrap_rtl(font, text: str, max_w: int):
    """
    Word-wrap a Hebrew string. Returns list of display-ready lines.
    Each line is already RTL-fixed and fits within max_w pixels.
    """
    words = text.split()
    lines = []
    line  = []
    for word in words:
        test = ' '.join(line + [word])
        if font.size(test)[0] <= max_w:
            line.append(word)
        else:
            if line:
                lines.append(_fix_rtl(' '.join(line)))
            line = [word]
    if line:
        lines.append(_fix_rtl(' '.join(line)))
    return lines


def _wrap_ltr(font, text: str, max_w: int):
    words = text.split()
    lines = []
    line  = []
    for word in words:
        test = ' '.join(line + [word])
        if font.size(test)[0] <= max_w:
            line.append(word)
        else:
            if line:
                lines.append(' '.join(line))
            line = [word]
    if line:
        lines.append(' '.join(line))
    return lines


# ── content ────────────────────────────────────────────────────────────────
CONTENT = {
    "en": {
        "title": "Keyboard Controls – Freedom Force: The Reckoning",
        "sections": [
            ("Movement", [
                ("A",     "Move left"),
                ("D",     "Move right"),
                ("Space", "Jump"),
            ]),
            ("Combat", [
                ("L",     "Fire red laser  (damages enemies and boss)"),
            ]),
            ("Special / Abilities", [
                ("O- char",     "Anti-bomb shield  (boss nuclear attack window)"),
                ("1",     "B2 Bomb – destroys all enemies in current stage"),
                ("2",     "Arrow Bomb – destroys enemies within 3-tile radius"),
                ("3",     "Halo Bomb – destroys half the ground layer"),
            ]),
            ("System", [
                ("P",     "Pause / Resume"),
                ("R",     "Restart  (Game Over screen only)"),
                ("Enter", "Start game  (title screen)"),
            ]),
        ],
        "notes": [
            "Anti-bomb shield (O) uses one anti-bomb item per activation. Collect orbs across stages 1-5 (6 total). Need 5 minimum to survive the boss fight.",
            "B2 Bomb: 3 total across the whole game.",
            "Arrow Bomb: 20 total across stages 1-5.",
            "Halo Bomb: 2 total across the whole game.",
            "Trump transformation (golden orb pickup) lasts 20 seconds — grants touch immunity. Activates automatically on pickup.",
        ],
        "back":   "Back to Title",
        "lang_switch": "Switch to Hebrew",
        "notes_title": "Notes",
    },
    "he": {
        "title": "בקרות מקלדת – כוח החירות: יום הדין"[::-1],
        "sections": [
            ("תנועה"[::-1], [
                ("A",     "תנועה שמאלה"[::-1]),
                ("D",     "תנועה ימינה"[::-1]),
                ("Space", "קפיצה"[::-1]),
            ]),
            ("לחימה"[::-1], [
                ("L",     "ירי לייזר אדום – פוגע באויבים ובבוס"[::-1]),
            ]),
            ("יכולות מיוחדות"[::-1], [
                ("O- char",     "מגן אנטי-פצצה – בחלון ההתקפה הגרעינית של הבוס"[::-1]),
                ("1", _fix_rtl("פצצת מפציץ אמריקאי – פצצת מטוס אמריקאית, הורסת את כל האויבים בשלב הנוכחי")[::-1]),
                ("2", _fix_rtl("פצצת חץ – פצצת מטוס ישראלית, פוגעת באויבים בטווח 3 אריחים")[::-1]),
                ("3", _fix_rtl("פצצת הילה – פצצת חודר בונקרים, הורסת מחצית משכבת הקרקע")[::-1]),
            ]),
            ("מערכת"[::-1], [
                ("P",     "השהה / המשך"[::-1]),
                ("R",     "הפעל מחדש – רק במסך Game Over"[::-1]),
                ("Enter", "התחל משחק – מסך כותרת"[::-1]),
            ]),
        ],
        "notes": [
            "מגן אנטי-פצצה גרעינית צורך פריט אחד בכל שימוש. אסוף אנטי-פצצות גרעין בשלבים. צריך לפחות 5 כדי לשרוד את הבוס."[::-1],
            "טרנספורמציית טראמפ - כדור זהב, נמשכת כ-חמש שניות ומעניקה חסינות למגע אויב. מופעלת אוטומטית."[::-1],
        ],
        "back":   "חזרה לתפריט"[::-1],
        "lang_switch": "Switch to English",
        "notes_title": "הערות"[::-1],
    },
}


class RulesScreen:
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self.screen = screen
        self.clock  = clock
        self.W, self.H = screen.get_size()
        self.lang   = None
        self.scroll = 0
        self.result = None
        self.tick   = 0
        self._total_h = self.H * 2
        self._lang_toggle_rect = pygame.Rect(0, 0, 1, 1)
        self._back_btn_rect    = pygame.Rect(0, 0, 1, 1)
        self._init_fonts()
        self._build_lang_rects()

    # ── fonts ──────────────────────────────────────────────────────────────
    def _init_fonts(self):
        pygame.font.init()
        # Use a font that supports Hebrew — try several fallbacks
        hebrew_candidates = [
            "Arial", "arialbd", "tahoma", "David",
            "FreeSans", "DejaVuSans", "NotoSans",
        ]
        heb_font = None
        for name in hebrew_candidates:
            try:
                f = pygame.font.SysFont(name, 20)
                # test Hebrew render
                f.render("שלום", True, (255,255,255))
                heb_font = name
                break
            except Exception:
                continue

        base = heb_font or "segoeui"

        self.f_title   = pygame.font.SysFont(base, 28, bold=True)
        self.f_section = pygame.font.SysFont(base, 22, bold=True)
        self.f_key     = pygame.font.SysFont("couriernew", 18, bold=True)
        self.f_desc    = pygame.font.SysFont(base, 18)
        self.f_note    = pygame.font.SysFont(base, 16)
        self.f_back    = pygame.font.SysFont(base, 20, bold=True)
        self.f_lang    = pygame.font.SysFont(base, 22, bold=True)

    # ── rects ──────────────────────────────────────────────────────────────
    def _build_lang_rects(self):
        bw, bh = 190, 58
        cx = self.W // 2
        self.rect_en = pygame.Rect(cx - bw - 20, self.H//2 + 10, bw, bh)
        self.rect_he = pygame.Rect(cx + 20,       self.H//2 + 10, bw, bh)

    # ── public API ─────────────────────────────────────────────────────────
    def update(self):
        self.tick += 1
        max_scroll = max(0, self._total_h - self.H + 60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit

            if self.lang is None:
                # language selection
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.rect_en.collidepoint(event.pos):
                        self.lang = "en"; self.scroll = 0
                    elif self.rect_he.collidepoint(event.pos):
                        self.lang = "he"; self.scroll = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.lang = "en"; self.scroll = 0
                    elif event.key == pygame.K_h:
                        self.lang = "he"; self.scroll = 0
                    elif event.key in (pygame.K_BACKSPACE, pygame.K_ESCAPE):
                        self.result = "back"
                continue

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_BACKSPACE, pygame.K_ESCAPE):
                    self.result = "back"
                elif event.key == pygame.K_DOWN:
                    self.scroll = min(self.scroll + 35, max_scroll)
                elif event.key == pygame.K_UP:
                    self.scroll = max(self.scroll - 35, 0)
                elif event.key == pygame.K_l:
                    self.lang = "he" if self.lang == "en" else "en"
                    self.scroll = 0

            if event.type == pygame.MOUSEWHEEL:
                self.scroll = max(0, min(self.scroll - event.y * 30, max_scroll))

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self._back_btn_rect.collidepoint(event.pos):
                    self.result = "back"
                if self._lang_toggle_rect.collidepoint(event.pos):
                    self.lang = "he" if self.lang == "en" else "en"
                    self.scroll = 0

        return self.result

    def draw(self):
        self.screen.fill(C_BG)
        self._draw_stars()
        if self.lang is None:
            self._draw_lang_prompt()
        else:
            self._draw_content()
        pygame.display.flip()
        self.clock.tick(60)

    # ── content ────────────────────────────────────────────────────────────
    def _draw_content(self):
        data   = CONTENT[self.lang]
        is_rtl = (self.lang == "he")
        pad    = 50
        cw     = self.W - pad * 2
        y      = 24 - self.scroll

        # title
        title_lines = _wrap_rtl(self.f_title, data["title"], cw) if is_rtl \
                      else _wrap_ltr(self.f_title, data["title"], cw)
        for line in title_lines:
            s = self.f_title.render(line, True, C_TITLE)
            x = self.W - pad - s.get_width() if is_rtl else pad
            self.screen.blit(s, (x, y))
            y += s.get_height() + 4
        y += 14

        # sections
        for sec_name, rows in data["sections"]:
            y = self._draw_section(sec_name, rows, pad, y, cw, is_rtl)
            y += 8

        # notes header
        y += 4
        nh = self.f_section.render(data["notes_title"], True, C_SECTION)
        nx = self.W - pad - nh.get_width() if is_rtl else pad
        self.screen.blit(nh, (nx, y))
        pygame.draw.line(self.screen, C_BORDER, (pad, y + nh.get_height()),
                         (self.W - pad, y + nh.get_height()), 1)
        y += nh.get_height() + 10

        # notes
        for note in data["notes"]:
            y = self._draw_note(note, pad, y, cw, is_rtl)
            y += 6

        y += 18

        # language toggle button
        tg_label = data["lang_switch"]
        tg_surf  = self.f_back.render(f"[ L ]  {tg_label}", True, (120, 200, 255))
        tg_x     = self.W - pad - tg_surf.get_width() if is_rtl else pad
        tg_rect  = tg_surf.get_rect(topleft=(tg_x, y))
        self.screen.blit(tg_surf, tg_rect)
        self._lang_toggle_rect = tg_rect
        y += tg_rect.height + 14

        # back button
        self._draw_back_btn(y, data["back"])
        y += 54

        self._total_h = y + self.scroll

        # scroll hint
        max_s = max(0, self._total_h - self.H + 60)
        if max_s > 0:
            hint = self.f_note.render("▲ ▼  Scroll  |  Mouse wheel", True, (90, 90, 130))
            self.screen.blit(hint, hint.get_rect(centerx=self.W//2, bottom=self.H - 4))

    # ── section ────────────────────────────────────────────────────────────
    def _draw_section(self, name, rows, x, y, cw, is_rtl):
        # header
        s = self.f_section.render(_fix_rtl(name) if is_rtl else name, True, C_SECTION)
        sx = self.W - x - s.get_width() if is_rtl else x
        self.screen.blit(s, (sx, y))
        pygame.draw.line(self.screen, C_BORDER,
                         (x, y + s.get_height() + 2),
                         (x + cw, y + s.get_height() + 2), 1)
        y += s.get_height() + 10

        key_w  = 100
        row_h  = 38
        desc_x = x + key_w + 12

        for key_txt, desc_txt in rows:
            # key badge (always LTR, monospaced)
            kb = pygame.Rect(x, y + 3, key_w - 6, row_h - 6)
            pygame.draw.rect(self.screen, C_KEY_BG, kb, border_radius=6)
            pygame.draw.rect(self.screen, C_KEY_BD, kb, 1, border_radius=6)
            ks = self.f_key.render(key_txt, True, C_KEY_TX)
            self.screen.blit(ks, ks.get_rect(center=kb.center))

            # description — word-wrap if needed
            desc_max = cw - key_w - 20
            if is_rtl:
                lines = _wrap_rtl(self.f_desc, desc_txt, desc_max)
            else:
                lines = _wrap_ltr(self.f_desc, desc_txt, desc_max)

            dy = y + (row_h - len(lines) * (self.f_desc.get_height() + 2)) // 2
            for line in lines:
                ds = self.f_desc.render(line, True, C_DESC_TX)
                if is_rtl:
                    self.screen.blit(ds, (self.W - x - ds.get_width(), dy))
                else:
                    self.screen.blit(ds, (desc_x, dy))
                dy += self.f_desc.get_height() + 2

            y += max(row_h, len(lines) * (self.f_desc.get_height() + 2) + 8) + 4

        return y

    # ── note ───────────────────────────────────────────────────────────────
    def _draw_note(self, note, x, y, cw, is_rtl):
        star = self.f_note.render("* ", True, C_NOTE_STAR)
        self.screen.blit(star, (x, y))
        indent = x + star.get_width()
        note_w = cw - star.get_width()

        if is_rtl:
            lines = _wrap_rtl(self.f_note, note, note_w)
        else:
            lines = _wrap_ltr(self.f_note, note, note_w)

        lh = self.f_note.get_height() + 3
        for line in lines:
            s = self.f_note.render(line, True, C_NOTE_TX)
            if is_rtl:
                self.screen.blit(s, (self.W - x - s.get_width(), y))
            else:
                self.screen.blit(s, (indent, y))
            y += lh
            indent = x + star.get_width()

        return y

    # ── back button ────────────────────────────────────────────────────────
    def _draw_back_btn(self, y, label):
        bw, bh = 240, 44
        rect   = pygame.Rect(self.W//2 - bw//2, y, bw, bh)
        mouse  = pygame.mouse.get_pos()
        hover  = rect.collidepoint(mouse)
        pygame.draw.rect(self.screen, C_BACK_HI if hover else C_BACK_BG, rect, border_radius=10)
        pygame.draw.rect(self.screen, C_BACK_HI if hover else C_BACK_BD, rect, 2, border_radius=10)
        s  = self.f_back.render(_fix_rtl(label), True, (20,20,20) if hover else C_DESC_TX)
        self.screen.blit(s, s.get_rect(center=rect.center))
        self._back_btn_rect = rect

    # ── language prompt ────────────────────────────────────────────────────
    def _draw_lang_prompt(self):
        cx, cy = self.W // 2, self.H // 2
        q = self.f_lang.render("Choose language / בחר שפה", True, (200, 220, 255))
        self.screen.blit(q, q.get_rect(center=(cx, cy - 60)))

        hint = self.f_note.render(
            "Click a button  or  press  E = English     H = Hebrew",
            True, (130, 130, 160))
        self.screen.blit(hint, hint.get_rect(center=(cx, cy - 22)))

        mouse = pygame.mouse.get_pos()
        for rect, label in [(self.rect_en, "English"), (self.rect_he, "עברית"[::-1])]:
            hover = rect.collidepoint(mouse)
            pygame.draw.rect(self.screen, C_LANG_HI if hover else C_LANG_BG, rect, border_radius=12)
            pygame.draw.rect(self.screen, C_LANG_HI if hover else C_LANG_BD, rect, 2, border_radius=12)
            s = self.f_lang.render(label, True, (20,20,20) if hover else C_LANG_TX)
            self.screen.blit(s, s.get_rect(center=rect.center))

    # ── stars ──────────────────────────────────────────────────────────────
    def _draw_stars(self):
        import random
        rng = random.Random(99)
        for _ in range(100):
            sx = rng.randint(0, self.W)
            sy = rng.randint(0, self.H)
            sz = rng.choice([1, 1, 2])
            phase = rng.random()
            bright = int(80 + 100 * math.sin(self.tick * 0.03 + phase * 6.28))
            bright = max(0, min(255, bright))
            col = (bright, bright, min(255, bright + 30))
            pygame.draw.circle(self.screen, col, (sx, sy), sz)