"""
ml_dashboard.py — Freedom Force: The Reckoning
================================================
ML Dashboard screen – press M in game-over / victory to open.
* אימון RandomForest, LinearRegression, Lasso
* הצגת גרפים ב-pygame (2x2 grid)
* פאנל ימני: Top-5 פיצרים + רשימת כל התכונות שאומנו
* שמירת גרפים / pkl / דוח ל-disk דרך ml_exporter
"""

import os, json, io
import pygame
import numpy  as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib as _mpl

# Safe rcParams dict — avoids pygame-ce injecting tuple colors into rcParams
_DARK_RC = {
    "figure.facecolor":  "#05051a",
    "axes.facecolor":    "#0f0f2d",
    "axes.edgecolor":    "#50dcff",
    "axes.labelcolor":   "white",
    "text.color":        "white",
    "xtick.color":       "white",
    "ytick.color":       "white",
    "grid.color":        "#303060",
    "figure.edgecolor":  "#05051a",
    "lines.color":       "white",
    "patch.edgecolor":   "white",
    "savefig.facecolor": "#05051a",
}

from sklearn.pipeline        import Pipeline
from sklearn.preprocessing   import StandardScaler, OneHotEncoder
from sklearn.compose         import ColumnTransformer
from sklearn.impute           import SimpleImputer
from sklearn.ensemble        import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model    import LinearRegression, Lasso, Ridge, ElasticNet
from sklearn.tree            import DecisionTreeRegressor
try:
    from xgboost import XGBRegressor as _XGBRegressor
    _HAS_XGB = True
except ImportError:
    _HAS_XGB = False
from sklearn.model_selection import cross_val_score
from sklearn.metrics         import mean_absolute_error, r2_score

try:
    from screens.ml_exporter import export as _ml_export
except ImportError:
    try:
        from ml_exporter import export as _ml_export
    except ImportError:
        _ml_export = None

# colours (pygame)
C_BG     = (  5,   5,  22)
C_WHITE  = (255, 255, 255)
C_YELLOW = (255, 215,   0)
C_CYAN   = ( 80, 220, 255)
C_GREEN  = ( 60, 220,  80)
C_ORANGE = (255, 140,   0)
C_PURPLE = (160,  80, 255)
C_PINK   = (255, 100, 180)

# matplotlib theme
FIG_BG   = "#05051a"
AX_BG    = "#0f0f2d"
ACCENT   = "#50dcff"
GOLD     = "#ffd700"
GREEN_C  = "#3cdc50"
ORANGE_C = "#ff8c00"
RED_C    = "#dc2832"

ENEMY_KEYS = [
    "Yahya-Sinwar","Naeem-Qassem","Nasrallah","Mohammad-Ali-Jafari",
    "Mohammed-Deif","Abdul-Malik al-Houthi","Recep-Erdogan",
    "Ismail-Haniyeh","Muhammad Al-Amri","Fouad-Shukr",
    "Marwan-Isa","Qasem-Soleimani","Khaled-Mashal",
]
DROP_COLS  = {"date", "time", "session_duration_sec",
              'stage_reached','lives_lost','enemies_killed'
              }
TARGET_COL = "score"

MODEL_DESCRIPTIONS = {
    "RandomForest":
        "Ensemble of decision trees — robust, non-linear, handles outliers, provides feature importance.",
    "LinearRegression":
        "Fits a hyperplane via MSE minimisation. Fast and interpretable; assumes linearity.",
    "Lasso":
        "Linear model with L1 regularisation. Shrinks weak coefficients to zero (auto feature selection).",
    "Ridge":
        "Linear model with L2 regularisation. Penalises large coefficients, reduces overfitting.",
    "ElasticNet":
        "Combines L1 + L2 regularisation (Lasso + Ridge). Balances sparsity and stability.",
    "GradientBoosting":
        "Sequential ensemble — each tree corrects the previous. High accuracy, slower to train.",
    "DecisionTree":
        "Single decision tree. Highly interpretable but prone to overfitting without depth limit.",
    "XGBoost":
        "Optimised gradient boosting with regularisation. Often top performer on tabular data.",
}

# ---------------------------------------------------------------------------
# DATA
# ---------------------------------------------------------------------------

