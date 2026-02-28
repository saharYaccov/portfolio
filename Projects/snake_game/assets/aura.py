"""
assets/aura.py
──────────────
Aura / halo rendering for the snake.

Modes by files_loaded:
  0        → normal (theme colours) + danger/corner outline overlays
  1–4      → SSJ1  : golden yellow full body, warm gold glow
  5–9      → SSJ2  : deep black body, bright yellow outline, white lightning
  10–19    → SSJ God : crimson-rose body, deep red glow halo
  20–39    → SSJ Blue: electric azure body, multilayer blue glow corona
  40+      → Ultra  : pure white body, gold tail, yellow lightning + white corona

Danger/corner outlines always draw ON TOP of whatever body colour is active.
"""

from __future__ import annotations
import math
import random
import pygame

# ── Palette ──────────────────────────────────────────────────────────────────

DANGER_COL  = (255,  45,  45)
CORNER_COL  = ( 40, 215, 255)

S1_HEAD     = (255, 240,  40)
S1_BODY     = (215, 170,  10)
S1_GLOW     = (255, 210,   0)

S2_HEAD     = (255, 235,  30)
S2_BODY     = ( 18,  18,  18)
S2_OUTLINE  = (255, 215,   0)
S2_GLOW     = (255, 200,   0)
S2_BOLT     = (255, 255, 255)

SG_HEAD     = (255,  50,  80)
SG_BODY     = (180,  20,  45)
SG_GLOW     = (255,  30,  60)

SB_HEAD     = ( 80, 200, 255)
SB_BODY     = ( 20, 110, 230)
SB_GLOW1    = (100, 210, 255)
SB_GLOW2    = ( 40, 130, 255)

UL_HEAD     = (255, 255, 255)
UL_BODY     = (230, 240, 255)
UL_TAIL     = (255, 200,  20)
UL_CORONA   = (255, 255, 230)
UL_BOLT     = (255, 230,  40)

# ── Snake Level labels & colours ─────────────────────────────────────────────
SNAKE_LEVELS = [
    (0,  "BASE",      (160, 170, 200)),
    (1,  "SSJ",       (255, 220,  30)),
    (3,  "SSJ2",      (255, 200,   0)),
    (5, "SSJ GOD",   (255,  60,  80)),
    (7, "SSJ BLUE",  ( 80, 195, 255)),
    (10, "ULTRA",     (255, 255, 255)),
    (13, "ULTRA PRO",  (255, 127, 127)),
]

def get_snake_level_label(files_loaded: int):
    """Return (label_str, color_tuple) for the HUD snake-level display."""
    result_label, result_color = SNAKE_LEVELS[0][1], SNAKE_LEVELS[0][2]
    for threshold, label, color in SNAKE_LEVELS:
        if files_loaded >= threshold:
            result_label, result_color = label, color
    return result_label, result_color


# ── Mode selection ────────────────────────────────────────────────────────────

def get_aura_mode(files_loaded: int, danger_mode: bool, corner_mode: bool) -> str:
    if files_loaded >= 13:  return "ultra_pro"
    if files_loaded >= 10:  return "ultra"
    if files_loaded >= 7:  return "ssj_blue"
    if files_loaded >= 5:  return "ssj_god"
    if files_loaded >= 3:   return "ssj2"
    if files_loaded >= 1:   return "ssj1"
    if corner_mode:         return "corner"
    if danger_mode:         return "danger"
    return "normal"


# ── Utilities ─────────────────────────────────────────────────────────────────

def _lerp(a, b, t):
    return tuple(int(a[k] * (1 - t) + b[k] * t) for k in range(3))

def _clamp(v, lo=0, hi=255):
    return max(lo, min(hi, int(v)))

def _pulse(blink, speed=3.0, lo=0.35, hi=1.0):
    return lo + (hi - lo) * (0.5 + 0.5 * math.sin(blink * speed))

def _glow_layer(screen, cx, cy, radius, color, alpha):
    r = max(4, int(radius))
    surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
    pygame.draw.circle(surf, (*color, _clamp(alpha)), (r, r), r)
    screen.blit(surf, (cx - r, cy - r), special_flags=pygame.BLEND_RGBA_ADD)


