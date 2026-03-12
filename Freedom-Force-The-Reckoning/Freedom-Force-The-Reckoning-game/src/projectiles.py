"""
projectiles.py — PlayerLaser + BossShot + NuclearWarning
יריות שחקן ואויב אקסטרה נחסמות ע"י פלטפורמות (פיזיקה נכונה).
"""
import pygame, math

PLAYER_LASER_SPEED = 14
PLAYER_LASER_W     = 18
PLAYER_LASER_H     = 6
BOSS_SHOT_SPEED    = 5
BOSS_SHOT_RADIUS   = 10


class PlayerLaser(pygame.sprite.Sprite):
    """
    ttl=None  → נעלם בקצה מסך (מצב bb)
    ttl=float → נעלם אחרי N שניות (מצב trump)
    platforms → נחסם ע"י מכשולים
    """
    def __init__(self, x, y, facing_right, ttl=None):
        super().__init__()
        self.image = pygame.Surface((PLAYER_LASER_W, PLAYER_LASER_H), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 60, 60),
                         (0, 0, PLAYER_LASER_W, PLAYER_LASER_H), border_radius=3)
        pygame.draw.rect(self.image, (255, 200, 200),
                         (2, 2, PLAYER_LASER_W-4, PLAYER_LASER_H-4), border_radius=2)
        self.rect   = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel_x  = PLAYER_LASER_SPEED if facing_right else -PLAYER_LASER_SPEED
        self.damage = 10
        self._ttl   = ttl

    def update(self, dt=0.016, world_width=99999, platforms=None, **_):
        self.rect.x += self.vel_x

        # ── חסימה ע"י פלטפורמות ─────────────────────────────────────────
        if platforms:
            for p in platforms:
                if self.rect.colliderect(p.rect):
                    self.kill()
                    return

        # ── TTL ─────────────────────────────────────────────────────────
        if self._ttl is not None:
            self._ttl -= dt
            if self._ttl <= 0:
                self.kill(); return

        # ── גבול עולם ───────────────────────────────────────────────────
        if self.rect.right < 0 or self.rect.left > world_width:
            self.kill()


class BossShot(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, colour="blue"):
        super().__init__()
        r = BOSS_SHOT_RADIUS
        self.image = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        core = (0,120,255) if colour=="blue" else (0,220,80)
        glow = (100,180,255) if colour=="blue" else (150,255,180)
        pygame.draw.circle(self.image, core, (r,r), r)
        pygame.draw.circle(self.image, glow, (r,r), r//2)
        self.rect = self.image.get_rect(center=(x,y))
        dx, dy   = target_x-x, target_y-y
        dist     = max(1, math.hypot(dx,dy))
        self.vx  = dx/dist*BOSS_SHOT_SPEED
        self.vy  = dy/dist*BOSS_SHOT_SPEED
        self.damage = 1

    def update(self, dt=0.016, world_width=99999, **_):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if (self.rect.right<0 or self.rect.left>world_width or
                self.rect.bottom<0 or self.rect.top>9999):
            self.kill()


class NuclearWarning:
    active: bool  = False
    timer:  float = 0.0
    DURATION: float = 2.0

    def start(self):
        self.active = True
        self.timer  = self.DURATION

    def tick(self, dt) -> bool:
        if not self.active: return False
        self.timer -= dt
        if self.timer <= 0: self.active = False
        return self.active

    @property
    def fraction(self):
        return max(0.0, self.timer / self.DURATION)
