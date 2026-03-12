"""
powerups.py
חדש: WeaponPickup (W) כחול בוהק, DamageX (X) איקס אדום, AmmoPickup (M) +20
"""
import pygame, math


class PowerUp(pygame.sprite.Sprite):
    KIND = "base"
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect  = self.image.get_rect(center=(x, y))
        self._t    = 0.0
    def update(self, dt=0.016, **_):
        self._t += dt
        self.rect.y += int(math.sin(self._t * 3) * 0.5)


class EnergySphere(PowerUp):
    KIND = "energy_sphere"
    def __init__(self, x, y, loader):
        s = loader.get("energy_sphere")
        g = pygame.Surface((s.get_width()+8, s.get_height()+8), pygame.SRCALPHA)
        pygame.draw.ellipse(g, (100,255,200,80), (0,0,g.get_width(),g.get_height()))
        g.blit(s,(4,4))
        super().__init__(x, y, g)

class ActivationOrb(PowerUp):
    KIND = "activation_orb"
    def __init__(self, x, y):
        r=20; s=pygame.Surface((r*2,r*2),pygame.SRCALPHA)
        pygame.draw.circle(s,(255,200,0),(r,r),r)
        pygame.draw.circle(s,(255,240,150),(r-4,r-4),r//3)
        super().__init__(x, y, s)

class AntiBomb(PowerUp):
    KIND = "antibomb"
    def __init__(self, x, y, loader):
        base=loader.get("antibomb"); r=base.get_width()//2+8
        s=pygame.Surface((r*2,r*2),pygame.SRCALPHA)
        pygame.draw.circle(s,(255,230,0,120),(r,r),r)
        pygame.draw.circle(s,(220,30,30),(r,r),r-6)
        s.blit(base,(r-base.get_width()//2, r-base.get_height()//2))
        super().__init__(x, y, s)

class B2BombPickup(PowerUp):
    KIND = "b2_bomb"
    def __init__(self, x, y, loader): super().__init__(x, y, loader.get("b2_bomb"))

class ArrowBombPickup(PowerUp):
    KIND = "arrow_bomb"
    def __init__(self, x, y, loader): super().__init__(x, y, loader.get("arrow_bomb"))

class HaloBombPickup(PowerUp):
    KIND = "halo_bomb"
    def __init__(self, x, y, loader): super().__init__(x, y, loader.get("halo_bomb"))


# ══ חדשים לשלב הבוס ══════════════════════════════════════════════════════════

class WeaponPickup(PowerUp):
    """W — כחול בוהק, מפעיל trump"""
    KIND = "weapon_pickup"
    def __init__(self, x, y):
        r=22; s=pygame.Surface((r*2,r*2),pygame.SRCALPHA)
        pygame.draw.circle(s,(0,180,255,90),(r,r),r)
        pygame.draw.circle(s,(0,220,255),(r,r),r-5)
        pygame.draw.circle(s,(255,255,255),(r-5,r-5),5)
        super().__init__(x, y, s)
    def update(self, dt=0.016, **_):
        self._t += dt
        self.image.set_alpha(max(0, min(255, int(180+75*math.sin(self._t*5)))))


class DamageX(PowerUp):
    """X — איקס אדום, מוריד חיים אחד"""
    KIND = "damage_x"
    def __init__(self, x, y):
        sz=38; s=pygame.Surface((sz,sz),pygame.SRCALPHA)
        pygame.draw.circle(s,(80,0,0,200),(sz//2,sz//2),sz//2)
        w=6
        pygame.draw.line(s,(255,30,30),(5,5),(sz-5,sz-5),w)
        pygame.draw.line(s,(255,30,30),(sz-5,5),(5,sz-5),w)
        pygame.draw.circle(s,(200,0,0),(sz//2,sz//2),sz//2,2)
        super().__init__(x, y, s)
    def update(self, dt=0.016, **_):
        self._t += dt
        self.image.set_alpha(max(0, min(255, int(140+115*abs(math.sin(self._t*6))))))


class AmmoPickup(PowerUp):
    """+20 יריות — ירוק-צהוב"""
    KIND = "ammo_pickup"
    def __init__(self, x, y):
        sz=32; s=pygame.Surface((sz,sz),pygame.SRCALPHA)
        pygame.draw.circle(s,(180,255,0,160),(sz//2,sz//2),sz//2)
        pygame.draw.circle(s,(140,210,0),(sz//2,sz//2),sz//2-4)
        font=pygame.font.SysFont(None,16)
        lbl=font.render("+20",True,(0,40,0))
        s.blit(lbl,(sz//2-lbl.get_width()//2, sz//2-lbl.get_height()//2))
        super().__init__(x, y, s)


class BombInventory:
    def __init__(self): self.b2=0; self.arrow=0; self.halo=0
    def add(self, k):
        if k=="b2_bomb": self.b2+=1
        elif k=="arrow_bomb": self.arrow+=1
        elif k=="halo_bomb":  self.halo+=1
    def use_b2(self):
        if self.b2>0: self.b2-=1; return True
        return False
    def use_arrow(self):
        if self.arrow>0: self.arrow-=1; return True
        return False
    def use_halo(self):
        if self.halo>0: self.halo-=1; return True
        return False
    @property
    def total_antibombs_label(self):
        return f"B2:{self.b2}  ARR:{self.arrow}  HALO:{self.halo}"