# ── Main draw entry point ─────────────────────────────────────────────────────

def draw_snake_with_aura(
    screen: pygame.Surface,
    body: list,
    ox: int, oy: int, cs: int,
    theme: dict,
    aura_mode: str,
    frame: int,
    blink: float,
):
    total = len(body)
    p     = _pulse(blink)
    br    = max(2, cs // 5)

    # 1. Background corona glow (behind segments)
    _draw_corona(screen, body, ox, oy, cs, aura_mode, p, frame, total)

    # 2. Body segments
    for i, (r, c) in enumerate(body):
        t   = i / max(total - 1, 1)
        pad = max(1, int(cs * 0.07 * t))
        rect = pygame.Rect(
            ox + c * cs + 1 + pad,
            oy + r * cs + 1 + pad,
            cs - 2 - 2 * pad,
            cs - 2 - 2 * pad,
        )
        col, outline_col, outline_w = _segment_style(aura_mode, i, t, total, p, theme)
        pygame.draw.rect(screen, col, rect, border_radius=br)
        if outline_col:
            pygame.draw.rect(screen, outline_col, rect, outline_w, border_radius=br)

    # 3. Danger / corner overlay outline (on top)
    if aura_mode in ("danger", "corner"):
        _draw_state_outline(screen, body, ox, oy, cs, aura_mode, p, total)

    # 4. Lightning bolts
    if aura_mode == "ssj2"  and frame % 5 in (0, 1):
        _draw_lightning(screen, body, ox, oy, cs, S2_BOLT,  count=4, width=2)
    if aura_mode == "ultra" and frame % 4 in (0, 1):
        _draw_lightning(screen, body, ox, oy, cs, UL_BOLT,  count=5, width=2)
        if frame % 8 == 0:
            _draw_lightning(screen, body, ox, oy, cs, (255,255,220), count=2, width=3)


# ── Per-segment colour ────────────────────────────────────────────────────────

def _segment_style(aura_mode, i, t, total, pulse, theme):
    if aura_mode == "ssj1":
        col = _lerp(S1_HEAD, S1_BODY, t)
        outline = _lerp((255, 230, 60), (180, 120, 0), t) if i == 0 else None
        return col, outline, 2

    elif aura_mode == "ssj2":
        col = _lerp(S2_HEAD, (200, 180, 0), t) if i == 0 else _lerp(S2_BODY, (40, 35, 0), t)
        return col, S2_OUTLINE, 2

    elif aura_mode == "ssj_god":
        col = _lerp(SG_HEAD, SG_BODY, t)
        outline = _lerp((255, 120, 100), (100, 0, 20), t) if i <= 1 else None
        return col, outline, 2

    elif aura_mode == "ssj_blue":
        col = _lerp(SB_HEAD, SB_BODY, t)
        if i == 0:      outline = SB_GLOW1
        elif i < 4:     outline = _lerp(SB_GLOW1, SB_GLOW2, i / 4)
        else:           outline = None
        return col, outline, 2

    elif aura_mode == "ultra":
        tail_start = max(1, total - total // 4)
        if i >= tail_start:
            tail_t = (i - tail_start) / max(1, total - tail_start)
            col = _lerp(UL_BODY, UL_TAIL, tail_t)
        else:
            col = UL_HEAD if i == 0 else UL_BODY
        out_col = _lerp((255, 255, 255), (255, 200, 30), pulse)
        return col, out_col, 2

    elif aura_mode == "ultra_pro":
        col = (255, 127, 127) if i == 0 else _lerp((255, 255, 30), (200, 180, 0), t)
        out_col = _lerp((255, 255, 255), (255, 255, 0), pulse)
        return col, out_col, 2

    else:
        col = theme["snake_head"] if i == 0 else _lerp(
            theme["snake_head"], theme["snake_body"], t)
        outline = theme["snake_outline"] if i == 0 else None
        return col, outline, 2


# ── Corona glow ───────────────────────────────────────────────────────────────

def _draw_corona(screen, body, ox, oy, cs, aura_mode, pulse, frame, total):
    configs = {
        "ssj1":     [(S1_GLOW,   cs * 0.9, 35), (S1_GLOW,   cs * 0.5, 55)],
        "ssj2":     [(S2_GLOW,   cs * 1.1, 45), (S2_GLOW,   cs * 0.6, 70)],
        "ssj_god":  [(SG_GLOW,   cs * 1.0, 50), ((255, 60, 100), cs * 0.55, 75)],
        "ssj_blue": [(SB_GLOW1,  cs * 1.2, 50), (SB_GLOW2,  cs * 0.65, 80),
                     ((160, 230, 255), cs * 0.35, 40)],
        "ultra":    [(UL_CORONA, cs * 1.4, 55), ((255, 255, 200), cs * 0.7, 85),
                     ((220, 240, 255), cs * 0.4, 50)],
        "ultra_pro": [((255, 255, 0), cs * 1.6, 60), ((255, 255, 150), cs * 0.9, 90),
                      ((255, 200, 0), cs * 0.5, 60)],
    }
    if aura_mode not in configs:
        return

    layers = configs[aura_mode]
    draw_indices = [0] + list(range(2, total, 2))
    anim = 0.7 + 0.3 * pulse

    for i in draw_indices:
        r, c = body[i]
        t    = i / max(total - 1, 1)
        pcx  = ox + c * cs + cs // 2
        pcy  = oy + r * cs + cs // 2
        fade = 1.0 - t * 0.55

        for color, base_radius, base_alpha in layers:
            radius = int(base_radius * anim * (0.6 + 0.4 * fade))
            alpha  = int(base_alpha  * anim * fade)
            _glow_layer(screen, pcx, pcy, radius, color, alpha)


# ── Danger / corner outline ───────────────────────────────────────────────────

def _draw_state_outline(screen, body, ox, oy, cs, aura_mode, pulse, total):
    col        = DANGER_COL if aura_mode == "danger" else CORNER_COL
    alpha_base = int(160 + 60 * pulse)

    for i, (r, c) in enumerate(body):
        t   = i / max(total - 1, 1)
        a   = int(alpha_base * (1 - t * 0.65))
        pad = max(1, int(cs * 0.07 * t))
        sz  = cs - 2 * pad + 8
        surf = pygame.Surface((sz, sz), pygame.SRCALPHA)
        br   = max(4, cs // 4)
        pygame.draw.rect(surf, (*col, a // 2),
                         pygame.Rect(0, 0, sz, sz), 5, border_radius=br + 2)
        pygame.draw.rect(surf, (*col, a),
                         pygame.Rect(2, 2, sz - 4, sz - 4), 2, border_radius=br)
        screen.blit(surf, (ox + c * cs - 4 + pad, oy + r * cs - 4 + pad))


# ── Lightning ─────────────────────────────────────────────────────────────────

def _draw_lightning(screen, body, ox, oy, cs, color, count=3, width=2):
    if len(body) < 2:
        return
    weights = [max(0.1, 1.0 - (i / len(body)) * 0.7) for i in range(len(body))]
    total_w = sum(weights)
    weights = [w / total_w for w in weights]

    chosen = random.choices(range(len(body)), weights=weights, k=min(count, len(body)))

    for idx in chosen:
        r, c = body[idx]
        cx = ox + c * cs + cs // 2
        cy = oy + r * cs + cs // 2

        for _ in range(random.randint(1, 2)):
            angle  = random.uniform(0, 2 * math.pi)
            length = random.randint(cs // 2, int(cs * 1.6))
            steps  = random.randint(4, 7)
            pts    = [(cx, cy)]
            for s in range(1, steps + 1):
                progress = s / steps
                jitter   = cs * 0.35 * (1 - progress * 0.4)
                nx = cx + math.cos(angle) * length * progress + random.uniform(-jitter, jitter)
                ny = cy + math.sin(angle) * length * progress + random.uniform(-jitter, jitter)
                pts.append((int(nx), int(ny)))
            if len(pts) >= 2:
                pygame.draw.lines(screen, color, False, pts, width)
                if width > 1:
                    pygame.draw.lines(screen, (255, 255, 255), False, pts, 1)
