"""
boss.py
-------
Stage 6 final boss — upgraded with ML-based movement prediction.

Behaviour
---------
* Stationary sprite, 500 HP.
* Fires a volley every 5 seconds.
* Uses a lightweight Random Forest to predict where the player will be
  and aims shots at the predicted position instead of the current one.
* Has 5 nuclear-bomb attacks triggered at HP thresholds.
  – Nuclear window: 5 seconds. Player must press O (shield).
  – Failing to shield = player takes a hit.
* Each player laser hit = -10 HP → 50 hits to kill.

ML model
--------
A sklearn RandomForestClassifier is trained in real-time on a rolling
window of the last HISTORY_LEN (x, y, vx, vy) snapshots of the player.
It predicts which of 5 movement zones the player will be in at next shot.

If sklearn is not installed the boss falls back to velocity extrapolation.
"""

import pygame
import random
import math
import collections
from projectiles import BossShot, NuclearWarning

import random as _rand
BOSS_MAX_HP         = 500
NUCLEAR_HP_TRIGGERS_COUNT = 20
SHOT_INTERVAL       = 3.0
import random as _random
NUCLEAR_HP_TRIGGERS = sorted(
    _random.sample(range(1, 500), 10), reverse=True
)
NUCLEAR_HP_TRIGGERS.sort(reverse=True)
NUCLEAR_TIME_INTERVAL = 30.0      # גם על בסיס זמן — כל 30 שניות
VOLLEY_SIZE         = 10
HISTORY_LEN         = 40
TRAIN_EVERY         = 60
MIN_SAMPLES_ML      = 20

try:
    from sklearn.ensemble import RandomForestClassifier
    import numpy as np
    _ML_AVAILABLE = True
except ImportError:
    _ML_AVAILABLE = False


def _xy_to_zone(x, y, sw=1280, sh=720):
    cx = x < sw / 2
    cy = y < sh / 2
    if cy and cx:       return 0
    if cy and not cx:   return 1
    if sw*0.3 < x < sw*0.7 and sh*0.3 < y < sh*0.7: return 2
    if cx:              return 3
    return 4


