"""
snake/ml_model.py
─────────────────
Random Forest Classifier that learns from the last N games.

Architecture: configurable max_depth (default 6), 50 trees, built with NumPy only.
  +/-  hotkeys change max_depth and retrain immediately.

Features (15 total):
  danger_up/down/left/right        — immediate collision in each dir
  food_row_sign / food_col_sign    — relative food direction (-1/0/1)
  snake_len_norm                   — body length / walkable area
  dir_up/down/left/right           — one-hot current direction
  space_up/down/left/right_norm    — flood-fill free space each dir

Label: int 0-3  (UP=0, DOWN=1, LEFT=2, RIGHT=3)
"""

from __future__ import annotations
import os, csv, math
from typing import Optional
import numpy as np

# ── Direction encoding ───────────────────────────────────────────────────────
DIRECTIONS = {(-1,0):0, (1,0):1, (0,-1):2, (0,1):3}
DIR_NAMES  = ["UP","DOWN","LEFT","RIGHT"]
DIR_DELTAS = [(-1,0),(1,0),(0,-1),(0,1)]

FEATURE_COLS = [
    "danger_up","danger_down","danger_left","danger_right",
    "food_row_sign","food_col_sign","snake_len_norm",
    "dir_up","dir_down","dir_left","dir_right",
    "space_up_norm","space_down_norm","space_left_norm","space_right_norm",
]
N_FEATURES          = len(FEATURE_COLS)   # 15
N_CLASSES           = 4
MIN_ACTIVE_FEATURES = 1
MAX_ACTIVE_FEATURES = N_FEATURES
MAX_GAMES_STORED = 15
DATA_DIR   = os.path.join(os.path.dirname(__file__), "..", "data")
INDEX_FILE = os.path.join(DATA_DIR, "game_index.txt")


# ── Feature extraction ───────────────────────────────────────────────────────

def _flood_fill_fast(start, occupied, walkable, limit=80):
    if start not in walkable or start in occupied:
        return 0
    visited, queue, count = {start}, [start], 0
    while queue and count < limit:
        cur = queue.pop(); count += 1
        r, c = cur
        for dr, dc in DIR_DELTAS:
            nb = (r+dr, c+dc)
            if nb in walkable and nb not in occupied and nb not in visited:
                visited.add(nb); queue.append(nb)
    return count


def extract_features(head, body, target, walkable, prev_dir, board_size):
    occupied = set(body)
    tail     = body[-1] if body else head
    dangers, spaces = [], []
    for dr, dc in DIR_DELTAS:
        nb    = (head[0]+dr, head[1]+dc)
        wall  = nb not in walkable
        body_ = nb in occupied and nb != tail
        dangers.append(1.0 if (wall or body_) else 0.0)
        free = _flood_fill_fast(nb, occupied-{tail}, walkable) if not (wall or body_) else 0
        spaces.append(free / max(len(walkable), 1))
    food_row  = math.copysign(1, target[0]-head[0]) if target[0]!=head[0] else 0.0
    food_col  = math.copysign(1, target[1]-head[1]) if target[1]!=head[1] else 0.0
    len_norm  = len(body) / max(len(walkable), 1)
    dir_idx   = DIRECTIONS.get(prev_dir, 3)
    dir_onehot = [1.0 if i==dir_idx else 0.0 for i in range(4)]
    return dangers + [food_row, food_col, len_norm] + dir_onehot + spaces


# ── Decision Tree (CART, Gini) ────────────────────────────────────────────────

class _DecisionTree:
    def __init__(self, max_depth=6, min_samples_split=4, max_features=None, rng=None):
        self.max_depth         = max_depth
        self.min_samples_split = min_samples_split
        self.max_features      = max_features
        self.rng               = rng or np.random.default_rng()
        self.feat_idx: list  = []
        self.threshold: list = []
        self.left:  list     = []
        self.right: list     = []
        self.value: list     = []

    def _gini(self, y):
        n = len(y)
        if n == 0: return 0.0
        p = np.bincount(y, minlength=N_CLASSES) / n
        return 1.0 - float(np.dot(p, p))

    def _best_split(self, X, y):
        n, n_feat = X.shape
        mf        = self.max_features or n_feat
        feats     = self.rng.choice(n_feat, size=min(mf, n_feat), replace=False)
        pg        = self._gini(y)
        best_gain = -1.0; best_f = best_t = None
        for f in feats:
            vals = X[:, f]
            uniq = np.unique(vals)
            if len(uniq) < 2: continue
            for thresh in (uniq[:-1]+uniq[1:])/2:
                lm = vals <= thresh; rm = ~lm
                nl, nr = lm.sum(), rm.sum()
                if nl==0 or nr==0: continue
                gain = pg - (nl/n*self._gini(y[lm]) + nr/n*self._gini(y[rm]))
                if gain > best_gain:
                    best_gain=gain; best_f=f; best_t=thresh
        return best_f, best_t

    def _build(self, X, y, depth):
        nid = len(self.feat_idx)
        self.feat_idx.append(-1); self.threshold.append(0.0)
        self.left.append(-1);     self.right.append(-1)
        self.value.append(None)
        if depth>=self.max_depth or len(y)<self.min_samples_split or len(np.unique(y))==1:
            c = np.bincount(y, minlength=N_CLASSES).astype(float)
            self.value[nid] = c/c.sum(); return nid
        f, t = self._best_split(X, y)
        if f is None:
            c = np.bincount(y, minlength=N_CLASSES).astype(float)
            self.value[nid] = c/c.sum(); return nid
        mask = X[:,f] <= t
        self.feat_idx[nid]=f; self.threshold[nid]=t
        self.left[nid]  = self._build(X[mask],  y[mask],  depth+1)
        self.right[nid] = self._build(X[~mask], y[~mask], depth+1)
        return nid

    def fit(self, X, y):
        self._build(X, y, 0)

    def predict_proba_one(self, x):
        node = 0
        while self.value[node] is None:
            node = self.left[node] if x[self.feat_idx[node]]<=self.threshold[node] else self.right[node]
        return self.value[node]

    def predict_proba(self, X):
        return np.array([self.predict_proba_one(x) for x in X])


