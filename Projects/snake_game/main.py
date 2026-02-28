"""
main.py
───────
Entry point for the AI Snake Game.

Run with:
    python main.py

Controls:
    M          – toggle dark / light mode
    Q / Escape – quit
    (game restarts automatically after death or level completion)
"""

from __future__ import annotations

import sys
import time
import math
import pygame

from board  import Board, LEVEL_CONFIG
from snake  import Snake, SnakeAI
from snake.ml_model import SnakeMLModel, extract_features, DIRECTIONS
from utils  import place_target
from assets import get_theme
from assets.aura import get_aura_mode, draw_snake_with_aura, get_snake_level_label

# ── constants ─────────────────────────────────────────────────────────────────
WIN_W, WIN_H    = 900, 700
HUD_H           = 78
BOARD_MARGIN    = 20
COUNTDOWN_SEC   = 0.5
AUTO_NEXT_SEC   = 0.5       # seconds before auto-restart / auto-advance
FPS             = 60
SNAKE_SPEED     = 16
CELL_MIN        = 12
CELL_MAX        = 34

pygame.init()
screen = pygame.display.set_mode((WIN_W, WIN_H), pygame.RESIZABLE)
pygame.display.set_caption("🐍  AI Snake")
clock = pygame.time.Clock()

FONT_HUD    = pygame.font.SysFont("Consolas", 22, bold=True)
FONT_LARGE  = pygame.font.SysFont("Consolas", 48, bold=True)
FONT_MEDIUM = pygame.font.SysFont("Consolas", 28, bold=True)
FONT_SMALL  = pygame.font.SysFont("Consolas", 17)
FONT_BTN    = pygame.font.SysFont("Consolas", 16, bold=True)


class GameState:
    COUNTDOWN = "countdown"
    PLAYING   = "playing"
    GAME_OVER = "game_over"
    LEVEL_UP  = "level_up"


