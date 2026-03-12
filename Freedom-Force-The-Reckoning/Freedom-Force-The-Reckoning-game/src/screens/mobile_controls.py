"""
screens/mobile_controls.py
==========================
On-screen touch buttons for mobile / touchscreen play.

Draws a D-pad (Left / Right / Jump) on the left side and
action buttons (Fire, O, 1, 2, 3, Pause) on the right side.

Usage:
    mc = MobileControls(screen)

    # in your game loop:
    mc.draw()
    keys_held = mc.get_keys()   # dict: {action: bool}

    # handle pygame touch / mouse events:
    for event in pygame.event.get():
        mc.handle_event(event)

keys_held keys:
    "left", "right", "jump", "fire", "shield", "b2", "arrow", "halo", "pause"
"""

import pygame
import math


C_BTN_BG   = (30,  35,  70, 180)
C_BTN_BD   = (80, 120, 200, 220)
C_BTN_TX   = (255, 220,  50)
C_BTN_HI   = (255, 220,  50,  80)
C_BTN_PRE  = (255, 255, 255, 120)   # pressed highlight


class _Button:
    def __init__(self, x, y, r, label, action):
        self.center = (x, y)
        self.r      = r
        self.label  = label
        self.action = action
        self.pressed = False

    def contains(self, pos):
        dx = pos[0] - self.center[0]
        dy = pos[1] - self.center[1]
        return dx*dx + dy*dy <= self.r*self.r

    def draw(self, surf, font):
        x, y = self.center
        col_bg = C_BTN_PRE if self.pressed else C_BTN_BG
        col_bd = C_BTN_TX  if self.pressed else C_BTN_BD
        # background circle (with alpha)
        tmp = pygame.Surface((self.r*2+4, self.r*2+4), pygame.SRCALPHA)
        pygame.draw.circle(tmp, col_bg, (self.r+2, self.r+2), self.r)
        pygame.draw.circle(tmp, col_bd, (self.r+2, self.r+2), self.r, 2)
        surf.blit(tmp, (x - self.r - 2, y - self.r - 2))
        # label
        s = font.render(self.label, True, C_BTN_TX if not self.pressed else (20,20,20))
        surf.blit(s, s.get_rect(center=(x, y)))


class MobileControls:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.W, self.H = screen.get_size()
        self._font = pygame.font.SysFont("segoeui", 15, bold=True)
        self._font_sm = pygame.font.SysFont("couriernew", 13, bold=True)
        self._buttons: list[_Button] = []
        self._touch_map: dict[int, str] = {}   # finger_id → action
        self._held: dict[str, bool] = {
            a: False for a in
            ["left","right","jump","fire","shield","b2","arrow","halo","pause"]
        }
        self._build_buttons()

    # ── layout ─────────────────────────────────────────────────────────────
    def _build_buttons(self):
        W, H = self.W, self.H
        r_big = 36
        r_sm  = 28

        # ── D-pad  (bottom-left) ──────────────────────────────────────────
        pad_cx = 120
        pad_cy = H - 100
        gap    = r_big + 10

        self._buttons += [
            _Button(pad_cx - gap, pad_cy, r_big, "◀",     "left"),
            _Button(pad_cx + gap, pad_cy, r_big, "▶",     "right"),
            _Button(pad_cx,       pad_cy - gap, r_big, "▲ JUMP", "jump"),
        ]

        # ── action buttons (bottom-right) ─────────────────────────────────
        ax = W - 60
        ay = H - 80
        self._buttons += [
            _Button(ax,        ay,        r_big, "FIRE",    "fire"),
        ]

        # special buttons row above
        sx  = W - 200
        sy  = H - 170
        gap2 = 50
        for i, (lbl, act) in enumerate([
            ("O",  "shield"),
            ("1",  "b2"),
            ("2",  "arrow"),
            ("3",  "halo"),
        ]):
            self._buttons.append(_Button(sx + i*gap2, sy, r_sm, lbl, act))

        # pause – top right
        self._buttons.append(_Button(W - 36, 50, 26, "II", "pause"))

    # ── public API ─────────────────────────────────────────────────────────
    def handle_event(self, event):
        """Feed pygame events here to update button states."""
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
            pos = self._event_pos(event)
            for btn in self._buttons:
                if btn.contains(pos):
                    btn.pressed = True
                    self._held[btn.action] = True
                    if event.type == pygame.FINGERDOWN:
                        self._touch_map[event.finger_id] = btn.action

        elif event.type in (pygame.MOUSEBUTTONUP, pygame.FINGERUP):
            if event.type == pygame.FINGERUP:
                action = self._touch_map.pop(event.finger_id, None)
                if action:
                    self._held[action] = False
                    for btn in self._buttons:
                        if btn.action == action:
                            btn.pressed = False
            else:
                pos = self._event_pos(event)
                for btn in self._buttons:
                    if btn.contains(pos):
                        btn.pressed = False
                        self._held[btn.action] = False

        elif event.type == pygame.FINGERMOTION:
            # handle finger slide onto a new button
            pos = self._event_pos(event)
            old = self._touch_map.get(event.finger_id)
            for btn in self._buttons:
                if btn.contains(pos):
                    if btn.action != old:
                        # release old
                        if old:
                            self._held[old] = False
                            for b in self._buttons:
                                if b.action == old:
                                    b.pressed = False
                        btn.pressed = True
                        self._held[btn.action] = True
                        self._touch_map[event.finger_id] = btn.action
                    break

    def get_keys(self) -> dict:
        """Returns dict of {action: bool} for currently held buttons."""
        return dict(self._held)

    def draw(self):
        for btn in self._buttons:
            f = self._font if len(btn.label) <= 4 else self._font_sm
            btn.draw(self.screen, f)

    # ── helpers ────────────────────────────────────────────────────────────
    def _event_pos(self, event):
        if hasattr(event, 'finger_id'):
            return (int(event.x * self.W), int(event.y * self.H))
        return event.pos
