# Freedom Force: The Reckoning

A 2D side-scrolling platformer with classic Mario-style mechanics, special power-ups, a transforming protagonist, difficulty levels, ML-powered analytics, and an epic boss battle with dynamic enemies.

---

## Table of Contents

1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Running the Game](#running-the-game)
4. [Project Structure](#project-structure)
5. [Gameplay Overview](#gameplay-overview)
6. [Difficulty Levels](#difficulty-levels)
7. [Characters & Assets](#characters--assets)
8. [Power-Ups & Items](#power-ups--items)
9. [Boss Fight (Stage 11)](#boss-fight-stage-11)
10. [Controls Summary](#controls-summary)
11. [ML Dashboard & Statistics](#ml-dashboard--statistics)
12. [Architecture Notes](#architecture-notes)

---

## Requirements

- Python 3.10+
- pygame 2.5.0+
- scikit-learn (for ML features)
- numpy
- pandas

---

## Installation

```bash
# 1. Clone or download the project
cd Freedom-Force-The-Reckoning-game

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

### First Launch
1. **Device Selection**: Choose PC or Mobile controls
2. **Difficulty Selection**: Choose Easy, Middle, or Hard
3. Press **Space** to start the game

---

## Project Structure

```
Freedom-Force-The-Reckoning-game/
│
├── main.py                  # Entry point
├── requirements.txt
├── README_explain.md        # This file
├── keyboard.md              # Full controls reference
│
├── src/                     # All game logic
│   ├── game_loop.py         # Main loop, state machine, camera
│   ├── player.py            # Player movement, transformation, damage
│   ├── enemy.py             # Enemy patrol AI, Extra enemies, group utilities
│   ├── boss.py              # Stage 11 boss mechanics with ML prediction
│   ├── projectiles.py       # Player lasers, boss shots, nuclear warning
│   ├── powerups.py          # All collectible items + BombInventory
│   ├── level_manager.py     # 11 stage definitions, tile/entity parsing
│   ├── hud.py               # HUD / UI rendering
│   ├── asset_loader.py      # Asset loading with procedural fallbacks
│   ├── stats_recorder.py    # Statistics tracking for ML
│   ├── kill_tracker.py      # Enemy kill tracking
│   └── screens/             # Screen modules
│       ├── title_screen.py  # Title screen with device & difficulty selection
│       ├── rules_screen.py  # Rules and help screen
│       ├── about_screen.py  # Developer information
│       ├── ml_dashboard.py  # ML analytics dashboard
│       └── mobile_controls.py # Mobile on-screen controls
│
├── assets/                  # Static game assets
│   ├── background.png       # Game background image
│   ├── sounds/             
│   │   └── background_music.mp3  # Background music (loops)
│   ├── powerups/           # antibomb.png, energy_sphere.png, etc.
│   └── ui/                 # door.png
│
├── current_ok_boys/         # Player sprites
│   ├── bb.png              # Default player state
│   └── trump.png           # Transformed state (20-second power-up)
│
├── current_enemy/           # Enemy sprites (randomly selected)
│   ├── Abdul-Malik al-Houthi.png
│   ├── Nasrallah.png
│   └── ...                 # All .png files here are used randomly
│
├── final_enemy_iran/        # Final boss sprite
│   └── boss.png
│
├── data/                    # Game data and statistics
│   └── record.csv          # Player statistics and scores
│
└── machine_learning/        # ML analysis (auto-generated)
    ├── best_model.pkl
    ├── model_analysis.txt
    ├── plots/              # Performance visualization charts
    └── best_generalizer/
```

> **Tip:** If sprite images are missing, the game auto-generates colored placeholder sprites so it always runs out of the box.

---

## Gameplay Overview

### Game Structure
- **10 Regular Stages** (Stages 1–10)
- **1 Boss Stage** (Stage 11)

### Stages 1–10
- Each stage lasts **4 minutes**.
- Navigate platforms, defeat enemies, collect items.
- Face **Extra Enemies** (blue soldiers) that vary by difficulty.
- Reach the glowing **"NEXT STAGE" door** to advance.
- Running out of time counts as a stage failure.

### Lives & Stamina
- The player has **3 lives**.
- Each life has a **stamina bar** (default 3 hits).
- Collecting **Energy Spheres** permanently increases your max stamina by 1.
- Losing all stamina on one life costs you one life; you respawn at the stage start.
- Losing all 3 lives = **Game Over**.

### Trump Transformation
- Collect a **golden Activation Orb** to enter Trump Mode for 20 seconds.
- In Trump Mode the player is **immune to all enemy contact**.
- A visual glow effect indicates active transformation.
- A bar at the bottom shows remaining transform time.

---

## Difficulty Levels

Choose your difficulty at the start. This affects the entire game:

| Difficulty | Extra Enemies/Stage | Boss Soldiers | Enemy Fire Rate |
|------------|--------------------|--------------|-----------------| 
| **Easy**   | 4 blue soldiers    | 2 shooters   | Normal          |
| **Middle** | 8 blue soldiers    | 4 shooters   | Normal          |
| **Hard**   | 12 blue soldiers   | 10 shooters  | 30% faster      |

### Extra Enemies (Blue Soldiers)
- Appear in all regular stages (1–10)
- **3 HP** each
- Fire **3 blue laser shots** at the player
- Their shots are **blocked by platforms** (use cover!)
- More challenging than regular enemies

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

| Item            | Symbol | Effect                                              | Quantity  |
|-----------------|--------|-----------------------------------------------------|-----------|
| Energy Sphere   | `S`    | +1 to max stamina (failure tolerance)               | Multiple per stage |
| Activation Orb  | `O`    | 20-second Trump transformation (immunity)           | Multiple per stage |
| Anti-Bomb       | `A`    | Required to survive boss nuclear attacks (press O)  | Scattered across stages |
| B2 Bomb         | `B`    | Instantly destroys ALL enemies on current stage     | 3 total   |
| Arrow Bomb      | `R`    | Destroys enemies within 3-tile radius               | 20 total  |
| Halo Bomb       | `H`    | Destroys ~half of the ground tiles                  | 2 total   |
| Weapon Pickup   | `W`    | Triggers Trump transformation                       | Rare      |
| Damage X        | `X`    | Damages player (avoid!)                             | Scattered |
| Ammo Pickup     | `M`    | Adds 20 laser shots                                 | Scattered |

---

## Boss Fight (Stage 11)

The final boss is stationary but extremely powerful, with **ML-powered movement prediction**.

### Boss Stats
| Stat              | Value                              |
|-------------------|------------------------------------|
| HP                | 500                                |
| Laser hits needed | 50 (10 damage per hit)             |
| Regular attack    | Volley of blue/green orbs (adaptive)|
| Nuclear attacks   | Multiple, triggered by HP AND time |
| Difficulty Adds   | 2-10 shooting soldiers (based on difficulty) |

### Boss AI Features
- **ML Movement Prediction**: Uses Random Forest to predict player position
- **Adaptive Firing**: Volley frequency and size change based on remaining HP
- **Dual Trigger System**: Nuclear attacks trigger both at HP thresholds AND every 30 seconds

### Nuclear Bomb Mode
- The boss enters Nuclear Bomb Mode multiple times during the fight.
- A **red flashing screen** and a 5-second countdown warn you.
- Press **O** immediately to activate your anti-nuclear shield.
- Each use consumes **1 anti-bomb item**.
- If you don't have an anti-bomb, or the timer expires → you take a hit.
- Collect enough anti-bombs across stages 1–10 to survive all attacks.

### Boss Stage Soldiers
In addition to the boss itself, you face shooting soldiers:
- **Easy**: 2 soldiers
- **Middle**: 4 soldiers
- **Hard**: 10 soldiers

These soldiers behave like Extra Enemies (3 HP, fire 3 shots each).

---

## Controls Summary

### Main Controls
| Key     | Action                                  |
|---------|-----------------------------------------|
| A / D   | Move left / right                       |
| Space   | Jump                                    |
| L       | Fire laser                              |
| O       | Activate anti-nuclear shield            |
| 1       | Deploy B2 Bomb                          |
| 2       | Deploy Arrow Bomb                       |
| 3       | Deploy Halo Bomb                        |
| P       | Pause / Resume                          |

### End Screen Controls
| Key     | Action                                  |
|---------|-----------------------------------------|
| R       | Restart (Game Over screen only)         |
| S       | Save score to database                  |
| M       | Open ML Dashboard                       |

### Title Screen Controls
| Key     | Action                                  |
|---------|-----------------------------------------|
| Space   | Start game                              |
| E       | Select Easy difficulty                  |
| M       | Select Middle difficulty / Mute music   |
| H       | Select Hard difficulty                  |
| R / F1  | Rules / Help                            |
| A       | About Developer                         |
| 1       | Select PC mode                          |
| 2       | Select Mobile mode                      |

See [keyboard.md](keyboard.md) for complete controls reference.

---

## ML Dashboard & Statistics

### Accessing the Dashboard
Press **M** on the Game Over or Victory screen to open the ML Dashboard.

### Features
1. **Score Prediction**: ML model predicts your final score based on performance
2. **Performance Metrics**: 
   - Enemies killed
   - Extra enemies eliminated
   - Stages completed
   - Accuracy rates
   - Survival time
3. **Feature Importance**: See which actions most affect your score
4. **Historical Analysis**: View trends and patterns from previous games
5. **Visual Charts**: 
   - Score distribution
   - Predicted vs actual performance
   - Correlation matrices
   - Residual analysis

### Statistics Tracked
- Laser shots fired
- Enemies killed (by type)
- Extra enemies eliminated
- Power-ups collected
- Bombs used
- Trump activations
- Lives lost
- Time survived
- Stages completed
- Final outcome

### Saving Scores
Press **S** on the end screen to save your performance to `data/record.csv`. This data feeds the ML model for better predictions.

---

## Architecture Notes

The codebase is split into focused, single-responsibility modules:

### Core Game Modules
| Module             | Responsibility                                         |
|--------------------|--------------------------------------------------------|
| `game_loop.py`     | State machine, render pipeline, input routing, camera, Extra enemy management |
| `player.py`        | Physics, movement, transformation timer, damage model |
| `enemy.py`         | Patrol AI, Extra enemy class, group destroy helpers  |
| `boss.py`          | HP tracking, ML prediction, volley firing, nuclear trigger logic |
| `projectiles.py`   | Player laser, boss shot, Extra enemy shots, nuclear warning |
| `powerups.py`      | All collectible types + BombInventory                 |
| `level_manager.py` | 11 ASCII map definitions → sprite groups, stage timer |
| `hud.py`           | Stateless HUD renderer, all overlay screens           |
| `asset_loader.py`  | File loading with procedural fallbacks, enemy randomization |

### Statistics & ML
| Module             | Responsibility                                         |
|--------------------|--------------------------------------------------------|
| `stats_recorder.py`| Track all game events and calculate scores           |
| `kill_tracker.py`  | Record enemy kills and generate reports               |
| `ml_dashboard.py`  | Interactive ML analytics visualization                |

### Screen Management
| Module              | Responsibility                                        |
|---------------------|-------------------------------------------------------|
| `title_screen.py`   | Device selection, difficulty selection, music toggle |
| `rules_screen.py`   | Game rules and help information                      |
| `about_screen.py`   | Developer information                                |
| `mobile_controls.py`| On-screen touch controls overlay                     |

### Extensibility

**Adding a new stage**: Append a new ASCII map to `STAGE_MAPS` in `level_manager.py` and adjust the stage count.

**Adding a new enemy type**: Drop an image into `current_enemy/` — no code changes needed.

**Adding a new power-up**: 
1. Subclass `PowerUp` in `powerups.py`
2. Add a symbol to the map legend
3. Add a `_parse` branch in `level_manager.py`

**Adjusting difficulty**: Modify `NUM_EXTRA_PER_STAGE` in `enemy.py` or adjust the difficulty selection in `title_screen.py`.

---

## Credits

Developed with passion for classic platformers and modern ML integration.

For questions or support, see the About screen (press `A` on title screen).

---

**Enjoy the game and may your reflexes be sharp! 🎮**
