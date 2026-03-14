"""
enemy.py — אויב פטרול + ExtraEnemy (מיני-בוס כחול, 3 יריות)
=============================================================
ML: Random Forest לומד תנועת שחקן, מנחה פטרול.
ניתוח (Feature Importance / F-test / T-test / Pearson) → model_analysis.txt
"""
import os, math, collections, threading
import pygame, random

try:
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.feature_selection import f_classif
    from scipy import stats as _scipy_stats
    _ML_OK = True
except ImportError:
    _ML_OK = False

# ── קבועים בסיסיים ───────────────────────────────────────────────────────────
TILE        = 48
MOVE_SPEED  = 2
GRAVITY     = 0.6
HISTORY_LEN = 60
TRAIN_EVERY = 120
MIN_SAMPLES = 20
WINDOW      = 5

# ── Extra Enemy ───────────────────────────────────────────────────────────────
EXTRA_MOVE_SPEED     = 3
EXTRA_SHOOT_COOLDOWN = 1.7     # שניות בין יריות (יעודכן לפי רמת קושי)
EXTRA_SHOT_SPEED     = 6
EXTRA_SHOT_RADIUS    = 8
EXTRA_HP             = 5
EXTRA_SCALE          = 1.4
NUM_EXTRA_PER_STAGE  = 5       # מספר אויבי Extra בכל שלב (יעודכן לפי רמת קושי)


def set_difficulty(level: str):
    """
    Configure global difficulty for shooting enemies.

    easy   → 4 Extra enemies per stage, normal fire rate
    middle → 8 Extra enemies per stage, normal fire rate
    hard   → 12 Extra enemies per stage, fire cooldown × 0.7 (faster)
    """
    global NUM_EXTRA_PER_STAGE, EXTRA_SHOOT_COOLDOWN

    lvl = (level or "easy").lower()
    base_cooldown = 1.7

    if lvl == "easy":
        NUM_EXTRA_PER_STAGE = 4
        EXTRA_SHOOT_COOLDOWN = base_cooldown
    elif lvl in ("middle", "medium"):
        NUM_EXTRA_PER_STAGE = 8
        EXTRA_SHOOT_COOLDOWN = base_cooldown
    elif lvl == "hard":
        NUM_EXTRA_PER_STAGE = 12
        EXTRA_SHOOT_COOLDOWN = base_cooldown * 0.7
    else:
        # fallback
        NUM_EXTRA_PER_STAGE = 5
        EXTRA_SHOOT_COOLDOWN = base_cooldown

    print(f"[enemy] difficulty set to '{lvl}': NUM_EXTRA_PER_STAGE={NUM_EXTRA_PER_STAGE}, "
          f"EXTRA_SHOOT_COOLDOWN={EXTRA_SHOOT_COOLDOWN:.2f}")

# ── ML נתיבים ─────────────────────────────────────────────────────────────────
_HERE   = os.path.dirname(os.path.abspath(__file__))
_ML_DIR = os.path.join(_HERE, "..", "machine_learning")
_REPORT = os.path.join(_ML_DIR, "model_analysis.txt")

_FEATURE_NAMES = [
    f"t-{WINDOW-1-i}_{v}"
    for i in range(WINDOW)
    for v in ("px", "py", "vx", "vy")
]

# ─────────────────────────────────────────────────────────────────────────────
#  ExtraEnemyShot  —  כדור כחול שנחסם ע"י פלטפורמות
# ─────────────────────────────────────────────────────────────────────────────

