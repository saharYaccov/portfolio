"""
player.py
bb    → מקסימום 50 יריות (+ אפשר להוסיף)
trump → 5 שניות בלבד, יריות בלתי מוגבלות, כל ירייה חיה 5 שניות
"""
import pygame
from projectiles import PlayerLaser

GRAVITY            = 0.7
JUMP_VEL           = -20
MOVE_SPEED         = 5
MAX_FAILURES       = 3
TRANSFORM_DURATION = 5.0   # ← 5 שניות בלבד
LASER_COOLDOWN     = 0.20
BB_MAX_LASERS      = 200
TRUMP_LASER_TTL    = 5.0


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, asset_loader):
        super().__init__()
        self._sprite_bb    = asset_loader.get("player_bb")
        self._sprite_trump = asset_loader.get("player_trump")
        self.image = self._sprite_bb
        self.rect  = self.image.get_rect(topleft=(x, y))
        self.vel_x = self.vel_y = 0.0
        self.on_ground = False
        self.facing_right = True
        self.state = "bb"
        self._transform_timer = 0.0
        self._laser_cooldown  = 0.0
        self.failures     = 0
        self.max_failures = MAX_FAILURES
        self.alive_flag   = True
        self.antibombs    = 0
        self.lives        = 3
        self.bb_lasers_left = BB_MAX_LASERS

    @property
    def is_immune(self): return self.state == "trump"

    @property
    def stamina(self): return self.max_failures - self.failures

    def update(self, dt, platforms, laser_group, keys, world_width=99999):
        self._handle_input(keys)
        self._move_and_collide(platforms, world_width)
        self._handle_laser(dt, keys, laser_group, world_width)
        self._update_transform_timer(dt)
        self._laser_cooldown = max(0.0, self._laser_cooldown - dt)
        self._sync_sprite()

    def _handle_input(self, keys):
        self.vel_x = 0
        if keys[pygame.K_a]: self.vel_x = -MOVE_SPEED; self.facing_right = False
        if keys[pygame.K_d]: self.vel_x =  MOVE_SPEED; self.facing_right = True
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = JUMP_VEL; self.on_ground = False

    def _handle_laser(self, dt, keys, laser_group, world_width):
        if not keys[pygame.K_l] or self._laser_cooldown > 0: return
        if self.state == "bb":
            if self.bb_lasers_left <= 0: return
            self.bb_lasers_left -= 1; ttl = None
        else:
            ttl = TRUMP_LASER_TTL
        cx = self.rect.right if self.facing_right else self.rect.left
        laser_group.add(PlayerLaser(cx, self.rect.centery, self.facing_right, ttl=ttl))
        self._laser_cooldown = LASER_COOLDOWN

    def _move_and_collide(self, platforms, world_width):
        self.rect.x += self.vel_x
        self.rect.left  = max(0, self.rect.left)
        self.rect.right = min(world_width, self.rect.right)
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel_x > 0: self.rect.right = p.rect.left
                elif self.vel_x < 0: self.rect.left = p.rect.right
        self.vel_y = min(self.vel_y + GRAVITY, 20)
        self.rect.y += int(self.vel_y)
        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel_y > 0:
                    self.rect.bottom = p.rect.top; self.vel_y = 0; self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = p.rect.bottom; self.vel_y = 0

    def activate_transform(self):
        self.state = "trump"; self._transform_timer = TRANSFORM_DURATION

    def _update_transform_timer(self, dt):
        if self.state == "trump":
            self._transform_timer -= dt
            if self._transform_timer <= 0:
                self.state = "bb"; self._transform_timer = 0.0

    def _sync_sprite(self):
        c = self.rect.center
        base = self._sprite_trump if self.state == "trump" else self._sprite_bb
        self.image = pygame.transform.flip(base, True, False) if not self.facing_right else base
        self.rect  = self.image.get_rect(center=c)

    def take_hit(self):
        if self.is_immune: return False
        self.failures += 1
        if self.failures >= self.max_failures:
            self.failures = 0; self.lives -= 1
            if self.lives <= 0: self.alive_flag = False
            return True
        return False

    def increase_stamina(self): self.max_failures += 1
    def add_ammo(self, n=20):   self.bb_lasers_left += n

    def use_antibomb(self):
        if self.antibombs > 0: self.antibombs -= 1; return True
        return False

    def respawn(self, x, y):
        self.rect.topleft = (x, y)
        self.vel_x = self.vel_y = 0.0
        self.state = "bb"; self._transform_timer = 0.0
        self.failures = 0; self.bb_lasers_left = BB_MAX_LASERS