# ── Random Forest ─────────────────────────────────────────────────────────────

class RandomForestClassifier:
    """50 trees, bootstrap sampling, sqrt features per split."""
    def __init__(self, n_estimators=30, max_depth=6):
        self.n_estimators = n_estimators
        self.max_depth    = max_depth
        self.trees: list[_DecisionTree] = []
        self._rng = np.random.default_rng(42)

    def fit(self, X, y):
        self.trees = []
        n  = X.shape[0]
        mf = max(1, int(math.sqrt(X.shape[1])))
        for _ in range(self.n_estimators):
            idx  = self._rng.integers(0, n, size=n)
            tree = _DecisionTree(
                max_depth=self.max_depth, max_features=mf,
                rng=np.random.default_rng(self._rng.integers(0, 2**31)))
            tree.fit(X[idx], y[idx])
            self.trees.append(tree)

    def predict_proba(self, X):
        avg = np.zeros((X.shape[0], N_CLASSES))
        for t in self.trees:
            avg += t.predict_proba(X)
        return avg / len(self.trees)

    def predict(self, X):
        return np.argmax(self.predict_proba(X), axis=1)


# ── SnakeMLModel ──────────────────────────────────────────────────────────────

class SnakeMLModel:
    """
    Manages game CSVs + a RandomForestClassifier.
    max_depth  ← controlled by +/- hotkeys (shown as 'Depth' in HUD).
    n_layers   ← alias for HUD compatibility.
    """

    def __init__(self, max_depth: int = 6):
        self.max_depth         = max_depth
        self.n_layers          = max_depth          # HUD alias
        self.forest:           Optional[RandomForestClassifier] = None
        self.trained           = False
        self.accuracy          = 0.0
        self.r2_score          = 0.0
        self.game_count        = 0
        self.files_loaded      = 0
        # ── feature selection ─────────────────────────────────────────────────
        self.n_active_features = N_FEATURES       # start with all 15 features
        self.feature_order:    list[int] = list(range(N_FEATURES))  # importance order
        os.makedirs(DATA_DIR, exist_ok=True)
        self._load_game_count()

    def _load_game_count(self):
        if os.path.exists(INDEX_FILE):
            with open(INDEX_FILE) as f:
                try:    self.game_count = int(f.read().strip())
                except: self.game_count = 0

    def _save_game_count(self):
        with open(INDEX_FILE, "w") as f:
            f.write(str(self.game_count))

    def _csv_path(self, idx):
        return os.path.join(DATA_DIR, f"game_data_{idx}.csv")

    # ── save ─────────────────────────────────────────────────────────────────

    def save_game_data(self, records):
        if not records: return
        self.game_count += 1
        self._save_game_count()
        path = self._csv_path(self.game_count)
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FEATURE_COLS+["label"])
            w.writeheader(); w.writerows(records)
        print(f"[RF] Game {self.game_count}: {len(records)} steps → {os.path.basename(path)}")
        old = self._csv_path(self.game_count - MAX_GAMES_STORED)
        if self.game_count > MAX_GAMES_STORED and os.path.exists(old):
            os.remove(old)

    # ── discover CSVs ────────────────────────────────────────────────────────

    def _discover_csv_files(self):
        found = []
        if not os.path.isdir(DATA_DIR): return found
        for fname in os.listdir(DATA_DIR):
            if fname.startswith("game_data_") and fname.endswith(".csv"):
                stem = fname[len("game_data_"):-len(".csv")]
                try:    found.append((int(stem), os.path.join(DATA_DIR, fname)))
                except: pass
        found.sort(key=lambda x: x[0])
        return found

    # ── train ────────────────────────────────────────────────────────────────

    def load_and_train(self) -> bool:
        all_files = self._discover_csv_files()
        if all_files:
            disk_max = all_files[-1][0]
            if disk_max > self.game_count:
                self.game_count = disk_max; self._save_game_count()

        rows, loaded_games = [], []
        for game_idx, fpath in all_files:
            try:
                with open(fpath, newline="") as f:
                    game_rows = [r for r in csv.DictReader(f)
                                 if all(c in r for c in FEATURE_COLS+["label"])]
                if game_rows:
                    rows.extend(game_rows); loaded_games.append(game_idx)
            except Exception as e:
                print(f"[RF] Warning: {e}")

        self.files_loaded = len(loaded_games)
        if len(rows) < 20:
            print(f"[RF] Not enough data ({len(rows)} rows)")
            return False

        X_full = np.array([[float(r[c]) for c in FEATURE_COLS] for r in rows])
        y      = np.array([int(r["label"]) for r in rows])
        if len(set(y)) < 2:
            print("[RF] Not enough label variety"); return False

        # ── Compute feature importance order (p-value + correlation) ─────────
        self.feature_order = self._compute_feature_order(X_full, y)

        # ── Select only the top n_active_features ────────────────────────────
        active_idx = self.feature_order[:self.n_active_features]
        X = X_full[:, active_idx]

        self.forest = RandomForestClassifier(n_estimators=50, max_depth=self.max_depth)
        self.forest.fit(X, y)
        self.trained = True

        # Accuracy
        preds = self.forest.predict(X)
        self.accuracy = float(np.mean(preds == y))

        # R²  (one-hot labels vs predicted probabilities, averaged over classes)
        proba  = self.forest.predict_proba(X)
        y_oh   = np.zeros((len(y), N_CLASSES))
        y_oh[np.arange(len(y)), y] = 1.0
        ss_res = np.sum((y_oh - proba)**2)
        ss_tot = np.sum((y_oh - y_oh.mean(axis=0))**2)
        self.r2_score = float(1.0 - ss_res / (ss_tot + 1e-10))

        active_names = [FEATURE_COLS[i] for i in active_idx]
        print(f"[RF] depth={self.max_depth}  features={self.n_active_features}/{N_FEATURES}"
              f"  acc={self.accuracy:.1%}  R²={self.r2_score:.3f}")
        print(f"[RF] Active features: {active_names}")
        return True

    # ── feature importance ────────────────────────────────────────────────────

    def _compute_feature_order(self, X: np.ndarray, y: np.ndarray) -> list[int]:
        """
        Rank features by combined score of:
          1. Chi² / F-statistic p-value proxy: variance of per-class means
          2. Absolute Pearson correlation with label
        Lower rank = more important.
        """
        n_feat   = X.shape[1]
        scores   = np.zeros(n_feat)
        y_float  = y.astype(float)
        y_mean   = y_float.mean()
        y_std    = y_float.std() + 1e-10
        classes  = np.unique(y)

        for f in range(n_feat):
            col       = X[:, f]
            col_std   = col.std() + 1e-10
            # Pearson |r| with label
            corr      = abs(float(np.corrcoef(col, y_float)[0, 1]))
            # Between-class variance of feature means (F-stat numerator proxy)
            class_means = np.array([col[y == c].mean() if (y == c).sum() > 0 else 0.0
                                    for c in classes])
            between_var = float(class_means.var())
            # Combined score (higher = more important)
            scores[f]  = corr + between_var / (col_std + 1e-10)

        order = list(np.argsort(-scores))   # descending importance
        print(f"[RF] Feature importance order: {[FEATURE_COLS[i] for i in order]}")
        return order

    def get_active_feature_names(self) -> list[str]:
        """Return names of currently active features in importance order."""
        return [FEATURE_COLS[i] for i in self.feature_order[:self.n_active_features]]

    def get_active_feature_indices(self) -> list[int]:
        return self.feature_order[:self.n_active_features]

    # ── n_active_features control (T/Y) ──────────────────────────────────────

    def change_n_features(self, delta: int) -> bool:
        new_n = max(MIN_ACTIVE_FEATURES, min(MAX_ACTIVE_FEATURES,
                                              self.n_active_features + delta))
        if new_n == self.n_active_features:
            return False
        self.n_active_features = new_n
        print(f"[RF] n_active_features → {self.n_active_features}")
        return self.load_and_train()

    # ── depth control (+/-) ──────────────────────────────────────────────────

    def change_layers(self, delta: int) -> bool:
        new_depth = max(1, min(30, self.max_depth + delta))
        if new_depth == self.max_depth: return False
        self.max_depth = new_depth
        self.n_layers  = new_depth
        print(f"[RF] max_depth → {self.max_depth}")
        return self.load_and_train()

    # ── predict ──────────────────────────────────────────────────────────────

    def predict_direction(self, features):
        if not self.trained or self.forest is None: return None
        # Select only the active features in importance order
        active_idx = self.get_active_feature_indices()
        x_active   = np.array([features[i] for i in active_idx]).reshape(1, -1)
        proba = self.forest.predict_proba(x_active)[0]
        order = np.argsort(-proba)
        names = [DIR_NAMES[i] for i in order]
        print(f'direction : {names[0]}  (ranking: {" > ".join(names)})')
        return [DIR_DELTAS[i] for i in np.argsort(-proba)]