def _load_and_preprocess(csv_path):
    df = pd.read_csv(csv_path)
    drop = {"id"} | DROP_COLS
    df.drop(columns=[c for c in drop if c in df.columns], inplace=True)
    if TARGET_COL not in df.columns:
        raise ValueError(f"'{TARGET_COL}' column not found in CSV")
    y = df.pop(TARGET_COL).astype(float)

    if "kills_by_enemy" in df.columns:
        def _parse(val):
            if pd.isna(val) or str(val).strip() in ("", "{}"): return {}
            try:    return json.loads(str(val))
            except: return {}
        parsed = df["kills_by_enemy"].apply(_parse)
        for key in ENEMY_KEYS:
            safe = "enemy_" + key.replace(" ", "_").replace("-", "_")
            df[safe] = parsed.apply(lambda d, k=key: d.get(k, 0))
        df.drop(columns=["kills_by_enemy"], inplace=True)

    for col in df.columns:
        if df[col].dtype == object:
            lowered = df[col].astype(str).str.lower()
            if set(lowered.unique()) <= {"true", "false", "nan"}:
                df[col] = lowered.map({"true": 1, "false": 0, "nan": np.nan})
    return df, y


def _build_pipeline(model, df):
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object","category","string"]).columns.tolist()
    transformers = []
    if num_cols:
        transformers.append(("num", Pipeline([
            ("imp",   SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
        ]), num_cols))
    if cat_cols:
        transformers.append(("cat", Pipeline([
            ("imp", SimpleImputer(strategy="most_frequent")),
            ("ohe", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]), cat_cols))
    pre  = ColumnTransformer(transformers, remainder="drop")
    pipe = Pipeline([("pre", pre), ("model", model)])
    return pipe, num_cols, cat_cols


def _get_feature_names(pipe, num_cols, cat_cols):
    names = list(num_cols)
    for name, trans, _ in pipe.named_steps["pre"].transformers_:
        if name == "cat":
            names += list(trans.named_steps["ohe"].get_feature_names_out(cat_cols))
    return names


def train_models(csv_path):
    df, y = _load_and_preprocess(csv_path)
    n     = len(df)
    candidates = {
        "RandomForest":     RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1),
        "LinearRegression": LinearRegression(),
        "Lasso":            Lasso(alpha=1.0, max_iter=50000),
        "Ridge":            Ridge(alpha=1.0),
        "ElasticNet":       ElasticNet(alpha=1.0, l1_ratio=0.5, max_iter=50000),
        "GradientBoosting": GradientBoostingRegressor(n_estimators=100, random_state=42),
        "DecisionTree":     DecisionTreeRegressor(max_depth=5, random_state=42),
    }
    if _HAS_XGB:
        candidates["XGBoost"] = _XGBRegressor(
            n_estimators=100, random_state=42,
            verbosity=0, eval_metric="mae")
    results = {}
    for name, model in candidates.items():
        pipe, num_cols, cat_cols = _build_pipeline(model, df)
        if n < 2:
            # פחות מ-2 שורות — אין CV אפשרי
            pipe.fit(df, y)
            y_pred  = pipe.predict(df)
            cv_mae  = float(mean_absolute_error(y, y_pred))
            cv_r2   = 0.0
            train_r2 = 0.0
        else:
            # CV עם min(5, n) folds — גם MAE וגם R² מה-CV
            cv_folds = min(5, n)
            cv_mae = float(-cross_val_score(
                pipe, df, y, cv=cv_folds,
                scoring="neg_mean_absolute_error").mean())
            cv_r2  = float(cross_val_score(
                pipe, df, y, cv=cv_folds,
                scoring="r2").mean())
            # fit על כל הנתונים לחיזוי ולfeat importance
            pipe.fit(df, y)
            y_pred   = pipe.predict(df)
            train_r2 = float(r2_score(y, y_pred))   # train R² — לצורך השוואה בלבד

        fitted     = pipe.named_steps["model"]
        feat_names = _get_feature_names(pipe, num_cols, cat_cols)
        if hasattr(fitted, "feature_importances_"):
            imp = fitted.feature_importances_
        elif hasattr(fitted, "coef_"):
            imp = np.abs(fitted.coef_)
        else:
            imp = None

        results[name] = {
            "model":      pipe,
            "cv_mae":     cv_mae,       # MAE מ-cross-validation ← מדד אמיתי
            "cv_r2":      cv_r2,        # R² מ-cross-validation ← מדד אמיתי
            "train_r2":   train_r2,     # R² על train (לצורך השוואה בלבד)
            "mae":        cv_mae,       # alias — best_name selector משתמש בזה
            "r2":         cv_r2,        # alias — טבלה משתמשת בזה
            "y_pred":     y_pred,
            "feat_names": feat_names,
            "importances": imp,
        }

    # בחר מודל לפי CV-R² הכי קרוב ל-0 (הכי פחות שלילי = הכי טוב)
    best_name = max(results, key=lambda k: results[k]["cv_r2"])
    return {"results": results, "best_name": best_name, "y": y, "df": df}


# ---------------------------------------------------------------------------
# PLOTS  (matplotlib -> pygame.Surface)
# ---------------------------------------------------------------------------

def _fig_to_surface(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor(), dpi=110)
    plt.close(fig)
    buf.seek(0)
    return pygame.image.load(buf, "png").convert()

def _ax_style(ax, title, tc=GOLD):
    ax.set_facecolor(AX_BG)
    ax.set_title(title, color=tc, fontsize=11, pad=8, fontweight="bold")
    ax.tick_params(colors="white", labelsize=8)
    for sp in ax.spines.values():
        sp.set_edgecolor(ACCENT)


def _make_feat_fig(best_name, results):
    imp  = results[best_name]["importances"]
    feat = results[best_name]["feat_names"]
    if imp is None:
        return None
    pairs = sorted(zip(imp, feat), reverse=True)[:5]
    vals, names = zip(*pairs)
    with _mpl.rc_context(_DARK_RC):
        fig, ax = plt.subplots(figsize=(5.5, 3.8), facecolor=FIG_BG)
        ax.barh(range(len(names)), vals,
                color=[GOLD, ACCENT, GREEN_C, ORANGE_C, "#a050ff"][:len(names)])
        ax.set_yticks(range(len(names)))
        ax.set_yticklabels([n[:22] for n in names], color="white", fontsize=9)
        ax.set_xlabel("Importance", color="white", fontsize=9)
        _ax_style(ax, f"Top-5 Features  [{best_name}]")
        plt.tight_layout()
    return fig


def _make_corr_fig(df, y):
    data = df.select_dtypes(include="number").copy()
    data["score"] = y.values
    corr = data.corr()["score"].drop("score").sort_values()
    with _mpl.rc_context(_DARK_RC):
        fig, ax = plt.subplots(figsize=(5.5, 3.8), facecolor=FIG_BG)
        ax.barh(range(len(corr)), corr.values,
                color=[RED_C if v < 0 else GREEN_C for v in corr.values])
        ax.set_yticks(range(len(corr)))
        ax.set_yticklabels([n[:20] for n in corr.index], color="white", fontsize=7)
        ax.axvline(0, color="white", linewidth=0.8)
        ax.set_xlabel("Pearson r with score", color="white", fontsize=9)
        _ax_style(ax, "Feature-Score Correlation", tc=ACCENT)
        plt.tight_layout()
    return fig


def _safe_text(ax, x, y, txt, **kw):
    """ax.text wrapper — skips if coordinates are not finite."""
    if np.isfinite(x) and np.isfinite(y):
        ax.text(x, y, txt, **kw)


def _make_mae_fig(results):
    names       = list(results.keys())
    maes        = [results[n]["mae"]    for n in names]
    r2s         = [results[n]["cv_r2"]  for n in names]
    labels      = [n[:11] for n in names]
    best_r2_i   = int(np.argmax(r2s))
    best_mae_i  = int(np.argmin(maes))
    n           = len(names)
    bw          = max(0.25, min(0.6, 4.0 / n))
    with _mpl.rc_context(_DARK_RC):
        fig, axes = plt.subplots(1, 2,
                                 figsize=(max(7, n * 1.1), 3.6),
                                 facecolor=FIG_BG)
        # ── CV-MAE ────────────────────────────────────────────────────────────
        ax = axes[0]
        ax.bar(labels, maes,
               color=[GOLD if i == best_mae_i else ACCENT for i in range(n)],
               width=bw, edgecolor="white", linewidth=0.4)
        mae_max = max(maes) if maes else 1
        for i, v in enumerate(maes):
            _safe_text(ax, i, v + mae_max * 0.02, f"{v:,.0f}",
                       ha="center", fontsize=7, color="white",
                       fontweight="bold", rotation=40)
        ax.set_ylabel("CV-MAE", color="white", fontsize=8)
        ax.tick_params(axis="x", labelrotation=30, labelsize=7)
        _ax_style(ax, "CV-MAE  (lower=better)")

        # ── CV-R2 ─────────────────────────────────────────────────────────────
        ax2 = axes[1]
        r2s_plot = [max(v, -50.0) for v in r2s]   # clip extreme negatives
        ax2.bar(labels, r2s_plot,
                color=[GOLD if i == best_r2_i else GREEN_C for i in range(n)],
                width=bw, edgecolor="white", linewidth=0.4)
        ax2.axhline(0, color="white", linewidth=0.9, linestyle="--", alpha=0.6)
        r2_min  = min(r2s_plot); r2_max = max(r2s_plot)
        margin  = max(abs(r2_min), abs(r2_max)) * 0.18 + 1
        ax2.set_ylim(r2_min - margin, r2_max + margin)
        for i, (vr, vp) in enumerate(zip(r2s, r2s_plot)):
            txt   = f"{vr:.1f}" if vr == vp else f"{vr:.0f}*"
            lbl_y = vp + (margin * 0.25 if vp >= 0 else -margin * 0.3)
            _safe_text(ax2, i, lbl_y, txt,
                       ha="center", fontsize=7, color="white",
                       fontweight="bold", rotation=40)
        ax2.set_ylabel("CV-R2", color="white", fontsize=8)
        ax2.tick_params(axis="x", labelrotation=30, labelsize=7)
        _ax_style(ax2, "CV-R2  (max=best)", tc=GREEN_C)

        plt.tight_layout(pad=1.2)
    return fig


def _make_pred_fig(best_name, results, y):
    yp = results[best_name]["y_pred"]
    y_arr  = np.array(y, dtype=float)
    yp_arr = np.array(yp, dtype=float)
    mn = min(float(y_arr.min()), float(yp_arr.min()))
    mx = max(float(y_arr.max()), float(yp_arr.max()))

    # קו רגרסיה ומשוואה
    coeffs   = np.polyfit(y_arr, yp_arr, 1)
    poly     = np.poly1d(coeffs)
    x_line   = np.linspace(mn, mx, 200)
    y_line   = poly(x_line)
    slope, intercept = coeffs
    sign     = "+" if intercept >= 0 else "-"
    eq_str   = f"ŷ = {slope:.3f}x {sign} {abs(intercept):.3f}"

    with _mpl.rc_context(_DARK_RC):
        fig, ax = plt.subplots(figsize=(4.8, 3.2), facecolor=FIG_BG)
        # נקודות פיזור — נתונים אמיתיים
        ax.scatter(y_arr, yp_arr, color=ACCENT, edgecolors=GOLD, s=60, zorder=3,
                   label="Data points")
        # קו perfect prediction (45°)
        ax.plot([mn, mx], [mn, mx], "--", color=RED_C, linewidth=1.2,
                label="Perfect fit", zorder=2)
        # קו רגרסיה
        ax.plot(x_line, y_line, color=GREEN_C, linewidth=2.0, zorder=4,
                label=f"Regression: {eq_str}")
        # משוואה על הגרף
        ax.text(0.04, 0.94, eq_str,
                transform=ax.transAxes,
                fontsize=8, color=GREEN_C,
                verticalalignment="top",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#0f0f2d", alpha=0.8,
                          edgecolor=GREEN_C))
        ax.legend(fontsize=7, loc="lower right",
                  framealpha=0.5, labelcolor="white",
                  facecolor="#0f0f2d", edgecolor=GREEN_C)
        ax.set_xlabel("Actual Score",    color="white", fontsize=9)
        ax.set_ylabel("Predicted Score", color="white", fontsize=9)
        _ax_style(ax, "Predicted vs Actual", tc=GREEN_C)
        plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# DASHBOARD CLASS
