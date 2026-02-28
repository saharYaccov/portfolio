# 🐍 AI Snake Game — Pathfinding + ML Showcase

A fully AI-controlled Snake game combining A\* pathfinding with a live-trained
Random Forest classifier.  Every game is recorded to CSV; after enough data the
model predicts the best direction and biases the AI's move selection.

---

## 🐍 Snake Game Demo

![Snake Demo]([Projects/snake_game/example/demo.gif](https://github.com/saharYaccov/portfolio/blob/main/Projects/snake_game/example/demo.gif))

[▶️ Watch full video](Projects/snake_game/example/video.mov)

## Project Structure

```
snake_game/
├── main.py              ← Game entry point (run this)
├── requirements.txt
├── README.md
├── Keyboard.md          ← Full keyboard reference
├── snake/
│   ├── snake.py         ← Snake body & collision logic
│   ├── ai.py            ← A* + flood-fill AI controller
│   └── ml_model.py      ← Random Forest model + feature selection
├── board/
│   └── board.py         ← Level layouts & board shapes
├── utils/
│   ├── pathfinding.py   ← A* & flood-fill algorithms
│   └── target.py        ← Random target placement
├── assets/
│   ├── colors.py        ← Dark / light theme palettes
│   └── aura.py          ← Snake glow / aura effects
└── data/                ← Auto-generated game CSVs (up to 10 files)
```

---

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch the game
python main.py
```

---

## Controls

### Game Controls

| Key | Action |
|-----|--------|
| `M` | Toggle dark / light mode |
| `R` | Restart (back to level 1, ML model preserved) |
| `Space` | Advance to next level after completion |
| `Q` / `Esc` | Quit |
| Mouse click | Toggle dark / light mode (button in HUD) |

### Corner Override (Hidden Keys)

| Key | Corner |
|-----|--------|
| `A` | Top-left |
| `Z` | Bottom-left |
| `L` | Top-right |
| `.` | Bottom-right |

### ML Model Controls

| Key | Action |
|-----|--------|
| `+` / `=` | Increase decision tree depth by 1 → retrain |
| `-` | Decrease decision tree depth by 1 → retrain |
| `T` | **Increase active features by 1** (adds next most-important feature) → retrain |
| `Y` | **Decrease active features by 1** (removes least-important active feature) → retrain |

---

## HUD Layout

The HUD is split into **two panels**:

### Top Panel (4 columns)
| Column | Content |
|--------|---------|
| A | ⏱ Timer · 🍎 Score & snake length |
| B | Level name · Goal · ⚠ Survival / 📍 Corner indicators |
| C | 🔄 Rounds · 💀 Deaths · 🐍 Snake rank badge |
| D | 🧠 NN status · 🌲 Tree depth · 🎯 Accuracy · 📐 R² |

### Bottom Panel — 🧬 Feature Box *(new)*
Displays:
- **`Features: N/15  [T/Y]`** — how many features the model currently uses
- **Colored tag per active feature** — shown left-to-right in importance order

---

## Levels

| # | Shape | Description |
|---|-------|-------------|
| 1 | Square | Classic full grid |
| 2 | Circle | Oval arena |
| 3 | Cross | Plus shape |
| 4 | Diamond | Rhombus |
| 5 | Ring | Hollow square corridor |
| 6 | Zigzag | Maze-like corridors |
| 7 | Hourglass | Bowtie shape |
| 8 | Spiral Ring | Dual concentric rings |

---

## AI Strategy

Per tick the AI follows a four-tier decision process:

1. **ML bias** — if trained, the model ranks directions; this ranking breaks ties.
2. **A\* direct path** — shortest path to target, verified by flood-fill safety.
3. **Tail-chase fallback** — follow own tail to buy time when direct path is unsafe.
4. **Survival mode** — pick the neighbour with maximum reachable free space.

---

## Feature Selection (T / Y keys)

The model uses up to **15 features** extracted each tick:

| Feature | Description |
|---------|-------------|
| `danger_up/down/left/right` | Immediate collision in each direction |
| `food_row_sign` / `food_col_sign` | Relative food direction (−1 / 0 / 1) |
| `snake_len_norm` | Body length / walkable area |
| `dir_up/down/left/right` | One-hot current direction |
| `space_up/down/left/right_norm` | Flood-fill free space each direction (normalised) |

**Importance ranking** is recomputed each training run using:
1. **Pearson |r|** — absolute correlation of the feature with the move label
2. **Between-class variance** — how well the feature separates the four directions

Pressing `T` adds the next most-important unused feature.
Pressing `Y` drops the least-important currently-active feature.
Valid range: 1 – 15 features (default: 15).

---

## ML Model Details

- **Algorithm:** Random Forest (50 trees, CART / Gini, NumPy only — no sklearn)
- **Training data:** last 10 games stored as CSVs in `data/`
- **Label:** move direction encoded as 0=UP, 1=DOWN, 2=LEFT, 3=RIGHT
- **Retrain triggers:** game end, `+`, `-`, `T`, `Y`
- **HUD metrics:** Accuracy (train set) · R² (predicted probabilities vs one-hot labels)