class Game:
    def __init__(self):
        self.dark_mode    = True
        self.level_index  = 0
        self.total_score  = 0
        self.elapsed_time = 0.0
        self.total_rounds = 0    # total steps taken across all games
        self.total_deaths = 0    # total number of deaths
        self._frame = 0          # global frame counter for animation
        # ── ML model — created once, preserved across restarts ────────────────
        self.ml_model = SnakeMLModel()
        trained = self.ml_model.load_and_train()
        if trained:
            print("[ML] Model trained from previous game data.")
        else:
            print("[ML] No previous data — starting without ML assistance.")
        self._init_level()

    # ── level setup ───────────────────────────────────────────────────────────

    def _init_level(self):
        self.board     = Board(self.level_index)
        self.walkable  = set(self.board.walkable_cells())
        self.snake     = Snake(self._board_center())
        self.ai        = SnakeAI(ml_model=self.ml_model)
        self.targets   = self._place_N_targets(3,                                       ######## Target numbers #######
            self.snake.occupied(), list(self.snake.body))
        self.state     = GameState.COUNTDOWN
        self.countdown = COUNTDOWN_SEC
        self._cd_start       = time.time()
        self._state_start    = time.time()   # when current overlay state began
        self._step_acc       = 0.0
        self._blink          = 0.0
        self._game_records: list[dict] = []   # ML: data for current game

    def _board_center(self) -> tuple[int, int]:
        n = self.board.grid_size
        for r in range(n//2, n):
            for c in range(n//2, n):
                if self.board.is_walkable(r, c):
                    return (r, c)
        return list(self.walkable)[0]

    # ── geometry ──────────────────────────────────────────────────────────────

    def _board_rect(self) -> pygame.Rect:
        w, h = screen.get_size()
        return pygame.Rect(BOARD_MARGIN, HUD_H+BOARD_MARGIN,
                           w-2*BOARD_MARGIN, h-HUD_H-2*BOARD_MARGIN)

    def _cell_size(self) -> int:
        rect = self._board_rect()
        n    = self.board.grid_size
        cs   = min(rect.width//n, rect.height//n)
        return max(CELL_MIN, min(CELL_MAX, cs))

    def _cell_origin(self) -> tuple[int, int]:
        rect  = self._board_rect()
        n, cs = self.board.grid_size, self._cell_size()
        return (rect.left+(rect.width-cs*n)//2,
                rect.top +(rect.height-cs*n)//2)

    # ── helpers ───────────────────────────────────────────────────────────────

    def _place_N_targets(
        self,
            N:int,
        occupied: set[tuple[int, int]],
        body:     list[tuple[int, int]],
    ) -> list[tuple[int, int]]:
        result, blocked = [], set(occupied)
        for _ in range(N):
            t = place_target(self.walkable, blocked, body)
            if t:
                result.append(t)
                blocked.add(t)
        return result

    def _advance_level(self):
        self.level_index += 1
        prev = self.total_score
        self._init_level()
        self.total_score = prev

    # ── update ────────────────────────────────────────────────────────────────

    def update(self, dt: float):
        self.elapsed_time += dt
        self._blink = (self._blink + dt*3) % (2*math.pi)

        if self.state == GameState.COUNTDOWN:
            remaining = COUNTDOWN_SEC - (time.time()-self._cd_start)
            self.countdown = max(0, remaining)
            if remaining <= 0:
                self.state = GameState.PLAYING

        elif self.state == GameState.PLAYING:
            self._step_acc += dt
            while self._step_acc >= 1/SNAKE_SPEED:
                self._step_acc -= 1/SNAKE_SPEED
                self._do_snake_step()

        elif self.state == GameState.GAME_OVER:
            # Auto-restart after AUTO_NEXT_SEC seconds
            if time.time() - self._state_start >= AUTO_NEXT_SEC:
                ml      = self.ml_model
                rounds  = self.total_rounds
                deaths  = self.total_deaths
                ml = self.ml_model   # preserve trained model across restart
                self.__init__()
                self.ml_model     = ml
                self.ai.ml_model  = ml
                self.total_rounds = rounds
                self.total_deaths = deaths

        elif self.state == GameState.LEVEL_UP:
            # Auto-advance after AUTO_NEXT_SEC seconds
            if time.time() - self._state_start >= AUTO_NEXT_SEC:
                self._advance_level()

    def _set_state(self, state: str):
        """Change state and record when it started."""
        self.state       = state
        self._state_start = time.time()

    def _save_ml_data_and_retrain(self):
        """Save this game's records to CSV and retrain the model."""
        if self._game_records:
            self.ml_model.save_game_data(self._game_records)
            trained = self.ml_model.load_and_train()
            if trained:
                print(f"[ML] Retrained on {len(self._game_records)} steps from this game.")
            self._game_records = []

    def _do_snake_step(self):
        if not self.targets or not self.snake.alive:
            return

        head    = self.snake.head
        nearest = min(self.targets,
                      key=lambda t: abs(t[0]-head[0])+abs(t[1]-head[1]))

        # ── Survival mode: navigate to nearest free corner ────────────────────
        # When the AI enters danger_mode and no corner is already set,
        # automatically steer toward the nearest walkable corner.
        if self.ai.danger_mode and self.ai._corner_target is None:
            corners = [
                self._find_corner(True,  True),   # top-left
                self._find_corner(True,  False),  # top-right
                self._find_corner(False, True),   # bottom-left
                self._find_corner(False, False),  # bottom-right
            ]
            occupied = self.snake.occupied()
            # Pick the corner that is free (not occupied by body) and nearest
            free_corners = [c for c in corners if c not in occupied]
            if free_corners:
                best = min(free_corners,
                           key=lambda c: abs(c[0]-head[0]) + abs(c[1]-head[1]))
                self.ai.set_corner(best)

        # ── ML: capture state BEFORE move ────────────────────────────────────
        body_snapshot = list(self.snake.body)
        prev_dir      = self.ai._prev_dir

        self.total_rounds += 1   # count every step

        next_cell = self.ai.compute_next_move(
            head=head, target=nearest,
            body=list(self.snake.body), walkable=self.walkable,
            board_size=self.board.grid_size)

        if next_cell is None:
            self.total_deaths += 1
            self._save_ml_data_and_retrain()
            self._set_state(GameState.GAME_OVER)
            return

        # ── ML: record (state → chosen direction) ────────────────────────────
        dr = next_cell[0] - head[0]
        dc = next_cell[1] - head[1]
        label = list(DIRECTIONS.keys()).index((dr, dc)) if (dr, dc) in DIRECTIONS else -1
        if label >= 0:
            features = extract_features(
                head, body_snapshot, nearest,
                self.walkable, prev_dir, self.board.grid_size)
            from snake.ml_model import FEATURE_COLS
            record = {col: features[i] for i, col in enumerate(FEATURE_COLS)}
            record["label"] = label
            self._game_records.append(record)

        ate = next_cell in self.targets
        self.snake.move(next_cell, ate, self.walkable)

        if not self.snake.alive:
            self.total_deaths += 1
            self._save_ml_data_and_retrain()
            self._set_state(GameState.GAME_OVER)
            return

        if ate:
            self.total_score += 1
            if self.snake.length >= self.board.max_len:
                self._set_state(GameState.LEVEL_UP)
                return
            self.targets.remove(next_cell)
            blocked = self.snake.occupied() | set(self.targets)
            t = place_target(self.walkable, blocked, list(self.snake.body))
            if t:
                self.targets.append(t)

    # ── draw ──────────────────────────────────────────────────────────────────

    def draw(self):
        self._frame += 1
        theme  = get_theme(self.dark_mode)
        w, h   = screen.get_size()
        screen.fill(theme["background"])
        self._draw_hud(theme, w)
        self._draw_board(theme)
        self._draw_grid(theme)
        self._draw_path_trail(theme)
        self._draw_target(theme)
        self._draw_snake(theme)
        self._draw_overlay(theme, w, h)
        pygame.display.flip()

    def _draw_hud(self, theme, w):
        pygame.draw.rect(screen, theme["hud_bg"], (0, 0, w, HUD_H))
        pygame.draw.line(screen, theme["board_border"], (0, HUD_H), (w, HUD_H), 2)

        # ── HUD layout: 4 equal columns ───────────────────────────────────────
        # COL_A | COL_B | COL_C | COL_D
        # score   level   stats   NN info
        PAD   = 12
        col_w = w // 4

        # helper: draw dividers between columns
        div_col = theme.get("grid", (60, 60, 60))
        for i in (1, 2, 3):
            pygame.draw.line(screen, div_col,
                             (col_w * i, 6), (col_w * i, HUD_H - 6), 1)

        # ── COL A  (x=0 .. col_w)  — Score & Timer ───────────────────────────
        mins = int(self.elapsed_time) // 60
        secs = int(self.elapsed_time) % 60
        ms   = int((self.elapsed_time % 1) * 100)
        ax   = PAD
        screen.blit(FONT_HUD.render(
            f"⏱  {mins:02d}:{secs:02d}.{ms:02d}", True, theme["text"]), (ax, 8))
        screen.blit(FONT_HUD.render(
            f"🍎  {self.total_score:04d}  |  len {self.snake.length}",
            True, theme["text"]), (ax, 36))

        # ── COL B  (x=col_w .. 2*col_w)  — Level info ────────────────────────
        cfg        = LEVEL_CONFIG[min(self.level_index, len(LEVEL_CONFIG) - 1)]
        bx         = col_w + PAD
        level_surf = FONT_HUD.render(f"{cfg[0]}  –  {cfg[3]}", True, theme["text"])
        goal_surf  = FONT_SMALL.render(f"goal: {self.board.max_len} segs",
                                       True, theme["text_dim"])
        screen.blit(level_surf, (bx, 8))
        screen.blit(goal_surf,  (bx, 38))

        # AI mode warnings (below level name, same column)
        wy = 56
        if self.ai.danger_mode and self.state == GameState.PLAYING:
            screen.blit(FONT_SMALL.render("⚠ SURVIVAL", True, (255, 120, 50)), (bx, wy))
            wy += 18
        if self.ai._corner_target and self.state == GameState.PLAYING:
            screen.blit(FONT_SMALL.render("📍 CORNER", True, (100, 200, 255)), (bx, wy))

        # ── COL C  (x=2*col_w .. 3*col_w)  — Rounds / Deaths / Snake level ───
        cx           = col_w * 2 + PAD
        files_loaded = getattr(self.ml_model, "files_loaded", 0)
        lvl_label, lvl_color = get_snake_level_label(files_loaded)

        rounds_surf = FONT_SMALL.render(
            f"🔄 rounds: {self.total_rounds:,}", True, theme["text"])
        deaths_surf = FONT_SMALL.render(
            f"💀 deaths: {self.total_deaths}", True, (220, 100, 80))
        screen.blit(rounds_surf, (cx, 8))
        screen.blit(deaths_surf, (cx, 28))

        # Snake level badge (inline, bottom of col C)
        badge_text = f"🐍 {lvl_label}  [{files_loaded} files]"
        badge_surf = FONT_SMALL.render(badge_text, True, lvl_color)
        badge_w    = badge_surf.get_width() + 14
        badge_h    = badge_surf.get_height() + 6
        badge_x    = cx
        badge_y    = HUD_H - badge_h - 6

        badge_bg = pygame.Surface((badge_w, badge_h), pygame.SRCALPHA)
        badge_bg.fill((0, 0, 0, 0))
        bg_col = tuple(max(0, c // 5) for c in lvl_color)
        pygame.draw.rect(badge_bg, (*bg_col, 160),
                         pygame.Rect(0, 0, badge_w, badge_h), border_radius=6)
        pulse_v = int(180 + 50 * math.sin(self._blink * 3))
        pygame.draw.rect(badge_bg, (*lvl_color, pulse_v),
                         pygame.Rect(0, 0, badge_w, badge_h), 2, border_radius=6)
        screen.blit(badge_bg, (badge_x, badge_y))
        screen.blit(badge_surf, (badge_x + 7, badge_y + 3))

        # ── COL D  (x=3*col_w .. w)  — NN status, layers, accuracy, dark-mode btn
        dx          = col_w * 3 + PAD
        n_layers    = getattr(self.ml_model, "n_layers", 20)
        accuracy    = getattr(self.ml_model, "accuracy", 0.0)

        if self.ml_model.trained:
            game_no = self.ml_model.game_count
            nn_surf = FONT_SMALL.render(
                f"🧠 NN ON  (game #{game_no})", True, (80, 220, 120))
        else:
            nn_surf = FONT_SMALL.render("🧠 NN learning...", True, (180, 180, 80))

        depth_surf = FONT_SMALL.render(
            f"🌲 Depth: {n_layers}  [+/-]", True, (120, 200, 255))
        acc_color  = (255, 220, 80) if accuracy < 0.7 else (80, 220, 120)
        acc_pct    = f"{accuracy:.1%}" if self.ml_model.trained else "N/A"
        acc_surf   = FONT_SMALL.render(f"🎯 Acc: {acc_pct}", True, acc_color)
        r2         = getattr(self.ml_model, "r2_score", 0.0)
        r2_color   = (255, 220, 80) if r2 < 0.5 else (80, 220, 120)
        r2_txt     = f"{r2:.3f}" if self.ml_model.trained else "N/A"
        r2_surf    = FONT_SMALL.render(f"📐 R²: {r2_txt}", True, r2_color)

        screen.blit(nn_surf,    (dx, 8))
        screen.blit(depth_surf, (dx, 26))
        screen.blit(acc_surf,   (dx, 44))
        screen.blit(r2_surf,    (dx, 62))

        # Dark-mode toggle button — bottom-right of col D, never overlapping text
        btn_w, btn_h = 82, 22
        btn_x = w - btn_w - PAD
        btn_y = HUD_H - btn_h - 5
        btn   = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
        pygame.draw.rect(screen, theme["mode_btn"], btn, border_radius=6)
        label = "☀  Light" if self.dark_mode else "🌙  Dark"
        lbl_s = FONT_BTN.render(label, True, theme["mode_btn_text"])
        screen.blit(lbl_s, lbl_s.get_rect(center=btn.center))
        self._mode_btn_rect = btn


    def _draw_board(self, theme):
        cs    = self._cell_size()
        ox,oy = self._cell_origin()
        n     = self.board.grid_size
        for r in range(n):
            for c in range(n):
                rect = pygame.Rect(ox+c*cs, oy+r*cs, cs, cs)
                col  = theme["board"] if self.board.is_walkable(r,c) else theme["wall"]
                pygame.draw.rect(screen, col, rect)

    def _draw_grid(self, theme):
        cs    = self._cell_size()
        ox,oy = self._cell_origin()
        n     = self.board.grid_size
        for r in range(n):
            for c in range(n):
                if self.board.is_walkable(r,c):
                    pygame.draw.rect(screen, theme["grid"],
                        pygame.Rect(ox+c*cs, oy+r*cs, cs, cs), 1)

    def _draw_path_trail(self, theme):
        cs    = self._cell_size()
        ox,oy = self._cell_origin()

        # ── 1. Body trail (where the snake has been) ──────────────────────────
        # Draw a fading ghost trail behind the snake body (tail → head direction)
        body  = list(self.snake.body)
        total = len(body)
        if total > 1:
            for i, (r, c) in enumerate(reversed(body[1:])):  # skip head, tail first
                t     = i / max(total - 1, 1)
                alpha = max(15, int(70 * (1 - t)))
                surf  = pygame.Surface((cs - 2, cs - 2), pygame.SRCALPHA)
                # Warm amber trail for the body history
                surf.fill((255, 180, 60, alpha))
                screen.blit(surf, (ox + c * cs + 1, oy + r * cs + 1))

        # ── 2. Future path (where AI plans to go) ─────────────────────────────
        if self.ai.path:
            total_p = len(self.ai.path)
            for i, (r, c) in enumerate(self.ai.path):
                alpha = max(30, int(160 * (1 - i / max(total_p, 1))))
                surf  = pygame.Surface((cs - 2, cs - 2), pygame.SRCALPHA)
                surf.fill((*theme["path_trail"], alpha))
                screen.blit(surf, (ox + c * cs + 1, oy + r * cs + 1))

            # Draw small directional arrows along the planned path
            if cs >= 16:
                for i in range(len(self.ai.path) - 1):
                    r0, c0 = self.ai.path[i]
                    r1, c1 = self.ai.path[i + 1]
                    cx0 = ox + c0 * cs + cs // 2
                    cy0 = oy + r0 * cs + cs // 2
                    cx1 = ox + c1 * cs + cs // 2
                    cy1 = oy + r1 * cs + cs // 2
                    # midpoint arrow
                    mx  = (cx0 + cx1) // 2
                    my  = (cy0 + cy1) // 2
                    dr  = r1 - r0
                    dc  = c1 - c0
                    arrow_len = max(3, cs // 5)
                    tip   = (mx + dc * arrow_len,     my + dr * arrow_len)
                    left  = (mx - dr * arrow_len // 2, my + dc * arrow_len // 2)
                    right = (mx + dr * arrow_len // 2, my - dc * arrow_len // 2)
                    fade  = max(20, int(80 * (1 - i / max(total_p, 1))))
                    arrow_col = (*theme["path_trail"], fade)
                    arrow_surf = pygame.Surface((cs * 2, cs * 2), pygame.SRCALPHA)
                    # draw relative to a local surface to support alpha
                    off_x = ox + (min(c0, c1) - 1) * cs
                    off_y = oy + (min(r0, r1) - 1) * cs
                    pts = [
                        (tip[0]   - off_x, tip[1]   - off_y),
                        (left[0]  - off_x, left[1]  - off_y),
                        (right[0] - off_x, right[1] - off_y),
                    ]
                    if all(0 <= p[0] < arrow_surf.get_width() and
                           0 <= p[1] < arrow_surf.get_height() for p in pts):
                        pygame.draw.polygon(arrow_surf, arrow_col, pts)
                        screen.blit(arrow_surf, (off_x, off_y))

    def _draw_target(self, theme):
        if not self.targets:
            return
        cs    = self._cell_size()
        ox,oy = self._cell_origin()
        pulse = 0.6+0.4*math.sin(self._blink)
        for r,c in self.targets:
            size = int(cs*0.55*pulse)
            cx_  = ox+c*cs+cs//2
            cy_  = oy+r*cs+cs//2
            gs   = pygame.Surface((cs,cs), pygame.SRCALPHA)
            pygame.draw.circle(gs, (*theme["target_glow"],60),
                               (cs//2,cs//2), int(cs*0.45*pulse))
            screen.blit(gs, (ox+c*cs, oy+r*cs))
            pygame.draw.circle(screen, theme["target"], (cx_,cy_), max(4,size))

    def _draw_snake(self, theme):
        cs     = self._cell_size()
        ox, oy = self._cell_origin()
        body   = list(self.snake.body)

        files_loaded = getattr(self.ml_model, "files_loaded", 0)
        aura_mode = get_aura_mode(
            files_loaded=files_loaded,
            danger_mode=self.ai.danger_mode,
            corner_mode=self.ai._corner_target is not None,
        )

        draw_snake_with_aura(
            screen=screen,
            body=body,
            ox=ox, oy=oy, cs=cs,
            theme=theme,
            aura_mode=aura_mode,
            frame=self._frame,
            blink=self._blink,
        )

    def _draw_overlay(self, theme, w, h):
        def bg(alpha=180):
            s = pygame.Surface((w,h), pygame.SRCALPHA)
            s.fill((*theme["background"], alpha))
            screen.blit(s, (0,0))

        if self.state == GameState.COUNTDOWN:
            bg(170)
            cd  = math.ceil(self.countdown)
            cfg = LEVEL_CONFIG[min(self.level_index, len(LEVEL_CONFIG)-1)]
            label       = str(cfg[0])
            description = str(cfg[3])
            cd_text     = "GO!" if cd <= 0 else str(cd)
            sub_text    = "GO!" if cd <= 0 else "Starting in..."
            for surf, y in [
                (FONT_LARGE.render(label,       True, theme["countdown"]), h//2-80),
                (FONT_MEDIUM.render(description, True, theme["text"]),      h//2-30),
                (FONT_MEDIUM.render(sub_text,    True, theme["text_dim"]),  h//2+30),
                (FONT_LARGE.render(cd_text,      True, theme["countdown"]), h//2+70),
            ]:
                screen.blit(surf, surf.get_rect(centerx=w//2, top=y))

        elif self.state == GameState.LEVEL_UP:
            bg(190)
            remaining = max(0, AUTO_NEXT_SEC-(time.time()-self._state_start))
            for surf, y in [
                (FONT_LARGE.render("LEVEL COMPLETE!", True, theme["level_up"]),           h//2-50),
                (FONT_MEDIUM.render(f"Next level in {remaining:.1f}s...", True, theme["text"]), h//2+20),
            ]:
                screen.blit(surf, surf.get_rect(centerx=w//2, top=y))

        elif self.state == GameState.GAME_OVER:
            bg(200)
            remaining = max(0, AUTO_NEXT_SEC-(time.time()-self._state_start))
            for surf, y in [
                (FONT_LARGE.render("GAME OVER", True, theme["target"]),                         h//2-60),
                (FONT_MEDIUM.render(f"Score: {self.total_score}", True, theme["text"]),          h//2),
                (FONT_MEDIUM.render(f"Restarting in {remaining:.1f}s...", True, theme["text_dim"]), h//2+60),
            ]:
                screen.blit(surf, surf.get_rect(centerx=w//2, top=y))

    # ── events ────────────────────────────────────────────────────────────────


    # ── corner helpers ────────────────────────────────────────────────────────

    def _find_corner(self, prefer_top: bool, prefer_left: bool) -> tuple[int, int]:
        """
        Find the walkable cell closest to a given corner of the board.
        prefer_top=True  → top row,  False → bottom row
        prefer_left=True → left col, False → right col
        """
        cells = list(self.walkable)
        rows  = sorted({r for r, c in cells})
        cols  = sorted({c for r, c in cells})

        target_row = rows[0]  if prefer_top  else rows[-1]
        target_col = cols[0]  if prefer_left else cols[-1]

        return min(cells, key=lambda rc: (
            abs(rc[0] - target_row) + abs(rc[1] - target_col)
        ))

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_q, pygame.K_ESCAPE):
                pygame.quit(); sys.exit()
            if event.key == pygame.K_m:
                self.dark_mode = not self.dark_mode
            if event.key == pygame.K_r:
                # Full reset — back to level 1, scores zeroed, ML model preserved
                ml         = self.ml_model
                dark       = self.dark_mode
                self.__init__()
                self.ml_model    = ml
                self.ai.ml_model = ml
                self.dark_mode   = dark
            # ── layer hotkeys ─────────────────────────────────────────────────
            if event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                self.ml_model.change_layers(+1)
                print(f"[UI] Layers → {self.ml_model.n_layers}")
            elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                self.ml_model.change_layers(-1)
                print(f"[UI] Layers → {self.ml_model.n_layers}")
            # ── hidden corner keys ────────────────────────────────────────────
            if self.state == GameState.PLAYING:
                if event.key == pygame.K_a:   # top-left
                    self.ai.set_corner(self._find_corner(True, True))
                elif event.key == pygame.K_l:   # top-right
                    self.ai.set_corner(self._find_corner(True, False))
                elif event.key == pygame.K_z:   # bottom-left
                    self.ai.set_corner(self._find_corner(False, True))
                # K_m is already used for dark mode, use K_PERIOD for bottom-right
                elif event.key == pygame.K_PERIOD:  # bottom-right  (. key)
                    self.ai.set_corner(self._find_corner(False, False))
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if hasattr(self, "_mode_btn_rect") and \
               self._mode_btn_rect.collidepoint(event.pos):
                self.dark_mode = not self.dark_mode


# ── main loop ─────────────────────────────────────────────────────────────────

def main():
    game = Game()
    while True:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            game.handle_event(event)
        game.update(dt)
        game.draw()

if __name__ == "__main__":
    main()