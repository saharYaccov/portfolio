# Freedom Force: The Reckoning

A 2D side-scrolling platformer with classic Mario-style mechanics, special power-ups, a transforming protagonist, and an epic 6-stage boss battle.

---

## Table of Contents

1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Running the Game](#running-the-game)
4. [Project Structure](#project-structure)
5. [Gameplay Overview](#gameplay-overview)
6. [Characters & Assets](#characters--assets)
7. [Power-Ups & Items](#power-ups--items)
8. [Boss Fight (Stage 6)](#boss-fight-stage-6)
9. [Controls Summary](#controls-summary)
10. [Architecture Notes](#architecture-notes)

---

## Requirements

- Python 3.10+
- pygame 2.5.0+

---

## Installation

```bash
# 1. Clone or download the project
git clone <repo-url>
cd platformer

# 2. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate.bat     # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Running the Game

```bash
python main.py
```

Press **Enter** on the title screen to begin.

---

## Project Structure

```
platformer/
│
├── main.py                  # Entry point
├── requirements.txt
├── README.md
├── keyboard.md              # Full controls reference
│
├── src/                     # All game logic
│   ├── game_loop.py         # Main loop, state machine, camera
│   ├── player.py            # Player movement, transformation, damage
│   ├── enemy.py             # Enemy patrol AI, group utilities
│   ├── boss.py              # Stage 6 boss mechanics
│   ├── projectiles.py       # Player lasers, boss shots, nuclear warning
│   ├── powerups.py          # All collectible items + BombInventory
│   ├── level_manager.py     # Stage definitions, tile/entity parsing
│   ├── hud.py               # HUD / UI rendering
│   └── asset_loader.py      # Asset loading with procedural fallbacks
│
├── assets/                  # Static game assets (optional, hand-crafted)
│   ├── powerups/            # antibomb.png, energy_sphere.png, etc.
│   └── ui/                  # door.png
│
├── current_ok_boys/         # Player sprites
│   ├── bb.png               # Default player state
│   └── trump.png            # Transformed state (20-second power-up)
│
├── current_enemy/           # Enemy sprites (add as many as you like)
│   ├── enemy1.png
│   └── ...                  # All .png/.jpg files here are used randomly
│
└── final_enemy_iran/        # Final boss sprite
    └── boss.png
```

> **Tip:** If sprite images are missing, the game auto-generates coloured placeholder sprites so it always runs out of the box.

---

## Gameplay Overview

### Stages 1–5
- Each stage lasts **4 minutes**.
- Navigate platforms, defeat enemies, collect items.
- Reach the glowing **"NEXT STAGE" door** to advance.
- Running out of time counts as a stage failure.

### Lives & Stamina
- The player has **3 lives**.
- Each life has a **stamina bar** (default 3 hits).
- Collecting **Energy Spheres** permanently increases your max stamina by 1.
- Losing all stamina on one life costs you one life; you respawn at the stage start.
- Losing all 3 lives = **Game Over**.

### Trump Transformation
- Collect a **golden orb** to enter Trump Mode for 20 seconds.
- In Trump Mode the player is **immune to all enemy contact**.
- A bar at the bottom-left shows remaining transform time.

---

## Characters & Assets

### Player (`current_ok_boys/`)
Place your character images here:
| File          | Used for                          |
|---------------|-----------------------------------|
| `bb.png`      | Default character state           |
| `trump.png`   | Transformed (immune) state        |

Supported formats: `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`

### Enemies (`current_enemy/`)
Place any number of enemy images here. The game randomly picks from every file in this folder when spawning enemies. All enemies patrol horizontally and attempt to touch the player.

### Boss (`final_enemy_iran/`)
Place the final boss image here (first image file found is used).

---

## Power-Ups & Items

| Item            | Effect                                              | Quantity  |
|-----------------|-----------------------------------------------------|-----------|
| Energy Sphere   | +1 to max stamina (failure tolerance)               | 1 per stage (5 total) |
| Golden Orb      | 20-second Trump transformation (immunity)           | 2 per stage           |
| Anti-Bomb       | Required to survive boss nuclear attacks (press O)  | 1 per stage, 2 in S5 (6 total) |
| B2 Bomb `[1]`   | Instantly destroys ALL enemies on current stage     | 3 total   |
| Arrow Bomb `[2]`| Destroys enemies within 3-tile radius               | 20 total  |
| Halo Bomb `[3]` | Destroys ~half of the ground tiles                  | 2 total   |

---

## Boss Fight (Stage 6)

The final boss is stationary but extremely powerful.

| Stat              | Value                              |
|-------------------|------------------------------------|
| HP                | 500                                |
| Laser hits needed | 50 (10 damage per hit)             |
| Regular attack    | Volley of blue/green orbs every 10s|
| Nuclear attacks   | 5 total, triggered at HP thresholds|

### Nuclear Bomb Mode
- The boss enters Nuclear Bomb Mode 5 times during the fight.
- A **red flashing screen** and a 5-second countdown warn you.
- Press **O** immediately to activate your anti-bomb shield.
- Each use consumes **1 anti-bomb item**.
- If you don't have an anti-bomb, or the timer expires → you take a hit.
- Collect 6 anti-bombs across stages 1–5 to have a safety margin.

---

## Controls Summary

| Key     | Action                                  |
|---------|-----------------------------------------|
| A / D   | Move left / right                       |
| Space   | Jump                                    |
| L       | Fire laser                              |
| O       | Activate anti-bomb shield               |
| 1       | Deploy B2 Bomb                          |
| 2       | Deploy Arrow Bomb                       |
| 3       | Deploy Halo Bomb                        |
| P       | Pause / Resume                          |
| R       | Restart (Game Over screen only)         |
| Enter   | Start game (title screen)               |

See [keyboard.md](keyboard.md) for extended notes.

---

## Architecture Notes

The codebase is split into focused, single-responsibility modules:

| Module             | Responsibility                                         |
|--------------------|--------------------------------------------------------|
| `game_loop.py`     | State machine, render pipeline, input routing, camera |
| `player.py`        | Physics, movement, transformation timer, damage model |
| `enemy.py`         | Patrol AI, group destroy helpers                      |
| `boss.py`          | HP tracking, volley firing, nuclear trigger logic     |
| `projectiles.py`   | Player laser, boss shot, nuclear warning data class   |
| `powerups.py`      | All collectible types + BombInventory                 |
| `level_manager.py` | ASCII map parsing → sprite groups, stage timer        |
| `hud.py`           | Stateless HUD renderer, all overlay screens           |
| `asset_loader.py`  | File loading with procedural fallbacks, enemy randomisation |

Adding a new stage: append a new ASCII map to `STAGE_MAPS` in `level_manager.py` and adjust the stage count.  
Adding a new enemy type: drop an image into `current_enemy/` — no code changes needed.  
Adding a new power-up: subclass `PowerUp` in `powerups.py`, add a symbol to the map legend and a `_parse` branch in `level_manager.py`.