# ---------------------------------------------------------------------------

class MLDashboard:
    SW = 1280; SH = 720
    HEADER_H  = 110
    METRICS_H = 160
    EQ_BAR_H  = 32          # פס כפתור בתחתית
    TOP_TOTAL = HEADER_H + METRICS_H   # 270
    RIGHT_W   = 295
    PLOTS_RIGHT = SW - RIGHT_W - 4     # 981

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock  = clock
        self._ready        = False
        self._error        = None
        self._surfaces     = []
        self._title_str    = ""
        self._desc_line    = ""
        self._metrics      = []
        self._top5         = []
        self._all_features = []
        self._export_msg   = ""
        self._export_t     = 0.0
        # מסך טבלת תכונות
        self._eq_rows      = []    # list of (rank, feature, coef, abs_coef)
        self._eq_model     = ""
        self._eq_intercept = 0.0
        self._feat_screen  = False # האם מסך הטבלה פתוח
        self._feat_scroll  = 0    # גלילה אנכית (שורות)

        self._fxs = pygame.font.SysFont("consolas", 13)
        self._fsm = pygame.font.SysFont("consolas", 15)
        self._fmd = pygame.font.SysFont("consolas", 18, bold=True)
        self._flg = pygame.font.SysFont("consolas", 24, bold=True)
        self._fxl = pygame.font.SysFont("consolas", 30, bold=True)

    # ---- public --------------------------------------------------------------

    def open(self, csv_path, base_dir="."):
        self._ready = False; self._error = None; self._surfaces = []
        try:
            data = train_models(csv_path)
        except Exception as exc:
            self._error = str(exc); self._ready = True; return

        results   = data["results"]
        best_name = data["best_name"]
        y         = data["y"]
        df        = data["df"]

        self._title_str = f"{best_name}  —  Machine Learning Dashboard"
        self._desc_line = MODEL_DESCRIPTIONS.get(best_name, "")
        self._metrics   = [{"name": n,
                              "mae":      r["cv_mae"],
                              "r2":       r["cv_r2"],
                              "train_r2": r["train_r2"],
                              "best":     n == best_name}
                             for n, r in results.items()]

        # ── חילוץ קבועי המודל הלינארי ──────────────────────────────────────────
        self._eq_rows      = []
        self._eq_model     = ""
        self._eq_intercept = 0.0
        _lin_pref = ["LinearRegression", "Ridge", "Lasso", "ElasticNet"]
        _eq_src   = next((n for n in _lin_pref if n in results and
                          results[n]["importances"] is not None), None)
        if _eq_src is None and hasattr(
                results[best_name]["model"].named_steps["model"], "coef_"):
            _eq_src = best_name
        if _eq_src:
            _fitted    = results[_eq_src]["model"].named_steps["model"]
            _feats     = results[_eq_src]["feat_names"]
            _coefs     = _fitted.coef_
            _intercept = float(_fitted.intercept_) if hasattr(_fitted, "intercept_") else 0.0
            self._eq_intercept = _intercept
            self._eq_model     = _eq_src
            # מיון לפי |coef| יורד
            _pairs = sorted(zip(_coefs, _feats), key=lambda x: abs(x[0]), reverse=True)
            self._eq_rows = [(i+1, fname, float(coef), abs(float(coef)))
                             for i, (coef, fname) in enumerate(_pairs)]

        imp  = results[best_name]["importances"]
        feat = results[best_name]["feat_names"]
        self._all_features = feat
        self._top5 = sorted(
            [(v, n) for v, n in zip(imp, feat) if np.isfinite(float(v))],
            reverse=True)[:5] if imp is not None else []

        # 2x2 plots
        figs = [
            ("feat", lambda: _make_feat_fig(best_name, results)),
            ("corr", lambda: _make_corr_fig(df, y)),
            ("mae",  lambda: _make_mae_fig(results)),
            ("pred", lambda: _make_pred_fig(best_name, results, y)),
        ]
        raw = []
        for key, fn in figs:
            try:
                fig = fn()
                if fig: raw.append(_fig_to_surface(fig))
            except Exception as e:
                print(f"[ml_dashboard] plot '{key}' error: {e}")

        plots_w = self.PLOTS_RIGHT - 8
        area_h  = self.SH - self.TOP_TOTAL - self.EQ_BAR_H - 8
        pw = (plots_w - 6) // 2
        ph = (area_h  - 6) // 2
        top = self.TOP_TOTAL + 4
        positions = [
            (4,         top),
            (4+pw+4,    top),
            (4,         top+ph+4),
            (4+pw+4,    top+ph+4),
        ]
        for i, surf in enumerate(raw[:4]):
            scaled = pygame.transform.smoothscale(surf, (pw, ph))
            self._surfaces.append((scaled, pygame.Rect(positions[i], (pw, ph))))

        # export
        if _ml_export is not None:
            try:
                export_dir = _ml_export(data, base_dir)
                rel = os.path.relpath(export_dir, base_dir)
                self._export_msg = f"Saved  ->  {rel}/   (6 plots + best_model.pkl + model_analysis.txt)"
                self._export_t   = 8.0
            except Exception as e:
                self._export_msg = f"Export error: {e}"; self._export_t = 6.0

        self._ready = True

    def update(self, dt=0.016):
        if self._export_t > 0: self._export_t -= dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self._feat_screen:
                        self._feat_screen = False  # סגור טבלה קודם
                    else:
                        return "back"
                elif event.key == pygame.K_m:
                    if self._feat_screen:
                        self._feat_screen = False
                    else:
                        return "back"
                elif event.key == pygame.K_f:
                    self._feat_screen = not self._feat_screen
                    self._feat_scroll = 0
                # גלילה אנכית בטבלת התכונות
                elif self._feat_screen:
                    if event.key == pygame.K_DOWN:  self._feat_scroll += 1
                    if event.key == pygame.K_UP:    self._feat_scroll = max(0, self._feat_scroll - 1)
                    if event.key == pygame.K_PAGEDOWN: self._feat_scroll += 10
                    if event.key == pygame.K_PAGEUP:   self._feat_scroll = max(0, self._feat_scroll - 10)
            if event.type == pygame.MOUSEWHEEL and self._feat_screen:
                self._feat_scroll = max(0, self._feat_scroll - event.y)
        return None

    # ── פס כפתור תחתון ───────────────────────────────────────────────────────

    def _draw_bottom_bar(self):
        bar_y = self.SH - self.EQ_BAR_H
        panel = pygame.Surface((self.SW, self.EQ_BAR_H), pygame.SRCALPHA)
        panel.fill((6, 18, 45, 240))
        pygame.draw.rect(panel, (*C_CYAN, 160), (0, 0, self.SW, self.EQ_BAR_H), 1)
        self.screen.blit(panel, (0, bar_y))

        if self._eq_model:
            # כפתור מהבהב
            pulse = int(160 + 95 * abs(
                __import__("math").sin(pygame.time.get_ticks() / 500)))
            btn_col = (0, pulse // 2, pulse)
            btn_txt = self._fsm.render(
                f"[ F ]  Feature Equation Table  ·  {self._eq_model}", True, (80, 220, 255))
            bw = btn_txt.get_width() + 32
            bh = self.EQ_BAR_H - 6
            bx = self.SW // 2 - bw // 2
            by = bar_y + 3
            pygame.draw.rect(self.screen, (0, 30, 70), (bx, by, bw, bh), border_radius=6)
            pygame.draw.rect(self.screen, btn_col,     (bx, by, bw, bh), 2, border_radius=6)
            self.screen.blit(btn_txt, (bx + 16, by + (bh - btn_txt.get_height()) // 2))
        else:
            no_lbl = self._fxs.render(
                "No linear model available for equation display", True, (80, 90, 120))
            self.screen.blit(no_lbl, (self.SW // 2 - no_lbl.get_width() // 2, bar_y + 8))

    # ── מסך טבלת תכונות ─────────────────────────────────────────────────────

    def _draw_feature_table(self):
        """Overlay מלא — טבלה: # | Feature | Coefficient | |coef| | Bar"""
        SW, SH = self.SW, self.SH
        PAD = 30

        # רקע כהה
        bg = pygame.Surface((SW, SH), pygame.SRCALPHA)
        bg.fill((2, 6, 22, 248))
        self.screen.blit(bg, (0, 0))
        pygame.draw.rect(self.screen, (*C_CYAN, 220), (6, 6, SW-12, SH-12), 2, border_radius=10)

        # ── כותרת ──
        title = self._fxl.render(
            f"Feature Equation  —  {self._eq_model}", True, C_YELLOW)
        self.screen.blit(title, (SW // 2 - title.get_width() // 2, 14))

        # intercept
        ic_col = C_ORANGE if self._eq_intercept >= 0 else (255, 80, 80)
        ic_txt = self._fsm.render(
            f"Intercept (bias):  {self._eq_intercept:+.4f}", True, ic_col)
        self.screen.blit(ic_txt, (SW // 2 - ic_txt.get_width() // 2, 52))

        # hint
        hint = self._fxs.render(
            "↑↓  /  scroll wheel  to navigate     ESC / M  to close", True, (80, 110, 160))
        self.screen.blit(hint, (SW // 2 - hint.get_width() // 2, 78))

        pygame.draw.line(self.screen, (*C_CYAN, 120), (PAD, 98), (SW - PAD, 98), 1)

        # ── עמודות ──
        TABLE_TOP  = 104
        TABLE_BOT  = SH - 18
        ROW_H      = 22
        VIEW_ROWS  = (TABLE_BOT - TABLE_TOP) // ROW_H

        # רוחב עמודות: #, Feature, Coef, |Coef|, Bar
        CX = [PAD, PAD+40, PAD+490, PAD+620, PAD+730]
        HDR = [("#","#", C_CYAN),
               ("Feature", "Feature", C_CYAN),
               ("Coefficient", "Coefficient", C_CYAN),
               ("|Coef|", "|Coef|", C_CYAN),
               ("Impact Bar", "Impact Bar", C_CYAN)]

        # כותרות עמודות
        for cx, (short, full, hc) in zip(CX, HDR):
            h = self._fsm.render(full, True, hc)
            self.screen.blit(h, (cx, TABLE_TOP))
        pygame.draw.line(self.screen, C_CYAN,
                         (PAD, TABLE_TOP + 20), (SW - PAD, TABLE_TOP + 20), 1)

        DATA_TOP = TABLE_TOP + 24

        # גלילה
        rows = self._eq_rows
        max_scroll = max(0, len(rows) - VIEW_ROWS + 1)
        self._feat_scroll = max(0, min(self._feat_scroll, max_scroll))
        visible = rows[self._feat_scroll: self._feat_scroll + VIEW_ROWS]

        # מקסימום |coef| לסרגל
        max_abs = max((r[3] for r in rows), default=1.0) or 1.0
        BAR_W   = SW - PAD - CX[4] - 10

        for ri, (rank, fname, coef, abs_coef) in enumerate(visible):
            ry  = DATA_TOP + ri * ROW_H
            # שורות מדגישות
            if ri % 2 == 0:
                pygame.draw.rect(self.screen, (10, 18, 50),
                                 (PAD, ry, SW - 2*PAD, ROW_H - 1), border_radius=3)

            # צבע לפי סימן מקדם
            coef_col = C_GREEN if coef >= 0 else (255, 80, 80)

            # #
            self.screen.blit(
                self._fxs.render(str(rank), True, (120, 130, 160)),
                (CX[0], ry + 3))

            # Feature (קצר אם צריך)
            fname_disp = fname if len(fname) <= 44 else fname[:42] + "…"
            is_top = any(n == fname for _, n in self._top5)
            fc = C_YELLOW if is_top else C_WHITE
            prefix = "★ " if is_top else "  "
            self.screen.blit(
                self._fxs.render(prefix + fname_disp, True, fc),
                (CX[1], ry + 3))

            # Coefficient
            self.screen.blit(
                self._fxs.render(f"{coef:+.6f}", True, coef_col),
                (CX[2], ry + 3))

            # |Coef|
            self.screen.blit(
                self._fxs.render(f"{abs_coef:.6f}", True, (180, 190, 210)),
                (CX[3], ry + 3))

            # Bar
            filled = max(3, int(BAR_W * abs_coef / max_abs))
            bar_col = (0, 180, 80) if coef >= 0 else (200, 50, 50)
            pygame.draw.rect(self.screen, (20, 30, 60),
                             (CX[4], ry + 5, BAR_W, ROW_H - 10), border_radius=3)
            pygame.draw.rect(self.screen, bar_col,
                             (CX[4], ry + 5, filled, ROW_H - 10), border_radius=3)

        # scrollbar
        if max_scroll > 0:
            sb_x  = SW - PAD - 8
            sb_h  = TABLE_BOT - DATA_TOP
            thumb = max(20, int(sb_h * VIEW_ROWS / max(len(rows), 1)))
            thumb_y = DATA_TOP + int((sb_h - thumb) * self._feat_scroll / max_scroll)
            pygame.draw.rect(self.screen, (20, 30, 60),
                             (sb_x, DATA_TOP, 6, sb_h), border_radius=3)
            pygame.draw.rect(self.screen, C_CYAN,
                             (sb_x, thumb_y, 6, thumb), border_radius=3)

        # ── משוואה מקוצרת בתחתית ──
        if rows:
            # בנה מחרוזת קצרה
            top3 = rows[:3]
            parts = [f"y = {self._eq_intercept:+.2f}"]
            for _, fname, coef, _ in top3:
                s = "+" if coef >= 0 else "−"
                parts.append(f" {s} {abs(coef):.3f}·{fname[:14]}")
            if len(rows) > 3:
                parts.append(f" + … ({len(rows)-3} more)")
            eq_line = "".join(parts)
            eq_surf = self._fxs.render(eq_line, True, (100, 180, 255))
            ey = SH - 16
            self.screen.blit(eq_surf, (SW // 2 - eq_surf.get_width() // 2, ey))

    def draw(self):
        self.screen.fill(C_BG)
        if not self._ready:
            lbl = self._flg.render("Training & saving models...", True, C_YELLOW)
            self.screen.blit(lbl, (self.SW//2 - lbl.get_width()//2, self.SH//2-20))
            return
        if self._error:
            self.screen.blit(self._fmd.render(f"Error: {self._error}", True, (255,80,80)), (40,300))
            self.screen.blit(self._fsm.render("Press ESC / M to go back", True, C_CYAN), (40,335))
            return
        self._draw_header()
        self._draw_metrics(self.HEADER_H + 2)
        self._draw_plots()
        self._draw_right_panel()
        self._draw_bottom_bar()
        if self._feat_screen:
            self._draw_feature_table()
        if self._export_t > 0: self._draw_export_toast()

    # ---- private draw --------------------------------------------------------

    def _draw_header(self):
        panel = pygame.Surface((self.SW, self.HEADER_H), pygame.SRCALPHA)
        panel.fill((14, 14, 48, 240))
        pygame.draw.rect(panel, (*C_CYAN, 160), (0, 0, self.SW, self.HEADER_H), 2)
        self.screen.blit(panel, (0, 0))
        self.screen.blit(self._fxl.render(self._title_str, True, C_YELLOW), (14, 8))
        desc = self._fxs.render(self._desc_line, True, C_CYAN)
        self.screen.blit(desc, (16, 48))
        hint = self._fxs.render("Press  M / ESC  to return", True, (110, 110, 160))
        self.screen.blit(hint, (self.SW - hint.get_width() - 10, self.HEADER_H - 18))

    def _draw_metrics(self, y0):
        panel = pygame.Surface((self.SW, self.METRICS_H), pygame.SRCALPHA)
        panel.fill((8, 22, 8, 225))
        pygame.draw.rect(panel, (*C_GREEN, 120), (0, 0, self.SW, self.METRICS_H), 1)
        self.screen.blit(panel, (0, y0))

        col_x = [14, 280, 470, 650, 830, 960]
        hdrs  = [("Model",C_YELLOW),("CV-MAE",C_ORANGE),("CV-R2",C_GREEN),("Train-R2",C_CYAN),("Best?",C_PINK)]
        for i,(h,hc) in enumerate(hdrs):
            self.screen.blit(self._fsm.render(h, True, hc), (col_x[i], y0+4))

        for ri, m in enumerate(self._metrics):
            ry  = y0 + 24 + ri*17
            bg  = (25,45,15) if m["best"] else (16,16,38)
            pygame.draw.rect(self.screen, bg, (10, ry-1, self.SW-20, 16), border_radius=3)
            nc  = C_YELLOW if m["best"] else C_WHITE
            train_r2_val = m.get("train_r2", m["r2"])
            row = [(m["name"][:28],nc),
                   (f"{m['mae']:>10,.0f}",  C_ORANGE),
                   (f"{m['r2']:>7.4f}",     C_GREEN),
                   (f"{train_r2_val:>8.4f}", C_CYAN),
                   ("BEST" if m["best"] else "", C_PINK)]
            for i,(txt,col) in enumerate(row):
                self.screen.blit(self._fxs.render(txt, True, col), (col_x[i], ry))

    def _draw_plots(self):
        for surf, rect in self._surfaces:
            pygame.draw.rect(self.screen, C_CYAN, rect.inflate(4,4), width=2)
            self.screen.blit(surf, rect.topleft)

    def _draw_right_panel(self):
        rx   = self.PLOTS_RIGHT + 2
        rw   = self.RIGHT_W
        rtop = self.TOP_TOTAL
        rh   = self.SH - rtop - 2

        panel = pygame.Surface((rw, rh), pygame.SRCALPHA)
        panel.fill((8, 8, 35, 245))
        pygame.draw.rect(panel, (*C_YELLOW, 140), (0, 0, rw, rh), 2)
        self.screen.blit(panel, (rx, rtop))

        y = rtop + 8
        bar_cols = [C_YELLOW, C_CYAN, C_GREEN, C_ORANGE, C_PURPLE]

        # Top-5 header
        self.screen.blit(self._fsm.render("Top-5 Feature Importances", True, C_YELLOW), (rx+8, y))
        y += 22
        max_imp = self._top5[0][0] if self._top5 else 1.0

        for rank, (imp, name) in enumerate(self._top5):
            col = bar_cols[rank]
            lbl = self._fxs.render(f"{rank+1}. {name[:27]}", True, col)
            self.screen.blit(lbl, (rx+8, y))
            # guard against nan/inf importance values
            imp_safe    = float(imp) if np.isfinite(float(imp)) else 0.0
            max_imp_safe = float(max_imp) if (np.isfinite(float(max_imp)) and max_imp > 0) else 1.0
            bw = max(4, min(rw - 26, int((imp_safe / max_imp_safe) * (rw - 22))))
            pygame.draw.rect(self.screen, col, (rx+8, y+14, bw, 5), border_radius=2)
            pct_s = self._fxs.render(f"{imp_safe:.3f}", True, (170,170,170))
            self.screen.blit(pct_s, (rx+10+bw, y+11))
            y += 30

        # divider
        pygame.draw.line(self.screen, C_CYAN, (rx+6, y+3), (rx+rw-6, y+3), 1)
        y += 11

        # All features
        self.screen.blit(
            self._fsm.render(f"All Trained Features ({len(self._all_features)})", True, C_CYAN),
            (rx+8, y))
        y += 19

        imp_names = {nm for _, nm in self._top5}
        for feat in self._all_features:
            if y > self.SH - 16:
                self.screen.blit(
                    self._fxs.render("...", True, (100,100,140)),
                    (rx+8, y))
                break
            is_top = feat in imp_names
            col    = C_YELLOW if is_top else (150, 160, 180)
            prefix = "* " if is_top else "  "
            self.screen.blit(
                self._fxs.render(prefix + feat[:29], True, col),
                (rx+6, y))
            y += 13

    def _draw_export_toast(self):
        if not self._export_msg: return
        s  = self._fxs.render(self._export_msg, True, C_GREEN)
        bg = pygame.Surface((s.get_width()+24, 26), pygame.SRCALPHA)
        bg.fill((0, 35, 0, 210))
        bx = self.SW//2 - bg.get_width()//2
        by = self.SH - 34
        self.screen.blit(bg, (bx, by))
        self.screen.blit(s,  (bx+12, by+5))


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    csv  = sys.argv[1] if len(sys.argv) > 1 else "data/record.csv"
    base = sys.argv[2] if len(sys.argv) > 2 else "."
    pygame.init(); pygame.font.init()
    screen = pygame.display.set_mode((1280, 720))
    clock  = pygame.time.Clock()
    dash   = MLDashboard(screen, clock)
    dash.open(csv, base)
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        r  = dash.update(dt)
        if r in ("back", "quit"): running = False
        dash.draw()
        pygame.display.flip()
    pygame.quit()