"""
hud.py — Freedom Force: The Reckoning
HUD panel (3 rows) + overlays
"""
import pygame, math

try:
    from player import BB_MAX_LASERS
except ImportError:
    try:
        from src.player import BB_MAX_LASERS
    except ImportError:
        BB_MAX_LASERS = 30

C_WHITE  = (255,255,255); C_BLACK  = (  0,  0,  0)
C_RED    = (220, 40, 40); C_YELLOW = (255,220,  0)
C_CYAN   = ( 80,220,255); C_ORANGE = (255,140,  0)
C_PINK   = (255,100,180); C_GREEN  = ( 60,220, 80)
C_LBLUE  = ( 80,160,255); C_HUD_BG = ( 10, 10, 30,175)
C_KILL   = (255,  80, 80)   # colour for last-kill text
PAD = 14


class HUD:
    def __init__(self, screen_w, screen_h):
        self.sw = screen_w; self.sh = screen_h
        self._font_sm = pygame.font.SysFont("consolas", 17, bold=True)
        self._font_md = pygame.font.SysFont("consolas", 22, bold=True)
        self._font_lg = pygame.font.SysFont("consolas", 40, bold=True)
        self._font_xl = pygame.font.SysFont("consolas", 64, bold=True)
        self._t = 0.0

    # ── main ─────────────────────────────────────────────────────────────────

    def draw(self, surface, dt, gs):
        self._t += dt
        self._draw_panel(surface, gs)

        if gs.get("trump_active"):
            self._draw_transform_bar(surface, gs)
        if gs.get("nuclear_active"):
            self._draw_nuclear_warning(surface, gs)

        # ── מקש אחרון — פינה ימין עליון ──────────────────────────────────
        if gs.get("last_key_timer", 0) > 0:
            self._draw_last_key(surface, gs)

        # ── popups ניקוד ──────────────────────────────────────────────────
        self._draw_kill_popups(surface, gs)

        overlay = gs.get("overlay")
        if   overlay == "game_over":   self._draw_game_over(surface, gs)
        elif overlay == "stage_clear": self._draw_stage_clear(surface, gs.get("stage_num",0))
        elif overlay == "victory":     self._draw_victory(surface, gs)
        elif overlay == "paused":      self._draw_paused(surface)

        if gs.get("save_flash", 0) > 0:
            self._draw_save_notice(surface, gs)


    # ── HUD panel (3 rows) ────────────────────────────────────────────────────
    #
    #  ROW 1  — stage / timer / run-time / lives / stamina / boss-hp
    #  ROW 2  — laser / anti-bomb / bomb counts
    #  ROW 3  — KILL TRACKER  (always visible, bold red)
    #           in boss stage: "Final Round – Khamenei" (animated)
    #           otherwise:     "☠ <last enemy> Eliminated"  |  empty if no kills yet

    def _draw_panel(self, surface, gs):
        panel_h = 105           # taller panel to fit 3 rows
        pw = self.sw - 4
        panel = pygame.Surface((pw, panel_h), pygame.SRCALPHA)
        panel.fill(C_HUD_BG)
        pygame.draw.rect(panel, (60,80,160,200), (0,0,pw,panel_h), 2)
        surface.blit(panel, (2, 2))

        stage_num = gs.get("stage_num", 1)
        timer     = gs.get("stage_timer", 0)
        failures  = gs.get("failures", 0)
        max_fail  = gs.get("max_failures", 3)
        lives     = gs.get("lives", 3)
        antibombs = gs.get("antibombs", 0)
        b2        = gs.get("b2", 0)
        arr       = gs.get("arr", 0)
        halo      = gs.get("halo", 0)
        bb_lasers = gs.get("bb_lasers_left", BB_MAX_LASERS)
        trump_on  = gs.get("trump_active", False)
        tr        = gs.get("transform_remaining", 0)
        is_boss   = gs.get("is_boss_stage", False)
        boss_hp   = gs.get("boss_hp", 500)
        boss_max  = gs.get("boss_max_hp", 500)
        game_time = gs.get("game_time", 0)
        last_kill = gs.get("last_kill", "")
        is_final  = gs.get("is_final_stage", False)

        # ── ROW 1 ──────────────────────────────────────────────────────────
        x = 12; y1 = 8

        s_col = C_RED if is_boss else C_YELLOW
        lbl = self._font_md.render(
            f"< {'BOSS' if is_boss else f'STAGE {stage_num}'} >", True, s_col)
        surface.blit(lbl, (x, y1)); x += lbl.get_width()+PAD; self._vd(surface,x,y1,22)

        mins=int(timer)//60; secs=int(timer)%60
        tc = C_RED if 0 < timer < 30 else C_WHITE
        tlbl = self._font_md.render(f"T:{mins}:{secs:02d}", True, tc)
        surface.blit(tlbl,(x,y1)); x += tlbl.get_width()+PAD; self._vd(surface,x,y1,22)

        gm=int(game_time)//60; gs2=int(game_time)%60
        gtl = self._font_sm.render(f"RUN {gm}:{gs2:02d}", True, (160,200,255))
        surface.blit(gtl,(x,y1+4)); x += gtl.get_width()+PAD; self._vd(surface,x,y1,22)

        ll = self._font_md.render(f"LIVES:{lives}", True, C_PINK)
        surface.blit(ll,(x,y1)); x += ll.get_width()+PAD; self._vd(surface,x,y1,22)

        sl = self._font_sm.render("STA:", True, C_CYAN)
        surface.blit(sl,(x,y1+4)); x += sl.get_width()+6
        for i in range(max_fail):
            col = C_RED if i < (max_fail-failures) else (50,50,70)
            pygame.draw.circle(surface, col, (x+i*20, y1+13), 7)
            pygame.draw.circle(surface, (180,180,220), (x+i*20, y1+13), 7, 1)
        x += max_fail*20 + PAD

        if is_boss and boss_max > 0:
            self._vd(surface,x,y1,22)
            bl = self._font_sm.render("BOSS HP:", True, C_RED)
            surface.blit(bl,(x,y1+4)); x += bl.get_width()+6
            bw=180; bh=14; ratio=max(0.0, boss_hp/boss_max)
            pygame.draw.rect(surface,(60,0,0),(x,y1+4,bw,bh))
            pygame.draw.rect(surface,(200,0,0) if ratio>0.4 else (255,100,0),
                             (x,y1+4,int(bw*ratio),bh))
            pygame.draw.rect(surface,C_WHITE,(x,y1+4,bw,bh),1)
            ht = self._font_sm.render(f"{boss_hp}/{boss_max}", True, C_WHITE)
            surface.blit(ht,(x+bw//2-ht.get_width()//2, y1+3))

        # ── ROW 2 ──────────────────────────────────────────────────────────
        x = 12; y2 = 40

        if trump_on:
            col = (255,200,0) if tr > 2 else C_RED
            al = self._font_sm.render(f"** TRUMP: {tr:.1f}s **", True, col)
        else:
            col = C_RED if bb_lasers <= 10 else C_LBLUE
            al = self._font_sm.render(f"LASER:{bb_lasers}/{BB_MAX_LASERS}", True, col)
        surface.blit(al,(x,y2+2)); x += al.get_width()+PAD; self._vd(surface,x,y2,20)

        abl = self._font_sm.render(f"ANTI-BOMB:{antibombs}", True, C_YELLOW)
        surface.blit(abl,(x,y2+2)); x += abl.get_width()+PAD; self._vd(surface,x,y2,20)

        for txt,col in [(f"B2:{b2}",C_ORANGE),(f"ARR:{arr}",C_GREEN),(f"HALO:{halo}",C_CYAN)]:
            lb = self._font_sm.render(txt, True, col)
            surface.blit(lb,(x,y2+2)); x += lb.get_width()+PAD; self._vd(surface,x,y2,20)

        # ── ROW 3  — kill tracker ──────────────────────────────────────────
        y3 = 78

        if is_final:
            pulse = int(200 + 55 * abs(math.sin(self._t * 3.0)))
            fr_lbl = self._font_md.render(
                "⚔  Final Round – Khamenei  ⚔", True, (255, pulse, 0))
            surface.blit(fr_lbl,
                         (self.sw // 2 - fr_lbl.get_width() // 2, y3))
        else:
            # תמיד מציג — שם קובץ האויב האחרון שחוסל
            if last_kill:
                text = f"☠  Eliminated:  {last_kill}"
                col  = (255, 80, 80)
            else:
                text = "☠  --"
                col  = (70, 70, 90)
            k_lbl = self._font_md.render(text, True, col)
            surface.blit(k_lbl, (12, y3))

    def _vd(self, s, x, y, h):
        pygame.draw.line(s,(80,100,160),(x,y),(x,y+h),1)

    # ── popups ניקוד צפים ────────────────────────────────────────────────────

    def _draw_kill_popups(self, surface, gs):
        popups        = gs.get("kill_popups", [])
        running_score = gs.get("running_score", 0)

        fnt_pop   = pygame.font.SysFont("consolas", 22, bold=True)
        fnt_total = pygame.font.SysFont("consolas", 17, bold=True)

        for p in popups:
            sx, sy, text, col, timer = p[0], p[1], p[2], p[3], p[4]
            # שקיפות — מתפוגגת ב-0.6 שניות האחרונות
            alpha = int(255 * min(1.0, timer / 0.6)) if timer < 0.6 else 255

            # צל
            shadow = fnt_pop.render(text, True, (0, 0, 0))
            shadow.set_alpha(alpha)
            surface.blit(shadow, (int(sx) - shadow.get_width()//2 + 2, int(sy) + 2))

            # טקסט ראשי
            lbl = fnt_pop.render(text, True, col)
            lbl.set_alpha(alpha)
            surface.blit(lbl, (int(sx) - lbl.get_width()//2, int(sy)))

            # סכום מצטבר מתחתיו (קטן יותר)
            total_txt = f"Total: {running_score:,}"
            tlbl = fnt_total.render(total_txt, True, (200, 220, 255))
            tlbl.set_alpha(int(alpha * 0.75))
            surface.blit(tlbl, (int(sx) - tlbl.get_width()//2, int(sy) + 26))

    # ── תצוגת מקש אחרון — פינה ימין עליון ───────────────────────────────────

    def _draw_last_key(self, surface, gs):
        key_name  = gs.get("last_key_name", "")
        key_desc  = gs.get("last_key_desc", "")
        timer     = gs.get("last_key_timer", 0.0)
        if not key_name:
            return

        # שקיפות — מתפוגגת ב-0.7 שניות האחרונות
        FADE_START = 0.7
        if timer < FADE_START:
            alpha = int(255 * (timer / FADE_START))
        else:
            alpha = 255

        # מידות פנל
        PAD_BOX = 10
        key_surf = self._font_lg.render(f"[{key_name}]", True, C_YELLOW)
        desc_surf= self._font_sm.render(key_desc,        True, C_WHITE)
        bw = max(key_surf.get_width(), desc_surf.get_width()) + PAD_BOX * 2
        bh = key_surf.get_height() + desc_surf.get_height() + PAD_BOX * 2 + 4

        # מיקום: פינה ימין עליון, מרווח 8px מהשפה וממה שמתחת ל-HUD (y≈112)
        bx = self.sw - bw - 8
        by = 112

        # רקע
        box = pygame.Surface((bw, bh), pygame.SRCALPHA)
        box.fill((0, 0, 0, 0))
        pygame.draw.rect(box, (0, 20, 50, 180), (0, 0, bw, bh), border_radius=8)
        pygame.draw.rect(box, (80, 160, 255, 200), (0, 0, bw, bh), 2, border_radius=8)

        # שם מקש (גדול, צהוב)
        kx = bw // 2 - key_surf.get_width() // 2
        box.blit(key_surf, (kx, PAD_BOX))

        # תיאור (קטן, לבן)
        dx = bw // 2 - desc_surf.get_width() // 2
        box.blit(desc_surf, (dx, PAD_BOX + key_surf.get_height() + 4))

        box.set_alpha(alpha)
        surface.blit(box, (bx, by))

    # ── overlays ─────────────────────────────────────────────────────────────

    def _draw_transform_bar(self, surface, gs):
        tr = gs.get("transform_remaining",0)
        bx,by,bw,bh = 10, self.sh-34, 220, 18
        pygame.draw.rect(surface,(30,30,60),(bx,by,bw,bh))
        pygame.draw.rect(surface,(255,200,0),(bx,by,int(bw*tr/20.0),bh))
        pygame.draw.rect(surface,C_WHITE,(bx,by,bw,bh),2)
        surface.blit(self._font_sm.render("TRUMP MODE",True,C_YELLOW),(bx+bw+8,by))

    def _draw_nuclear_warning(self, surface, gs):
        fraction = gs.get("nuclear_fraction",1.0)
        alpha = int(abs(math.sin(self._t*8))*100)
        ov = pygame.Surface((self.sw,self.sh),pygame.SRCALPHA)
        ov.fill((200,0,0,alpha)); surface.blit(ov,(0,0))
        secs = int(fraction*5)+1
        l1 = self._font_xl.render("** NUCLEAR ATTACK **", True, C_YELLOW)
        l2 = self._font_lg.render(f"Press  O  to activate shield! ({secs}s)", True, C_WHITE)
        surface.blit(l1,(self.sw//2-l1.get_width()//2, self.sh//2-80))
        surface.blit(l2,(self.sw//2-l2.get_width()//2, self.sh//2+10))

    def _bg(self, surface):
        bg = pygame.Surface((self.sw,self.sh),pygame.SRCALPHA)
        bg.fill((0,0,20,190)); surface.blit(bg,(0,0))

    def _draw_game_over(self, surface, gs=None):
        self._bg(surface)
        cy = self.sh // 2
        l = self._font_xl.render("GAME  OVER", True, C_RED)
        surface.blit(l, (self.sw//2 - l.get_width()//2, cy - 160))
        if gs:
            score      = gs.get("final_score", 0)
            stage      = gs.get("stage_num", 1)
            t          = gs.get("game_time", 0)
            gm         = int(t) // 60; gs2 = int(t) % 60
            enemies    = gs.get("enemies_killed", 0)
            lives_lost = gs.get("lives_lost_total", 0)
            self._draw_score_panel(surface, score, stage, gm, gs2,
                                   enemies, lives_lost, cy - 90, C_RED)
        restart = self._font_md.render("Press R to restart", True, C_WHITE)
        surface.blit(restart, (self.sw//2 - restart.get_width()//2, cy + 120))
        hint = self._font_sm.render("Press  S  to save your score", True, (160,200,160))
        surface.blit(hint, (self.sw//2 - hint.get_width()//2, cy + 160))
        ml_hint = self._font_sm.render(
            "Press  M  to open ML Dashboard (requires saved data)",
            True,
            (80, 180, 255)
        )
        surface.blit(ml_hint, (self.sw // 2 - ml_hint.get_width() // 2, cy + 188))

    def _draw_stage_clear(self, surface, stage_num):
        self._bg(surface)
        l = self._font_xl.render(f"STAGE {stage_num} CLEAR!", True, C_GREEN)
        s = self._font_md.render("Proceeding to next stage...", True, C_WHITE)
        surface.blit(l,(self.sw//2-l.get_width()//2, self.sh//2-60))
        surface.blit(s,(self.sw//2-s.get_width()//2, self.sh//2+20))

    def _draw_victory(self, surface, gs=None):
        self._bg(surface)
        cy = self.sh // 2
        for i in range(40):
            angle = (self._t * 80 + i * 37) % 360
            rx = int(self.sw//2 + math.cos(math.radians(angle)) * (180 + i*8))
            ry = int(self.sh//2 + math.sin(math.radians(angle * 0.7)) * (80 + i*5))
            col = [(255,220,0),(0,220,120),(80,180,255),(255,80,180),(255,140,0)][i%5]
            pygame.draw.circle(surface, col, (rx%self.sw, ry%self.sh), 5)
        pulse = int(200 + 55*abs(math.sin(self._t*3)))
        lbl = self._font_xl.render("*** VICTORY! ***", True, (255, pulse, 0))
        sub = self._font_lg.render("You defeated Iran's Supreme Leader, Ali Khamenei", True, C_GREEN)
        surface.blit(lbl, (self.sw//2 - lbl.get_width()//2, cy - 200))
        surface.blit(sub, (self.sw//2 - sub.get_width()//2, cy - 140))
        if gs:
            score      = gs.get("final_score", 0)
            stage      = gs.get("stage_num", 11)
            t          = gs.get("game_time", 0)
            gm         = int(t) // 60; gs2 = int(t) % 60
            enemies    = gs.get("enemies_killed", 0)
            lives_lost = gs.get("lives_lost_total", 0)
            self._draw_score_panel(surface, score, stage, gm, gs2,
                                   enemies, lives_lost, cy - 90, C_GREEN)
        hint = self._font_sm.render("Press  S  to save your score", True, (160,220,160))
        surface.blit(hint, (self.sw//2 - hint.get_width()//2, cy + 160))
        ml_hint = self._font_sm.render(
            "Press  M  to open ML Dashboard (requires saved data)",
            True,
            (80, 180, 255)
        )
        surface.blit(ml_hint, (self.sw // 2 - ml_hint.get_width() // 2, cy + 188))

    def _draw_score_panel(self, surface, score, stage, minutes, seconds,
                          enemies, lives_lost, top_y, accent_col):
        pw, ph = 560, 200
        px = self.sw // 2 - pw // 2
        panel = pygame.Surface((pw, ph), pygame.SRCALPHA)
        panel.fill((0, 10, 30, 200))
        pygame.draw.rect(panel, accent_col + (180,), (0, 0, pw, ph), 2, border_radius=10)
        surface.blit(panel, (px, top_y))
        cx = self.sw // 2
        score_str  = f"{score:,}"
        score_surf = self._font_xl.render(score_str, True, C_YELLOW)
        glow = self._font_xl.render(score_str, True, (100, 80, 0))
        for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
            surface.blit(glow, (cx - score_surf.get_width()//2 + dx, top_y + 10 + dy))
        surface.blit(score_surf, (cx - score_surf.get_width()//2, top_y + 10))
        label = self._font_sm.render("SCORE", True, C_YELLOW)
        surface.blit(label, (cx - label.get_width()//2, top_y + 74))
        details = [
            (f"STAGE  {stage}",          C_CYAN),
            (f"TIME  {minutes}:{seconds:02d}", C_WHITE),
            (f"KILLS  {enemies}",         C_GREEN),
            (f"LIVES LOST  {lives_lost}", C_RED),
        ]
        row_y = top_y + 105
        col_w = pw // len(details)
        for i, (txt, col) in enumerate(details):
            s = self._font_sm.render(txt, True, col)
            sx = px + col_w * i + col_w // 2 - s.get_width() // 2
            surface.blit(s, (sx, row_y))
        pygame.draw.line(surface, (60, 80, 120),
                         (px + 20, top_y + 98), (px + pw - 20, top_y + 98), 1)
        rank, rank_col = self._get_rank(score)
        rank_surf = self._font_lg.render(rank, True, rank_col)
        surface.blit(rank_surf, (cx - rank_surf.get_width()//2, top_y + 145))

    def _get_rank(self, score):
        if score >= 150_000: return "S  RANK", (255, 220,   0)
        if score >= 84_000: return "A  RANK", (100, 220, 100)
        if score >=  63_000: return "B  RANK", ( 80, 180, 255)
        if score >=  12_000: return "C  RANK", (200, 200,  80)
        if score >=  1_000: return "D  RANK", (180, 140,  80)
        return                     "F  RANK", (150,  50,  50)

    def _draw_paused(self, surface):
        self._bg(surface)
        l = self._font_xl.render("PAUSED", True, C_CYAN)
        s = self._font_md.render("Press P to resume", True, C_WHITE)
        surface.blit(l,(self.sw//2-l.get_width()//2, self.sh//2-40))
        surface.blit(s,(self.sw//2-s.get_width()//2, self.sh//2+20))

    def _draw_save_notice(self, surface, gs):
        flash = gs.get("save_flash", 0)
        alpha = min(255, int(flash * 3 * 255))
        saved_already = gs.get("save_already_done", False)
        msg = "Score already saved!" if saved_already else "Score saved to record.csv"
        col = (255, 200, 80)      if saved_already else (80,  255, 140)
        box = pygame.Surface((460,52), pygame.SRCALPHA)
        box.fill((0,30,0,180))
        pygame.draw.rect(box,(0,200,80,200),(0,0,460,52),2)
        lbl = self._font_md.render(msg, True, col)
        box.blit(lbl,(230-lbl.get_width()//2, 26-lbl.get_height()//2))
        box.set_alpha(alpha)
        surface.blit(box,(self.sw//2-230, self.sh//2-140))