"""
enemy.py — אויב פטרול עם ML משותף
Random Forest לומד תנועת השחקן ומכוון פטרול לכיוונו.
"""
import pygame, random, collections
try:
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier
    _ML_OK = True
except ImportError:
    _ML_OK = False

TILE        = 48
MOVE_SPEED  = 2
GRAVITY     = 0.6
HISTORY_LEN = 40
TRAIN_EVERY = 90
MIN_SAMPLES = 16


class _SharedPredictor:
    """מודל ML אחד לכל האויבים — לומד תנועת שחקן."""
    def __init__(self):
        self._hist    = collections.deque(maxlen=HISTORY_LEN)
        self._model   = (RandomForestClassifier(n_estimators=15, max_depth=3,
                          random_state=7) if _ML_OK else None)
        self._trained = False
        self._frame   = 0
        self._last    = None
        self._vel     = (0.0, 0.0)
        self.direction = 0   # -1/0/1 — ניבוי אחרון

    def record(self, px, py):
        vx = (px - self._last[0]) if self._last else 0.0
        vy = (py - self._last[1]) if self._last else 0.0
        self._vel  = (vx, vy)
        self._last = (px, py)
        self._hist.append((px, py, vx, vy))
        self._frame += 1
        if _ML_OK and self._frame % TRAIN_EVERY == 0 and len(self._hist) >= MIN_SAMPLES:
            self._train()
        if self._trained:
            self.direction = self._predict()

    def _train(self):
        data = list(self._hist)
        X, y = [], []
        for i in range(len(data) - 4):
            feats = [v for snap in data[i:i+4] for v in snap]
            nxt   = data[i+4][2]   # next vx
            label = 1 if nxt > 0.4 else (-1 if nxt < -0.4 else 0)
            X.append(feats); y.append(label)
        if len(set(y)) < 2: return
        try:
            self._model.fit(np.array(X, dtype=float), y)
            self._trained = True
        except Exception:
            pass

    def _predict(self):
        if len(self._hist) < 4: return 0
        try:
            feats = [v for snap in list(self._hist)[-4:] for v in snap]
            return int(self._model.predict(np.array([feats], dtype=float))[0])
        except Exception:
            return 0

    @property
    def player_x(self):
        return self._last[0] if self._last else 0


SHARED = _SharedPredictor()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, patrol_left, patrol_right, sprite, sprite_name="Enemy"):
        super().__init__()
        self._base    = sprite
        self.image    = sprite.copy()
        self.rect     = self.image.get_rect(topleft=(x, y))
        self.pl       = patrol_left
        self.pr       = patrol_right
        self._dir     = 1
        self.vel_y    = 0.0
        self.on_ground = False
        self.alive_flag = True
        self.sprite_name = sprite_name   # display name for kill message

    def update(self, platforms, **_):
        if not self.alive_flag:
            self.kill(); return

        # ML: הסט טווח פטרול לכיוון השחקן
        if SHARED._trained and SHARED.direction != 0:
            px = SHARED.player_x
            if px > self.rect.centerx:
                self.pr = min(self.pr + 3, px + 4*TILE)
            else:
                self.pl = max(self.pl - 3, px - 4*TILE)

        # X
        self.rect.x += MOVE_SPEED * self._dir
        if self.rect.right >= self.pr:
            self._dir = -1
            self.image = pygame.transform.flip(self._base, True, False)
        elif self.rect.left <= self.pl:
            self._dir = 1
            self.image = self._base.copy()

        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self._dir > 0:
                    self.rect.right = p.rect.left; self._dir = -1
                    self.image = pygame.transform.flip(self._base, True, False)
                else:
                    self.rect.left = p.rect.right; self._dir = 1
                    self.image = self._base.copy()

        # Y
        self.vel_y = min(self.vel_y + GRAVITY, 20)
        self.rect.y += int(self.vel_y)
        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel_y > 0:
                    self.rect.bottom = p.rect.top; self.vel_y = 0; self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = p.rect.bottom; self.vel_y = 0

    def destroy(self):         self.alive_flag = False
    def touches_player(self, r): return self.rect.colliderect(r)


class EnemyGroup(pygame.sprite.Group):
    @staticmethod
    def spawn(x, y, pl, pr, loader):
        sprite = loader.get_random_enemy_sprite()
        name   = loader.get_enemy_sprite_name(sprite)
        return Enemy(x, y, pl, pr, sprite, sprite_name=name)

    def destroy_all(self):
        for e in list(self.sprites()): e.destroy()

    def destroy_radius(self, cx, cy, radius_tiles):
        r = radius_tiles * TILE
        for e in list(self.sprites()):
            if (e.rect.centerx-cx)**2 + (e.rect.centery-cy)**2 <= r*r:
                e.destroy()


def record_player(px, py):
    """קרא כל פריים מה-game_loop."""
    SHARED.record(px, py)
