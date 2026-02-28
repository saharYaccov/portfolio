# 🐍 AI Snake Game — Pathfinding Showcase

A fully AI-controlled Snake game with A* pathfinding, flood-fill safety checking,
multiple board shapes, dark/light mode, and real-time path visualisation.

---

## Project Structure

```
snake_game/
├── main.py              ← Game entry point (run this)
├── requirements.txt
├── snake/
│   ├── __init__.py
│   ├── snake.py         ← Snake body & collision logic
│   └── ai.py            ← A* + flood-fill AI controller
├── board/
│   ├── __init__.py
│   └── board.py         ← Level layouts & board shapes
├── utils/
│   ├── __init__.py
│   ├── pathfinding.py   ← A* & flood-fill algorithms
│   └── target.py        ← Random target placement
└── assets/
    ├── __init__.py
    └── colors.py        ← Dark / light theme palettes
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

| Key | Action |
|-----|--------|
| `M` | Toggle dark / light mode |
| `R` | Restart after game over |
| `Space` | Advance to next level (after level complete) |
| `Q` / `Esc` | Quit |
| Mouse click on button | Toggle dark / light mode |

---

## Levels

| # | Shape | Description |
|---|-------|-------------|
| 1 | Square | Classic full grid |
| 2 | Circle | Oval arena |
| 3 | Cross | Dalton / plus shape |
| 4 | Diamond | Rhombus |
| 5 | Ring | Hollow square corridor |
| 6 | Zigzag | Maze-like corridors |
| 7 | Hourglass | Bowtie / hourglass |
| 8 | Spiral Ring | Dual concentric rings |

---

## AI Strategy

The AI uses a three-tier decision process each tick:

1. **A\* direct path** — Find the shortest path to the target, then verify the
   resulting board position via flood-fill to ensure the snake has enough free
   space and won't trap itself.

2. **Tail-chase fallback** — If the direct path would trap the snake, follow
   the snake's own tail to buy time until a safe path opens.

3. **Survival mode** — If neither option yields a safe path, pick the neighbour
   cell that maximises reachable free space (pure escape heuristic).

The **AI trail** (faint blue/purple cells) shows the currently planned path.
An ⚠ SURVIVAL MODE warning appears in the HUD when the AI is in fallback mode.

---

## HUD

- ⏱ **Timer** — elapsed game time (mm:ss.cs)  
- 🍎 **Score** — targets eaten / snake length  
- **Level label** and shape description  
- **Goal** — target snake length to advance  
- **⚠ Survival Mode** indicator (when AI is in fallback)