class ExtraEnemyShot(pygame.sprite.Sprite):
    """כדור לייזר כחול שנורה מ-ExtraEnemy. נחסם לחלוטין ע"י platforms."""

    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        r = EXTRA_SHOT_RADIUS
        self.image = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 80, 255), (r, r), r)
        pygame.draw.circle(self.image, (120, 180, 255), (r, r), r // 2)
        pygame.draw.circle(self.image, (200, 230, 255), (r, r), r // 4)
        self.rect   = self.image.get_rect(center=(x, y))
        self._x     = float(x)
        self._y     = float(y)
        dx, dy      = target_x - x, target_y - y
        dist        = max(1, math.hypot(dx, dy))
        self.vx     = dx / dist * EXTRA_SHOT_SPEED
        self.vy     = dy / dist * EXTRA_SHOT_SPEED
        self.damage = 1

    def update(self, dt=0.016, world_width=99999, platforms=None, **_):
        self._x += self.vx
        self._y += self.vy
        self.rect.x = int(self._x)
        self.rect.y = int(self._y)

        # ── חסימה ע"י פלטפורמות ─────────────────────────────────────────────
        if platforms:
            for p in platforms:
                if self.rect.colliderect(p.rect):
                    self.kill()
                    return

        # ── יציאה מגבולות ───────────────────────────────────────────────────
        if (self.rect.right < 0 or self.rect.left > world_width or
                self.rect.bottom < 0 or self.rect.top > 9999):
            self.kill()


# ─────────────────────────────────────────────────────────────────────────────
#  ExtraEnemy  —  חייל כחול עם ריבוע, 3 HP, יורה 3 כדורים
# ─────────────────────────────────────────────────────────────────────────────

class ExtraEnemy(pygame.sprite.Sprite):
    """חייל אקסטרה: גדול יותר, כחול, יורה פרץ של 3 יריות."""

    # מרחק ירי מקסימלי (פיקסלים) — רק כשהשחקן בטווח
    SHOOT_RANGE = 500

    def __init__(self, x, y, patrol_left, patrol_right, sprite, sprite_name="ExtraEnemy"):
        super().__init__()
        # שינוי גודל
        sw = int(sprite.get_width()  * EXTRA_SCALE)
        sh = int(sprite.get_height() * EXTRA_SCALE)
        scaled        = pygame.transform.scale(sprite, (sw, sh))
        self._base    = scaled
        self.image    = scaled.copy()
        self.rect     = self.image.get_rect(topleft=(x, y))

        self.pl           = patrol_left
        self.pr           = patrol_right
        self._dir         = 1
        self.vel_y        = 0.0
        self.on_ground    = False
        self.alive_flag   = True
        self.sprite_name  = sprite_name
        self.hp           = EXTRA_HP

        # ירי פרץ: כל EXTRA_SHOOT_COOLDOWN שניות — 3 כדורים ברצף
        self._shoot_timer  = random.uniform(1.0, EXTRA_SHOOT_COOLDOWN)
        self._burst_count  = 0          # כמה יריות שנורו בפרץ הנוכחי
        self._burst_timer  = 0.0        # השהייה בין יריות בפרץ
        self._burst_target = (0, 0)     # מטרה קבועה לכל הפרץ

        # אנימציית ריבוע כחול
        self._pulse = 0.0

    # ── ציור ריבוע כחול ────────────────────────────────────────────────────
    def draw_box(self, surface, cam_x, cam_y):
        """מצייר ריבוע כחול מהבהב סביב האויב — קרא מ-_draw."""
        self._pulse += 0.06
        alpha = int(160 + 90 * abs(math.sin(self._pulse)))
        sx = self.rect.x - cam_x
        sy = self.rect.y - cam_y
        pad = 4
        box = pygame.Rect(sx - pad, sy - pad,
                          self.rect.width + pad * 2,
                          self.rect.height + pad * 2)
        # HP pips מעל
        for i in range(EXTRA_HP):
            col = (0, 100, 255) if i < self.hp else (40, 40, 80)
            pygame.draw.rect(surface, col,
                             (sx + i * 10, sy - 14, 8, 7), border_radius=2)
        # ריבוע
        pygame.draw.rect(surface, (0, 100, 255, alpha), box, 2, border_radius=4)
        # פינות מוארות
        L = 10
        for cx2, cy2, dx2, dy2 in [
            (box.left,  box.top,    1,  1),
            (box.right, box.top,   -1,  1),
            (box.left,  box.bottom, 1, -1),
            (box.right, box.bottom,-1, -1),
        ]:
            pygame.draw.line(surface, (80, 180, 255),
                             (cx2, cy2), (cx2 + dx2 * L, cy2), 2)
            pygame.draw.line(surface, (80, 180, 255),
                             (cx2, cy2), (cx2, cy2 + dy2 * L), 2)

    # ── update ─────────────────────────────────────────────────────────────
    def update(self, platforms, dt=0.016, shot_group=None, player_rect=None, **_):
        if not self.alive_flag:
            self.kill(); return

        # ── תנועה ──────────────────────────────────────────────────────────
        self.rect.x += EXTRA_MOVE_SPEED * self._dir
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

        # ── כבידה ─────────────────────────────────────────────────────────
        self.vel_y = min(self.vel_y + GRAVITY, 20)
        self.rect.y += int(self.vel_y)
        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel_y > 0:
                    self.rect.bottom = p.rect.top; self.vel_y = 0; self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = p.rect.bottom; self.vel_y = 0

        # ── ירי פרץ ────────────────────────────────────────────────────────
        if shot_group is not None and player_rect is not None:
            self._handle_shooting(dt, shot_group, player_rect)

    def _handle_shooting(self, dt, shot_group, player_rect):
        px, py = player_rect.centerx, player_rect.centery
        dist   = math.hypot(px - self.rect.centerx, py - self.rect.centery)

        # ── בין פרצים: ספירה לאחור ──────────────────────────────────────
        if self._burst_count == 0:
            self._shoot_timer -= dt
            if self._shoot_timer <= 0 and dist <= self.SHOOT_RANGE:
                # התחלת פרץ — קבע מטרה קבועה
                self._burst_target = (px, py)
                self._burst_count  = 3
                self._burst_timer  = 0.0
                self._shoot_timer  = EXTRA_SHOOT_COOLDOWN

        # ── בתוך פרץ: ירי עם השהייה קטנה בין יריות ─────────────────────
        else:
            self._burst_timer -= dt
            if self._burst_timer <= 0:
                tx, ty = self._burst_target
                shot_group.add(ExtraEnemyShot(
                    self.rect.centerx, self.rect.centery, tx, ty))
                self._burst_count -= 1
                self._burst_timer  = 0.18   # 0.18 שנ' בין כל כדור

    def take_hit(self, dmg=10):
        self.hp -= 1
        if self.hp <= 0:
            self.alive_flag = False
            return True
        return False

    def destroy(self):           self.alive_flag = False
    def touches_player(self, r): return self.rect.colliderect(r)


# ─────────────────────────────────────────────────────────────────────────────
#  ML helpers
# ─────────────────────────────────────────────────────────────────────────────

def _sig_stars(p):
    if p < 0.001: return "***"
    if p < 0.01:  return "** "
    if p < 0.05:  return "*  "
    return "   "

def _pearson(x, y):
    if not _ML_OK or np.std(x) == 0: return 0.0
    try:
        r, _ = _scipy_stats.pearsonr(x, y)
        return float(r) if not math.isnan(r) else 0.0
    except Exception:
        return 0.0

def _write_report(feature_names, importances, f_vals, p_vals_f,
                  t_stats, p_vals_t, correlations, n_samples, class_dist):
    os.makedirs(_ML_DIR, exist_ok=True)
    W = 76
    lines = []; a = lines.append
    a("=" * W)
    a("  FREEDOM FORCE — ניתוח מודל ML  (enemy.py / _SharedPredictor)")
    a("=" * W)
    a(f"  דגימות לאימון : {n_samples}")
    dist_str = "  |  ".join(
        f"{'RIGHT' if k==1 else ('LEFT' if k==-1 else 'STILL')}: {v}"
        for k, v in sorted(class_dist.items()))
    a(f"  התפלגות מחלקות: {dist_str}"); a("")

    a("-" * W)
    a("  חשיבות תכונות  (Random Forest Feature Importance)")
    a("-" * W)
    a(f"  {'תכונה':<22} {'חשיבות':>10}  {'F-value':>9}  {'p(F)':>9}  sig")
    a("  " + "-" * 60)
    for i in sorted(range(len(feature_names)), key=lambda i: importances[i], reverse=True):
        a(f"  {feature_names[i]:<22} {importances[i]:>10.5f}"
          f"  {f_vals[i]:>9.3f}  {p_vals_f[i]:>9.5f}  {_sig_stars(p_vals_f[i])}")
    a("")

    a("-" * W); a("  מבחן T  (Welch t-test: RIGHT vs LEFT)"); a("-" * W)
    a(f"  {'תכונה':<22} {'t-stat':>9}  {'p(t)':>9}  sig  פרשנות")
    a("  " + "-" * 62)
    for i in sorted(range(len(feature_names)), key=lambda i: abs(t_stats[i]), reverse=True):
        interp = ("גבוה ב-RIGHT" if t_stats[i] > 0 else "גבוה ב-LEFT") if p_vals_t[i] < 0.05 else "ללא הבדל"
        a(f"  {feature_names[i]:<22} {t_stats[i]:>+9.3f}  {p_vals_t[i]:>9.5f}"
          f"  {_sig_stars(p_vals_t[i])}  {interp}")
    a("")

    a("-" * W); a("  קורלציה  (Pearson r — תכונה מול כיוון RIGHT=1)"); a("-" * W)
    a(f"  {'תכונה':<22} {'r':>10}  {'|r|':>8}  כיוון"); a("  " + "-" * 52)
    for i in sorted(range(len(feature_names)), key=lambda i: abs(correlations[i]), reverse=True):
        a(f"  {feature_names[i]:<22} {correlations[i]:>+10.4f}"
          f"  {abs(correlations[i]):>8.4f}  {'חיובי (+)' if correlations[i]>=0 else 'שלילי (-)'}")
    a(""); a("=" * W)
    a("  נוצר אוטומטית ע\"י enemy.py — _SharedPredictor._train()"); a("=" * W)
    try:
        with open(_REPORT, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"[ML] דוח נשמר → {_REPORT}")
    except Exception as e:
        print(f"[ML] שגיאה: {e}")

def get_report_text():
    """מחזיר את תוכן הדוח כטקסט (לתצוגה במסך)."""
    try:
        if os.path.isfile(_REPORT):
            with open(_REPORT, encoding="utf-8") as f:
                return f.read()
    except Exception:
        pass
    return "(דוח לא נמצא — שחק קצת כדי לאמן את המודל)"


# ─────────────────────────────────────────────────────────────────────────────
#  _SharedPredictor
# ─────────────────────────────────────────────────────────────────────────────

class _SharedPredictor:
    def __init__(self):
        self._hist    = collections.deque(maxlen=HISTORY_LEN)
        self._model   = (RandomForestClassifier(
                             n_estimators=25, max_depth=4,
                             random_state=7, n_jobs=1) if _ML_OK else None)
        self._trained = False
        self._frame   = 0
        self._last    = None
        self.direction = 0
        self._class_dist = {}

    def record(self, px, py):
        vx = (px - self._last[0]) if self._last else 0.0
        vy = (py - self._last[1]) if self._last else 0.0
        self._last = (px, py)
        self._hist.append((px, py, vx, vy))
        self._frame += 1
        if (_ML_OK and self._frame % TRAIN_EVERY == 0
                and len(self._hist) >= MIN_SAMPLES + WINDOW):
            threading.Thread(target=self._train, daemon=True).start()
        if self._trained:
            self.direction = self._predict()

    @property
    def player_x(self):
        return self._last[0] if self._last else 0

    def _build_dataset(self):
        data = list(self._hist)
        X, y = [], []
        for i in range(len(data) - WINDOW):
            feats = [v for snap in data[i:i+WINDOW] for v in snap]
            nxt_vx = data[i+WINDOW][2]
            label = 1 if nxt_vx > 0.4 else (-1 if nxt_vx < -0.4 else 0)
            X.append(feats); y.append(label)
        if len(X) < MIN_SAMPLES:
            return None, None
        return np.array(X, dtype=float), np.array(y, dtype=int)

    def _train(self):
        if not _ML_OK: return
        try:
            X, y = self._build_dataset()
            if X is None or y is None or len(set(y.tolist())) < 2: return
            self._model.fit(X, y)
            self._trained = True
            classes, counts = np.unique(y, return_counts=True)
            self._class_dist = dict(zip(classes.tolist(), counts.tolist()))
            importances = self._model.feature_importances_

            try:
                f_vals, p_vals_f = f_classif(X, y)
                f_vals   = np.nan_to_num(f_vals,   nan=0.0)
                p_vals_f = np.nan_to_num(p_vals_f, nan=1.0)
            except Exception:
                f_vals   = np.zeros(X.shape[1])
                p_vals_f = np.ones(X.shape[1])

            mask_r = (y == 1); mask_l = (y == -1)
            t_stats, p_vals_t = [], []
            for j in range(X.shape[1]):
                g1, g2 = X[mask_r, j], X[mask_l, j]
                if len(g1) >= 2 and len(g2) >= 2:
                    try:
                        t, p = _scipy_stats.ttest_ind(g1, g2, equal_var=False)
                        t = 0.0 if math.isnan(t) else float(t)
                        p = 1.0 if math.isnan(p) else float(p)
                    except Exception:
                        t, p = 0.0, 1.0
                else:
                    t, p = 0.0, 1.0
                t_stats.append(t); p_vals_t.append(p)
            t_stats  = np.array(t_stats)
            p_vals_t = np.array(p_vals_t)
            y_bin    = (y == 1).astype(float)
            correlations = np.array([_pearson(X[:, j], y_bin) for j in range(X.shape[1])])

            _write_report(_FEATURE_NAMES, importances, f_vals, p_vals_f,
                          t_stats, p_vals_t, correlations,
                          n_samples=len(X), class_dist=self._class_dist)
        except Exception as e:
            print(f"[ML] train error: {e}")

    def _predict(self):
        if len(self._hist) < WINDOW: return 0
        try:
            feats = [v for snap in list(self._hist)[-WINDOW:] for v in snap]
            return int(self._model.predict(np.array([feats], dtype=float))[0])
        except Exception:
            return 0


SHARED = _SharedPredictor()


# ─────────────────────────────────────────────────────────────────────────────
#  Enemy  (רגיל)
# ─────────────────────────────────────────────────────────────────────────────

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, patrol_left, patrol_right, sprite, sprite_name="Enemy"):
        super().__init__()
        self._base     = sprite
        self.image     = sprite.copy()
        self.rect      = self.image.get_rect(topleft=(x, y))
        self.pl        = patrol_left
        self.pr        = patrol_right
        self._dir      = 1
        self.vel_y     = 0.0
        self.on_ground = False
        self.alive_flag = True
        self.sprite_name = sprite_name

    def update(self, platforms, **_):
        if not self.alive_flag:
            self.kill(); return
        if SHARED._trained and SHARED.direction != 0:
            px = SHARED.player_x
            if px > self.rect.centerx:
                self.pr = min(self.pr + 3, px + 4 * TILE)
            else:
                self.pl = max(self.pl - 3, px - 4 * TILE)

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

        self.vel_y = min(self.vel_y + GRAVITY, 20)
        self.rect.y += int(self.vel_y)
        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel_y > 0:
                    self.rect.bottom = p.rect.top; self.vel_y = 0; self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = p.rect.bottom; self.vel_y = 0

    def destroy(self):           self.alive_flag = False
    def touches_player(self, r): return self.rect.colliderect(r)


# ─────────────────────────────────────────────────────────────────────────────
#  EnemyGroup
# ─────────────────────────────────────────────────────────────────────────────

class EnemyGroup(pygame.sprite.Group):
    @staticmethod
    def spawn(x, y, pl, pr, loader):
        sprite = loader.get_random_enemy_sprite()
        name   = loader.get_enemy_sprite_name(sprite)
        return Enemy(x, y, pl, pr, sprite, sprite_name=name)

    @staticmethod
    def spawn_extra(x, y, pl, pr, loader):
        sprite = loader.get_random_enemy_sprite()
        name   = loader.get_enemy_sprite_name(sprite)
        return ExtraEnemy(x, y, pl, pr, sprite, sprite_name=name)

    def destroy_all(self):
        for e in list(self.sprites()): e.destroy()

    def destroy_radius(self, cx, cy, radius_tiles):
        r = radius_tiles * TILE
        for e in list(self.sprites()):
            if (e.rect.centerx-cx)**2 + (e.rect.centery-cy)**2 <= r*r:
                e.destroy()


def record_player(px, py):
    SHARED.record(px, py)