def _zone_to_offset(zone, sw=1280, sh=720):
    return {0:(-sw//4,-sh//4), 1:(sw//4,-sh//4), 2:(0,0),
            3:(-sw//4,sh//4),  4:(sw//4,sh//4)}.get(zone, (0,0))


class MovementPredictor:
    def __init__(self):
        self._history  = collections.deque(maxlen=HISTORY_LEN)
        self._model    = (RandomForestClassifier(n_estimators=20, max_depth=4,
                          random_state=42) if _ML_AVAILABLE else None)
        self._trained  = False
        self._frame    = 0
        self._last_pos = None
        self._last_vel = (0.0, 0.0)

    def record(self, x, y):
        if self._last_pos:
            vx = x - self._last_pos[0]
            vy = y - self._last_pos[1]
        else:
            vx, vy = 0.0, 0.0
        self._last_vel = (vx, vy)
        self._history.append((x, y, vx, vy))
        self._last_pos = (x, y)
        self._frame   += 1
        if _ML_AVAILABLE and self._frame % TRAIN_EVERY == 0 and len(self._history) >= MIN_SAMPLES_ML:
            self._train()

    def _train(self):
        data, window = list(self._history), 4
        if len(data) < window + 1:
            return
        X, y = [], []
        for i in range(len(data) - window):
            feats = []
            for j in range(window):
                feats.extend(data[i+j])
            X.append(feats)
            y.append(_xy_to_zone(data[i+window][0], data[i+window][1]))
        if len(set(y)) < 2:
            return
        try:
            self._model.fit(np.array(X, dtype=float), y)
            self._trained = True
        except Exception:
            pass

    def predict_aim(self, boss_cx, boss_cy, px, py, speed=5.0):
        vx, vy = self._last_vel
        if _ML_AVAILABLE and self._trained and len(self._history) >= 4:
            try:
                feats = []
                for snap in list(self._history)[-4:]:
                    feats.extend(snap)
                zone   = self._model.predict(np.array([feats], dtype=float))[0]
                dx, dy = _zone_to_offset(zone)
                tx = px + dx*0.6 + vx*12*0.4
                ty = py + dy*0.6 + vy*12*0.4
                return tx, ty
            except Exception:
                pass
        dist = max(1, math.hypot(px-boss_cx, py-boss_cy))
        t    = dist / max(speed, 1)
        return px + vx*t, py + vy*t


class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, asset_loader):
        super().__init__()
        self.image = asset_loader.get("boss")
        self.rect  = self.image.get_rect(center=(x, y))

        self.hp           = BOSS_MAX_HP
        self.max_hp       = BOSS_MAX_HP
        self.alive_flag   = True
        self._shot_timer  = SHOT_INTERVAL

        self._nuclear_triggers  = list(NUCLEAR_HP_TRIGGERS)
        self._nuclear_time_timer = NUCLEAR_TIME_INTERVAL  # זמן לנוקלר הבא
        self._nuclear_count     = 0                        # כמה נוקלר כבר הופעלו
        self.nuclear            = NuclearWarning()

        self.predictor = MovementPredictor()
        self._pulse    = 0.0

    def update(self, dt, player_rect, shot_group, **_):
        events = []
        if not self.alive_flag:
            return events

        px, py = float(player_rect.centerx), float(player_rect.centery)
        self.predictor.record(px, py)
        self._pulse = (self._pulse + dt*3) % (2*3.14159)

        # ── nuclear countdown (אם פעיל) ──────────────────────────────────────
        if self.nuclear.active:
            still = self.nuclear.tick(dt)
            if not still:
                events.append("nuclear_expired")
            return events          # בזמן nuclear לא יורים ולא מפעילים טריגר חדש

        # ── בדוק טריגר HP בכל פריים ─────────────────────────────────────────
        if self._nuclear_triggers and self.hp <= self._nuclear_triggers[0]:
            self._nuclear_triggers.pop(0)
            self._nuclear_count += 1
            self.nuclear.start()
            self._nuclear_time_timer = NUCLEAR_TIME_INTERVAL  # איפוס טיימר הזמן
            events.append("nuclear_start")
            return events

        # ── טריגר על בסיס זמן (גם אם השחקן לא פוגע) ────────────────────────
        self._nuclear_time_timer -= dt
        if self._nuclear_time_timer <= 0 and self._nuclear_count < 5:
            self._nuclear_time_timer = NUCLEAR_TIME_INTERVAL
            self._nuclear_count += 1
            self.nuclear.start()
            events.append("nuclear_start")
            return events

        # ── ירי רגיל — תלוי HP ───────────────────────────────────────────────
        interval, volley = self._get_fire_params()
        self._shot_timer -= dt
        if self._shot_timer <= 0:
            self._shot_timer = interval
            self._fire_volley(player_rect, shot_group, volley)
            events.append("volley_fired")

        return events

    def check_nuclear_trigger(self):
        """נקרא אחרי פגיעת לייזר — הטריגר עצמו רץ גם ב-update() כל פריים."""
        if not self._nuclear_triggers:
            return False
        if self.hp <= self._nuclear_triggers[0] and not self.nuclear.active:
            self._nuclear_triggers.pop(0)
            self._nuclear_count += 1
            self.nuclear.start()
            return True
        return False

    def take_hit(self, damage=10, level_manager=None):
        self.hp = max(0, self.hp - damage)
        if self.hp == 0:
            self.alive_flag = False
            # בדיקה אם זה לא השלב האחרון
            if level_manager and level_manager.current_index < len(level_manager._stages) - 1:
                level_manager.advance()
            return True
        return False

    def _get_fire_params(self):
        """מחזיר (interval_sec, volley_size) לפי HP נוכחי."""
        hp = self.hp
        if hp < 20:
            return 2.0, 50
        elif hp < 100:
            return 6.0, 40
        elif hp < 200:
            return 10.0, 40
        elif hp < 400:
            return 3.0, 25
        else:
            return 3.0, 10

    def _fire_volley(self, player_rect, shot_group, volley_size=10):
        cx, cy = self.rect.center
        px, py = float(player_rect.centerx), float(player_rect.centery)
        tx, ty = self.predictor.predict_aim(cx, cy, px, py)
        colour = random.choice(["blue", "green"])
        shot_group.add(BossShot(cx, cy, int(tx), int(ty), colour))
        for _ in range(volley_size - 1):
            sx = int(tx) + random.randint(-100, 100)
            sy = int(ty) + random.randint(-60,  60)
            shot_group.add(BossShot(cx, cy, sx, sy, colour))

    def draw_hp_bar(self, surface, x, y, width, height):
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, (60,0,0),         (x, y, width, height))
        col = (200,0,0) if ratio > 0.25 else (255,80,0)
        pygame.draw.rect(surface, col,              (x, y, int(width*ratio), height))
        pygame.draw.rect(surface, (255,255,255),    (x, y, width, height), 2)
        ml_lbl = "ML:ON" if (_ML_AVAILABLE and self.predictor._trained) else "ML:learning..."
        font   = pygame.font.SysFont("consolas", 14)
        surface.blit(font.render(ml_lbl, True, (180,255,180)), (x+width+8, y))