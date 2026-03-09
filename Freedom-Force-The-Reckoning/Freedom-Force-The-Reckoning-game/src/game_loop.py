"""game_loop.py — Freedom Force: The Reckoning"""
import sys, os, math, pygame

_src = os.path.dirname(__file__)
if _src not in sys.path:
    sys.path.insert(0, _src)

from asset_loader   import AssetLoader
from player         import Player
from boss           import Boss
from powerups       import BombInventory
from level_manager  import LevelManager, TOTAL_STAGES
from hud            import HUD
from enemy          import record_player
from stats_recorder import StatsRecorder
from kill_tracker   import KillTracker

SCREEN_W=1280; SCREEN_H=720; FPS=60
TITLE="Freedom Force – The Reckoning"
TILE=48; STAGE_CLEAR_HOLD=2.5

C_YELLOW=(255,220,0); C_WHITE=(255,255,255); C_CYAN=(80,220,255)
C_RED=(220,40,40)


class Game:
    def __init__(self, base_dir="."):
        pygame.init(); pygame.font.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption(TITLE)
        self.clock  = pygame.time.Clock()
        self.loader = AssetLoader(base_dir); self.loader.load_all()
        self.hud    = HUD(SCREEN_W, SCREEN_H)
        self.level  = LevelManager(self.loader)
        self.bomb_inv = BombInventory()
        self.stats  = StatsRecorder()
        self.kt     = KillTracker()
        self.player = None; self.boss = None
        self.laser_group = pygame.sprite.Group()
        self.boss_shots  = pygame.sprite.Group()

        self.state        = "start_screen"
        self._clear_timer = 0.0
        self._paused_state = None
        self._shield_flash = 0.0
        self._cam_x = self._cam_y = 0
        self._game_time   = 0.0
        self._title_t     = 0.0

        # שמירת ציון
        self._save_flash        = 0.0   # שניות להציג הודעה
        self._save_already_done = False  # כבר נשמר בסשן זה

        # תוצאה סופית (לשמירה ב-S)
        self._end_outcome     = None   # "game_over" / "victory"
        self._end_stage       = 0
        self._final_score     = 0      # ניקוד מחושב להצגה
        self._total_lives_lost = 0     # מונה כולל של חיים שאבדו

        self._init_stage()

    # ── main loop ────────────────────────────────────────────────────────────

    def run(self):
        while True:
            dt = min(self.clock.tick(FPS)/1000.0, 0.05)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                self._handle_event(event)

            # מסך פתיחה — רק ציור, ללא update
            if self.state == "start_screen":
                self._title_t += dt
                self._draw_start_screen()
                pygame.display.flip()
                continue

            # טיימר שמירה
            if self._save_flash > 0:
                self._save_flash -= dt

            # update
            if self.state not in ("game_over","victory","menu","stage_clear","paused"):
                self._update(dt)
                self._game_time += dt
            elif self.state == "stage_clear":
                self._clear_timer -= dt
                self._game_time += dt
                if self._clear_timer <= 0:
                    self._advance_stage()

            self._draw(dt)
            pygame.display.flip()

    # ── start screen ─────────────────────────────────────────────────────────

    def _draw_start_screen(self):
        t = self._title_t
        # gradient background
        for y in range(SCREEN_H):
            r = y/SCREEN_H
            col = (int(5+(15-5)*r), int(5+(8-5)*r), int(30+(70-30)*r))
            pygame.draw.line(self.screen, col, (0,y), (SCREEN_W,y))

        f_xl = pygame.font.SysFont("consolas", 76, bold=True)
        f_lg = pygame.font.SysFont("consolas", 36, bold=True)
        f_md = pygame.font.SysFont("consolas", 24, bold=True)
        f_sm = pygame.font.SysFont("consolas", 17)

        def blit_c(surf, y):
            self.screen.blit(surf, (SCREEN_W//2 - surf.get_width()//2, y))

        # כותרת מהבהבת
        pulse = int(255*abs(math.sin(t*1.3)))
        blit_c(f_xl.render("FREEDOM FORCE", True, (255, pulse, 0)), 100)
        blit_c(f_lg.render("The Reckoning", True, C_CYAN), 195)

        # קו קישוט
        lx = SCREEN_W//2 - 320
        pygame.draw.line(self.screen, (60,100,200), (lx,250), (SCREEN_W-lx,250), 2)

        # בקרות
        blit_c(f_md.render("CONTROLS", True, C_YELLOW), 270)
        ctrl = [
            ("A / D",    "Move"),
            ("Space",    "Jump"),
            ("L",        "Laser"),
            ("1 / 2 / 3","Bombs"),
            ("O",        "Shield  (boss only)"),
            ("P",        "Pause"),
            ("S",        "Save score  (end screen)"),
        ]
        for i,(k,v) in enumerate(ctrl):
            kl = f_sm.render(k, True, (160,200,255))
            vl = f_sm.render(v, True, C_WHITE)
            bx = SCREEN_W//2 - 220
            self.screen.blit(kl, (bx,       305+i*27))
            self.screen.blit(vl, (bx+180,   305+i*27))

        # כפתור SPACE
        btn_alpha = int(180+75*abs(math.sin(t*2.5)))
        btn = pygame.Surface((440,60), pygame.SRCALPHA)
        pygame.draw.rect(btn, (0,0,0,0), (0,0,440,60))
        pygame.draw.rect(btn, (0,140,255,110), (0,0,440,60), border_radius=14)
        pygame.draw.rect(btn, (80,200,255,btn_alpha), (0,0,440,60), 3, border_radius=14)
        sp_lbl = f_lg.render("PRESS  SPACE  TO  START", True, C_WHITE)
        btn.blit(sp_lbl, (220-sp_lbl.get_width()//2, 30-sp_lbl.get_height()//2))
        self.screen.blit(btn, (SCREEN_W//2-220, 510))

        badge = f_sm.render("10 Stages  +  Final Boss: Iran  (Stage 11)", True, (160,100,100))
        blit_c(badge, 590)

    # ── init stage ───────────────────────────────────────────────────────────

    def _init_stage(self):
        stage = self.level.current
        sx, sy = stage.player_spawn
        if self.player is None:
            self.player = Player(sx, sy, self.loader)
        else:
            self.player.respawn(sx, sy)
        self.laser_group.empty(); self.boss_shots.empty(); self.boss = None
        if self.level.is_boss_stage:
            bx = stage.width - 8*TILE; by = 2*TILE
            self.boss = Boss(bx, by, self.loader)
            self.state = "boss"
            self.stats.start_boss_fight()
        else:
            self.state = "playing"
        self._cam_x = self._cam_y = 0

    def _advance_stage(self):
        self.level.advance(); self._init_stage()

    def _full_reset(self):
        self.level.reset_to_start()
        self.bomb_inv = BombInventory()
        self.stats.reset()
        self.kt.reset()
        self._game_time = 0.0
        self._save_flash = 0.0
        self._save_already_done = False
        self._end_outcome = None
        self._end_stage = 0
        self._final_score = 0
        self._total_lives_lost = 0
        self.player = None
        self._init_stage()

    # ── input ────────────────────────────────────────────────────────────────

    def _handle_event(self, event):
        # ── מסך פתיחה ──
        if self.state == "start_screen":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self._begin_game()
            return

        if event.type != pygame.KEYDOWN:
            return
        key = event.key; p = self.player

        # השהייה
        if key == pygame.K_p:
            if self.state in ("playing","boss"):
                self._paused_state = self.state; self.state = "paused"
            elif self.state == "paused":
                self.state = self._paused_state

        # restart
        if key == pygame.K_r and self.state == "game_over":
            self._full_reset()

        # שמירת ציון — רק בסוף משחק
        if event.unicode.lower() == 's' and self.state in ("game_over","victory"):
            self._do_save()

        # פצצות
        if self.state in ("playing","boss") and p:
            stage = self.level.current
            if key == pygame.K_1 and self.bomb_inv.use_b2():
                self.kt.record_bomb("B2 Bomb")
                for e in list(stage.enemies.sprites()):
                    self.kt.record_kill(e.sprite_name)
                stage.enemies.destroy_all()
            elif key == pygame.K_2 and self.bomb_inv.use_arrow():
                self.kt.record_bomb("Arrow Bomb")
                for e in list(stage.enemies.sprites()):
                    self.kt.record_kill(e.sprite_name)
                stage.enemies.destroy_radius(p.rect.centerx, p.rect.centery, 3)
            elif key == pygame.K_3 and self.bomb_inv.use_halo():
                self.kt.record_bomb("Halo Bomb")
                stage.destroy_all_ground()

        # מגן נוקלר
        if key == pygame.K_o and self.state == "boss" and self.boss and p:
            if self.boss.nuclear.active:
                if p.use_antibomb():
                    self.boss.nuclear.active = False; self._shield_flash = 0.5
                else:
                    self._trigger_game_over()

    def _begin_game(self):
        self.state = "playing"
        self._game_time = 0.0
        self.stats.start_session()

    def _do_save(self):
        if self._save_already_done:
            self._save_flash = 2.5   # הצג "כבר נשמר"
            return
        if self._end_outcome and self._end_stage:
            ok = self.stats.save(self._end_stage, self._end_outcome)
            if ok:
                self._save_already_done = True
                self._save_flash = 3.0

    # ── update ───────────────────────────────────────────────────────────────

    def _update(self, dt):
        keys  = pygame.key.get_pressed()
        stage = self.level.current; p = self.player

        record_player(p.rect.centerx, p.rect.centery)

        prev = len(self.laser_group)
        p.update(dt, stage.platforms, self.laser_group, keys, world_width=stage.width)
        if len(self.laser_group) > prev:
            self.stats.on_laser_fired()

        if p.rect.top > stage.height + TILE:
            self._register_player_hit()

        for laser in list(self.laser_group):
            laser.update(dt=dt, world_width=stage.width)

        hits = pygame.sprite.spritecollide(p, stage.powerups, True)
        for item in hits:
            self._apply_powerup(item)

        if   self.state == "playing": self._update_playing(dt, stage, p)
        elif self.state == "boss":    self._update_boss(dt, stage, p)

        # camera
        tx = p.rect.centerx - SCREEN_W//2
        ty = p.rect.centery - SCREEN_H//2
        self._cam_x += (tx - self._cam_x) * 0.15
        self._cam_y += (ty - self._cam_y) * 0.15
        self._cam_x = max(0, min(self._cam_x, stage.width  - SCREEN_W))
        self._cam_y = max(0, min(self._cam_y, stage.height - SCREEN_H))

    def _update_playing(self, dt, stage, p):
        for enemy in list(stage.enemies):
            enemy.update(stage.platforms)
            if not p.is_immune and enemy.touches_player(p.rect):
                self._register_player_hit(); break
        for laser in list(self.laser_group):
            destroyed = pygame.sprite.spritecollide(laser, stage.enemies, False)
            for e in destroyed:
                self.kt.record_kill(e.sprite_name)
                e.destroy()
                self.stats.on_enemy_killed(e.sprite_name, p.state if p else "bb")
            if destroyed: laser.kill()
        door = stage.door_group.sprite
        if door and p.rect.colliderect(door.rect):
            self._trigger_stage_clear()
        if stage.tick_timer(dt):
            self._trigger_game_over()
        stage.enemies.update(stage.platforms)
        stage.powerups.update(dt=dt)

    def _update_boss(self, dt, stage, p):
        boss = self.boss
        if not boss: return
        events = boss.update(dt, p.rect, self.boss_shots)
        if "nuclear_expired" in events:
            self._register_player_hit()
        for shot in list(self.boss_shots):
            shot.update(dt=dt, world_width=stage.width*2)
            if shot.rect.colliderect(p.rect) and not p.is_immune:
                shot.kill(); self._register_player_hit()
        for laser in list(self.laser_group):
            if laser.rect.colliderect(boss.rect):
                laser.kill()
                if boss.take_hit(laser.damage):
                    self._trigger_victory(); return
                boss.check_nuclear_trigger()
        stage.powerups.update(dt=dt)

    def _apply_powerup(self, item):
        p = self.player; k = item.KIND
        self.stats.on_powerup_collected(k)
        if   k == "energy_sphere":  p.increase_stamina()
        elif k == "activation_orb":
            prev = p.state; p.activate_transform()
            if prev != "trump": self.stats.on_trump_activated()
        elif k == "antibomb":       p.antibombs += 1
        elif k in ("b2_bomb","arrow_bomb","halo_bomb"):
            self.bomb_inv.add(k)
        elif k == "weapon_pickup":
            prev = p.state; p.activate_transform()
            if prev != "trump": self.stats.on_trump_activated()
        elif k == "damage_x":       self._register_player_hit()
        elif k == "ammo_pickup":    p.add_ammo(20)

    def _register_player_hit(self):
        self.player.take_hit()
        if not self.player.alive_flag:
            self._trigger_game_over()
        else:
            self.stats.on_life_lost()
            self._total_lives_lost += 1

    def _trigger_game_over(self):
        if self.state == "boss":
            self.stats.end_boss_fight()
        self.state = "game_over"
        self._end_outcome = "game_over"
        self._end_stage   = self.level.current_index + 1
        self._final_score = self.stats.get_score(self._end_stage, "game_over")

    def _trigger_victory(self):
        self.stats.end_boss_fight()
        self.state = "victory"
        self._end_outcome = "victory"
        self._end_stage   = self.level.current_index + 1
        self._final_score = self.stats.get_score(self._end_stage, "victory")

    def _trigger_stage_clear(self):
        self.state = "stage_clear"
        self._clear_timer = STAGE_CLEAR_HOLD

    # ── draw ─────────────────────────────────────────────────────────────────

    def _draw(self, dt):
        self._draw_background()
        cam = (int(self._cam_x), int(self._cam_y))
        stage = self.level.current

        for tile in stage.platforms:
            self.screen.blit(tile.image, (tile.rect.x-cam[0], tile.rect.y-cam[1]))
        door = stage.door_group.sprite
        if door:
            self.screen.blit(door.image, (door.rect.x-cam[0], door.rect.y-cam[1]))
        for pu in stage.powerups:
            self.screen.blit(pu.image, (pu.rect.x-cam[0], pu.rect.y-cam[1]))
        for enemy in stage.enemies:
            self.screen.blit(enemy.image, (enemy.rect.x-cam[0], enemy.rect.y-cam[1]))
        for laser in self.laser_group:
            self.screen.blit(laser.image, (laser.rect.x-cam[0], laser.rect.y-cam[1]))
        if self.boss:
            self.screen.blit(self.boss.image, (self.boss.rect.x-cam[0], self.boss.rect.y-cam[1]))
            for shot in self.boss_shots:
                self.screen.blit(shot.image, (shot.rect.x-cam[0], shot.rect.y-cam[1]))
        if self.player:
            px = self.player.rect.x - cam[0]
            py = self.player.rect.y - cam[1]
            if self.player.is_immune:
                self._draw_trump_glow(px, py)
            self.screen.blit(self.player.image, (px, py))

        # shield flash
        if self._shield_flash > 0:
            self._shield_flash -= dt
            alpha = max(0, min(255, int(180*(self._shield_flash/0.5))))
            flash = pygame.Surface((SCREEN_W,SCREEN_H), pygame.SRCALPHA)
            flash.fill((0,100,255,alpha))
            self.screen.blit(flash,(0,0))
            font = pygame.font.SysFont("consolas",48,bold=True)
            lbl  = font.render("SHIELD ACTIVATED!",True,(200,240,255))
            self.screen.blit(lbl,(SCREEN_W//2-lbl.get_width()//2, SCREEN_H//2-30))

        overlay = None
        if   self.state == "game_over":   overlay = "game_over"
        elif self.state == "stage_clear": overlay = "stage_clear"
        elif self.state == "victory":     overlay = "victory"
        elif self.state == "paused":      overlay = "paused"

        p  = self.player
        bi = self.bomb_inv
        self.hud.draw(self.screen, dt, {
            "stage_num":           self.level.current_index+1,
            "stage_timer":         stage.timer if stage.timer != float("inf") else 0,
            "game_time":           self._game_time,
            "failures":            p.failures if p else 0,
            "max_failures":        p.max_failures if p else 3,
            "lives":               p.lives if p else 3,
            "antibombs":           p.antibombs if p else 0,
            "b2":                  bi.b2,
            "arr":                 bi.arrow,
            "halo":                bi.halo,
            "is_boss_stage":       self.level.is_boss_stage,
            "boss_hp":             self.boss.hp if self.boss else 0,
            "boss_max_hp":         500,
            "trump_active":        p.state=="trump" if p else False,
            "transform_remaining": p._transform_timer if p else 0,
            "nuclear_active":      self.boss.nuclear.active if self.boss else False,
            "nuclear_fraction":    self.boss.nuclear.fraction if self.boss else 0,
            "bb_lasers_left":      p.bb_lasers_left if p else 0,
            "overlay":             overlay,
            "save_flash":          self._save_flash,
            "save_already_done":   self._save_already_done,
            # ── ניקוד ──────────────────────────────────────────────────────
            "final_score":         self._final_score,
            "enemies_killed":      self.stats.enemies_killed,
            "lives_lost_total":    self._total_lives_lost,
            "last_kill":           self.kt.last_kill,
            "is_final_stage":      self.level.is_boss_stage,
        })

    def _draw_background(self):
        idx = self.level.current_index
        tops = [(10,20,60),(20,15,50),(30,25,45),(50,20,10),(10,30,60),
                (5,5,20),(10,40,60),(5,20,5),(20,30,70),(30,5,5),(10,0,30)]
        bots = [(30,40,80),(40,35,70),(50,45,65),(80,40,20),(30,50,80),
                (15,15,40),(30,60,80),(15,40,15),(40,50,90),(50,15,15),(40,10,60)]
        t = tops[min(idx,10)]; b = bots[min(idx,10)]
        for y in range(SCREEN_H):
            r = y/SCREEN_H
            col = (int(t[0]+(b[0]-t[0])*r),
                   int(t[1]+(b[1]-t[1])*r),
                   int(t[2]+(b[2]-t[2])*r))
            pygame.draw.line(self.screen, col, (0,y), (SCREEN_W,y))

    def _draw_trump_glow(self, px, py):
        glow = pygame.Surface((80,90), pygame.SRCALPHA)
        pygame.draw.ellipse(glow, (255,200,0,60), (0,0,80,90))
        self.screen.blit(glow, (px-16, py-13))