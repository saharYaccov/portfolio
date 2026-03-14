"""
ml_exporter.py  Freedom Force: The Reckoning
===============================================
נקרא בלחיצת M  שומר ל-disk את:

  <game_root>/machine_learning/
      best_model.pkl                   המודל הטוב ביותר (pickle)
      model_analysis.txt               ניתוח מלא בטקסט
      plots/
          01_feature_importance.png
          02_correlation.png
          03_mae_comparison.png
          04_predicted_vs_actual.png
          05_residuals.png
          06_score_distribution.png

ממשק ציבורי:
    export(data, base_dir) -> export_dir (str)
        data  = dict מ-train_models()
        base_dir = שורש המשחק (כמו BASE_DIR ב-main.py)
"""

import os, pickle, textwrap
from datetime import datetime

import numpy  as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib as _mpl

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

#  matplotlib theme
FIG_BG   = "#05051a"
AX_BG    = "#0f0f2d"
ACCENT   = "#50dcff"
GOLD     = "#ffd700"
GREEN_C  = "#3cdc50"
ORANGE_C = "#ff8c00"
RED_C    = "#dc2832"
PURPLE   = "#a050ff"
C_WHITE  = (255, 255, 255)

BAR_COLORS = [GOLD, ACCENT, GREEN_C, ORANGE_C, PURPLE,
              "#ff6090", "#60ffa0", "#ffa060", "#60a0ff", "#ff60ff"]

_SHORT = {
    "RandomForestRegressor": "RandomForest",
    "LinearRegression":      "LinearReg",
    "Lasso":                 "Lasso",
}

#
# helpers
#

def _save(fig, path: str):
    fig.savefig(path, bbox_inches="tight",
                facecolor=fig.get_facecolor(), dpi=130)
    plt.close(fig)


def _ax_style(ax, title, title_color=GOLD, xlabel="", ylabel=""):
    ax.set_facecolor(AX_BG)
    ax.set_title(title, color=title_color, fontsize=12, pad=10, fontweight="bold")
    if xlabel: ax.set_xlabel(xlabel, color="white", fontsize=9)
    if ylabel: ax.set_ylabel(ylabel, color="white", fontsize=9)
    ax.tick_params(colors="white", labelsize=8)
    for spine in ax.spines.values():
        spine.set_edgecolor(ACCENT)


#
# plot functions  (כל אחת מחזירה fig ושומרת ל-path)
#

def _plot_feature_importance(best_name, results, path):
    with _mpl.rc_context(_DARK_RC):
        imp   = results[best_name]["importances"]
        feats = results[best_name]["feat_names"]
        if imp is None:
            return
        top_n = min(15, len(feats))
        pairs = sorted(zip(imp, feats), reverse=True)[:top_n]
        vals, names = zip(*pairs)

    fig, ax = plt.subplots(figsize=(9, 0.55 * top_n + 1.8), facecolor=FIG_BG)
    colors = [BAR_COLORS[i % len(BAR_COLORS)] for i in range(top_n)]
    bars = ax.barh(range(top_n), vals, color=colors, edgecolor="white",
                   linewidth=0.4)
    ax.set_yticks(range(top_n))
    ax.set_yticklabels([n[:32] for n in names], fontsize=8.5)
    for i, (bar, v) in enumerate(zip(bars, vals)):
        ax.text(v + max(vals) * 0.01, i, f"{v:.3f}",
                va="center", fontsize=7.5, color="white")
    _ax_style(ax, f" Top-{top_n} Feature Importances  [{best_name}]",
              xlabel="Importance Score")
    plt.tight_layout()
    _save(fig, path)


def _plot_correlation(df, y, path):
    with _mpl.rc_context(_DARK_RC):
        data = df.select_dtypes(include="number").copy()
        data["score"] = y.values
        corr = data.corr()["score"].drop("score").sort_values()

    fig, ax = plt.subplots(figsize=(9, max(4, 0.38 * len(corr) + 1.5)),
                           facecolor=FIG_BG)
    colors = [RED_C if v < 0 else GREEN_C for v in corr.values]
    bars = ax.barh(range(len(corr)), corr.values, color=colors,
                   edgecolor="white", linewidth=0.3)
    ax.set_yticks(range(len(corr)))
    ax.set_yticklabels([n[:30] for n in corr.index], fontsize=7.5)
    ax.axvline(0, color="white", linewidth=0.9, linestyle="--")
    for i, (bar, v) in enumerate(zip(bars, corr.values)):
        offset = 0.005 if v >= 0 else -0.005
        ax.text(v + offset, i, f"{v:+.3f}", va="center", fontsize=7,
                color="white", ha="left" if v >= 0 else "right")
    _ax_style(ax, " Pearson Correlation  All Features vs Score",
              title_color=ACCENT, xlabel="Pearson r")
    plt.tight_layout()
    _save(fig, path)


def _plot_mae_comparison(results, path):
    with _mpl.rc_context(_DARK_RC):
        names  = list(results.keys())
        maes   = [results[n]["cv_mae"] for n in names]
        r2s    = [results[n]["cv_r2"]  for n in names]
        # best by CV-R2 closest to 0 (max)
        best_r2_i  = int(np.argmax(r2s))
        best_mae_i = int(np.argmin(maes))
        labels = [n[:12] for n in names]

        n_models = len(names)
        fig_w    = max(12, n_models * 1.5)
        bw       = max(0.25, min(0.6, 4.0 / n_models))

        fig, axes = plt.subplots(1, 2, figsize=(fig_w, 5.0), facecolor=FIG_BG)

        # ── MAE bars ──────────────────────────────────────────────────────────
        ax = axes[0]
        bar_cols = [GOLD if i == best_mae_i else ACCENT for i in range(n_models)]
        ax.bar(labels, maes, color=bar_cols, width=bw,
               edgecolor="white", linewidth=0.5)
        mae_max = max(maes)
        for i, v in enumerate(maes):
            ax.text(i, v + mae_max * 0.02, f"{v:,.0f}",
                    ha="center", fontsize=8, color="white",
                    fontweight="bold", rotation=45)
        _ax_style(ax, "CV-MAE  (lower = better)", ylabel="Mean Absolute Error")
        ax.set_facecolor(AX_BG)
        ax.tick_params(axis="x", labelrotation=30, labelsize=8)

        # ── CV-R2 bars ────────────────────────────────────────────────────────
        ax2 = axes[1]
        r2_cols = [GOLD if i == best_r2_i else GREEN_C for i in range(n_models)]
        # clip extreme negatives for display — keep plot readable
        r2s_plot = [max(v, -50.0) for v in r2s]
        ax2.bar(labels, r2s_plot, color=r2_cols, width=bw,
                edgecolor="white", linewidth=0.5)
        ax2.axhline(0, color="white", linewidth=1.0, linestyle="--", alpha=0.6)
        r2_min = min(r2s_plot); r2_max = max(r2s_plot)
        margin = max(abs(r2_min), abs(r2_max)) * 0.15 + 1
        ax2.set_ylim(r2_min - margin, r2_max + margin)
        for i, (v_real, v_plot) in enumerate(zip(r2s, r2s_plot)):
            label_y = v_plot + (margin * 0.3 if v_plot >= 0 else -margin * 0.3)
            # mark clipped bars
            txt = f"{v_real:.2f}" if v_real == v_plot else f"{v_real:.1f}*"
            ax2.text(i, label_y, txt,
                     ha="center", fontsize=8, color="white",
                     fontweight="bold", rotation=45)
        _ax_style(ax2, "CV-R2  (higher = better, closest to 0)",
                  ylabel="CV-R2")
        ax2.set_facecolor(AX_BG)
        ax2.tick_params(axis="x", labelrotation=30, labelsize=8)

        plt.tight_layout(pad=1.5)
        _save(fig, path)


def _plot_pred_vs_actual(best_name, results, y, path):
    with _mpl.rc_context(_DARK_RC):
        y_pred = results[best_name]["y_pred"]
        mn = min(float(y.min()), float(y_pred.min()))
        mx = max(float(y.max()), float(y_pred.max()))

    fig, ax = plt.subplots(figsize=(7, 5.5), facecolor=FIG_BG)
    ax.scatter(y, y_pred, color=ACCENT, edgecolors=GOLD,
               s=80, zorder=3, label="Sessions")
    ax.plot([mn, mx], [mn, mx], "--", color=RED_C,
            linewidth=1.5, label="Perfect fit")

    # annotate each point
    for xi, yi_p in zip(y, y_pred):
        ax.annotate(f"{xi:,.0f}", (xi, yi_p),
                    textcoords="offset points", xytext=(4, 3),
                    fontsize=7, color="white", alpha=0.75)

    ax.legend(fontsize=9, facecolor=AX_BG, edgecolor=ACCENT)
    _ax_style(ax, f" Predicted vs Actual  [{best_name}]",
              title_color=GREEN_C,
              xlabel="Actual Score", ylabel="Predicted Score")
    plt.tight_layout()
    _save(fig, path)


def _plot_residuals(best_name, results, y, path):
    with _mpl.rc_context(_DARK_RC):
        y_pred    = results[best_name]["y_pred"]
        residuals = np.array(y) - np.array(y_pred)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), facecolor=FIG_BG)

    # scatter residuals
    ax = axes[0]
    ax.scatter(y_pred, residuals, color=ACCENT, edgecolors=GOLD, s=70, zorder=3)
    ax.axhline(0, color=RED_C, linewidth=1.3, linestyle="--")
    _ax_style(ax, " Residuals vs Predicted",
              xlabel="Predicted Score", ylabel="Residual (actual  predicted)")

    # histogram of residuals
    ax2 = axes[1]
    ax2.hist(residuals, bins=max(5, len(residuals)//2),
             color=ACCENT, edgecolor="white", linewidth=0.5)
    ax2.axvline(0, color=RED_C, linewidth=1.3, linestyle="--")
    _ax_style(ax2, " Residual Distribution",
              xlabel="Residual", ylabel="Count")

    plt.tight_layout()
    _save(fig, path)


def _plot_score_distribution(y, path):
    with _mpl.rc_context(_DARK_RC):
        fig, ax = plt.subplots(figsize=(8, 4.5), facecolor=FIG_BG)
        ax.hist(y, bins=max(5, len(y)//2), color=GOLD,
                edgecolor="white", linewidth=0.6, alpha=0.85)
        ax.axvline(float(y.mean()), color=RED_C,   linewidth=1.5,
                   linestyle="--", label=f"Mean  {y.mean():,.0f}")
        ax.axvline(float(y.median()), color=GREEN_C, linewidth=1.5,
                   linestyle=":",  label=f"Median {y.median():,.0f}")
        ax.legend(fontsize=9, facecolor=AX_BG, edgecolor=ACCENT)
        _ax_style(ax, " Score Distribution (all sessions)",
                  title_color=GOLD, xlabel="Score", ylabel="Count")
        plt.tight_layout()
        _save(fig, path)


#
# analysis report
#

def _write_analysis(data: dict, path: str):
    results   = data["results"]
    best_name = data["best_name"]
    y         = data["y"]
    df        = data["df"]
    best_res  = results[best_name]

    lines = []
    w = lines.append

    w("=" * 72)
    w("  FREEDOM FORCE: THE RECKONING  ML MODEL ANALYSIS REPORT")
    w(f"  Generated: {datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}")
    w("=" * 72)
    w("")

    #  Dataset summary
    w(" DATASET ")
    w(f"  Rows (sessions):   {len(y)}")
    w(f"  Features used:     {len(df.columns)}")
    w(f"  Target:            score")
    w(f"  Score range:       {y.min():,.0f}    {y.max():,.0f}")
    w(f"  Mean score:        {y.mean():,.1f}")
    w(f"  Median score:      {y.median():,.1f}")
    w(f"  Std deviation:     {y.std():,.1f}")
    w("")

    #  All features
    w(" FEATURES TRAINED (all columns after preprocessing) ")
    num_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(include=["object","category","string"]).columns.tolist()
    w(f"  Numeric  ({len(num_cols)}):")
    for c in num_cols:
        w(f"      {c}")
    if cat_cols:
        w(f"  Categorical  ({len(cat_cols)})   OHE encoded:")
        for c in cat_cols:
            w(f"      {c}")
    w("")

    #  Model comparison
    w(" MODEL COMPARISON ")
    w(f"  {'Model':<30}  {'CV-MAE':>12}  {'CV-R2':>10}  {'Train-R2':>10}  {'Best?':>6}")
    w("  " + "-" * 64)
    for name, res in results.items():
        flag = " BEST" if name == best_name else ""
        w(f"  {name:<30}  {res['cv_mae']:>12,.1f}  {res['cv_r2']:>10.4f}  {res['train_r2']:>10.4f}  {flag:>6}")
    w("")

    #  Best model detail
    w(f" BEST MODEL: {best_name} ")
    w(f"  CV-MAE   : {best_res['cv_mae']:,.1f}   (cross-validated mean absolute error)")
    w(f"  CV-R2    : {best_res['cv_r2']:.4f}  (cross-validated R2 — reliable estimate)")
    w(f"  Train-R2 : {best_res['train_r2']:.4f}  (R2 on train set — may show overfitting)")
    rmse = float(np.sqrt(np.mean((np.array(y) - best_res['y_pred'])**2)))
    w(f"  RMSE : {rmse:,.1f}")
    w("")

    #  Top-15 feature importances
    if best_res["importances"] is not None:
        w(" TOP-15 FEATURE IMPORTANCES ")
        pairs = sorted(zip(best_res["importances"], best_res["feat_names"]),
                       reverse=True)[:15]
        for rank, (imp, feat) in enumerate(pairs, 1):
            bar = "" * int(imp * 300)
            w(f"  {rank:>2}. {feat:<35}  {imp:.4f}  {bar}")
        w("")

    #  Per-session predictions
    w(" PER-SESSION PREDICTIONS ")
    w(f"  {'#':>3}  {'Actual':>10}  {'Predicted':>12}  {'Error':>10}  {'Error%':>8}")
    w("  " + "-" * 52)
    for i, (actual, pred) in enumerate(zip(y, best_res["y_pred"]), 1):
        err  = actual - pred
        pct  = (err / actual * 100) if actual != 0 else 0
        w(f"  {i:>3}  {actual:>10,.0f}  {pred:>12,.0f}  {err:>10,.0f}  {pct:>7.1f}%")
    w("")
    w("=" * 72)
    w("  END OF REPORT")
    w("=" * 72)

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))



def _write_best_generalizer(data: dict, path: str):
    """
    כותב קובץ טקסט בלבד עבור המודל עם ה-CV-R² הטוב ביותר (הכי מכליל).
    מסביר בשפה פשוטה מה משפיע על הציון.
    """
    results = data["results"]
    y       = data["y"]
    df      = data["df"]

    # בחר לפי CV-R² הכי גבוה (הכי קרוב ל-0 / הכי חיובי)
    best_r2_name = max(results, key=lambda k: results[k]["cv_r2"])
    res          = results[best_r2_name]

    imp   = res["importances"]
    feats = res["feat_names"]

    lines = []
    w = lines.append

    w("=" * 68)
    w("  BEST GENERALIZER MODEL — WHAT DRIVES YOUR SCORE")
    w(f"  Model  : {best_r2_name}")
    w(f"  CV-R2  : {res['cv_r2']:.4f}  (best cross-validated R2 across all models)")
    w(f"  CV-MAE : {res['cv_mae']:,.0f}  (average prediction error in score units)")
    w(f"  Generated: {datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}")
    w("=" * 68)
    w("")

    # ── What affects score ────────────────────────────────────────────────────
    w("WHAT AFFECTS YOUR SCORE — FEATURE INFLUENCE RANKING")
    w("-" * 68)

    if imp is not None:
        pairs  = sorted(zip(imp, feats), reverse=True)
        top    = pairs[:15]
        total  = sum(v for v, _ in pairs)

        # header
        w(f"  {'Rank':<5}  {'Feature':<35}  {'Influence':>10}  {'% of Total':>11}  {'Impact Bar'}")
        w("  " + "-" * 68)

        for rank, (v, feat) in enumerate(top, 1):
            pct      = (v / total * 100) if total > 0 else 0
            bar_len  = int(pct / 2)          # max ~50 chars
            bar      = "#" * bar_len
            # human-readable label
            label = feat
            if feat.startswith("enemy_"):
                label = "kills of " + feat[6:].replace("_", " ")
            elif feat == "stage_reached":
                label = "stage reached"
            elif feat == "lives_lost":
                label = "lives lost (penalty)"
            elif feat == "enemies_killed":
                label = "total enemies killed"
            elif feat == "kills_by_bb":
                label = "kills by BB"
            elif feat == "kills_by_trump":
                label = "kills by Trump"
            elif feat == "boss_fight_duration_sec":
                label = "boss fight duration"
            elif feat == "trump_activations":
                label = "Trump activations"
            elif feat in ("b2_collected","arr_collected","halo_collected"):
                label = feat.replace("_collected","") + " bombs collected"
            elif feat == "total_lasers_fired":
                label = "total lasers fired"
            w(f"  {rank:<5}  {label:<35}  {v:>10.4f}  {pct:>10.1f}%  {bar}")

        w("")
        w("INTERPRETATION")
        w("-" * 68)

        # top 3 explanation
        for rank, (v, feat) in enumerate(top[:3], 1):
            pct   = (v / total * 100) if total > 0 else 0
            label = feat
            if feat.startswith("enemy_"):
                label = "kills of " + feat[6:].replace("_", " ")
            elif feat == "stage_reached":   label = "stage_reached"
            elif feat == "lives_lost":      label = "lives_lost"
            elif feat == "enemies_killed":  label = "enemies_killed"
            elif feat == "boss_fight_duration_sec": label = "boss_fight_duration"

            if feat == "stage_reached":
                tip = "The further you get, the higher the score. Priority: reach later stages."
            elif feat == "lives_lost":
                tip = "Every life lost reduces score. Priority: stay alive."
            elif feat == "enemies_killed":
                tip = "More kills = more points. Priority: clear each stage fully."
            elif feat == "boss_fight_duration_sec":
                tip = "Defeating the boss fast gives a speed bonus. Priority: be aggressive."
            elif feat.startswith("enemy_"):
                enemy = feat[6:].replace("_", " ")
                tip = f"Killing {enemy} contributes to score. Prioritise this enemy type."
            elif feat == "kills_by_trump":
                tip = "Trump kills score more points per kill than BB. Use Trump mode often."
            elif feat == "kills_by_bb":
                tip = "BB laser kills are your main source of points."
            elif feat == "trump_activations":
                tip = "Activating Trump mode more often increases score."
            elif feat == "total_lasers_fired":
                tip = "High laser count with high kills = good accuracy bonus."
            else:
                tip = f"This feature contributes {pct:.1f}% of total model influence."

            w(f"  #{rank}  {label} ({pct:.1f}% influence)")
            w(f"      -> {tip}")
            w("")

    else:
        # linear model — use coefficients
        corr = df.select_dtypes(include="number").corrwith(y).sort_values(key=abs, ascending=False)
        w(f"  (Model has no feature_importances — showing Pearson correlation with score)")
        w("")
        w(f"  {'Rank':<5}  {'Feature':<35}  {'Correlation':>12}  {'Direction'}")
        w("  " + "-" * 65)
        for rank, (feat, c) in enumerate(corr.head(15).items(), 1):
            direction = "POSITIVE (more = higher score)" if c > 0 else "NEGATIVE (more = lower score)"
            w(f"  {rank:<5}  {feat:<35}  {c:>12.4f}  {direction}")

    # ── Score stats ───────────────────────────────────────────────────────────
    w("")
    w("SCORE STATISTICS ACROSS ALL SESSIONS")
    w("-" * 68)
    w(f"  Sessions recorded : {len(y)}")
    w(f"  Highest score     : {y.max():>12,.0f}")
    w(f"  Lowest score      : {y.min():>12,.0f}")
    w(f"  Average score     : {y.mean():>12,.0f}")
    w(f"  Median score      : {y.median():>12,.0f}")
    w(f"  Std deviation     : {y.std():>12,.0f}")
    w("")
    w("  NOTE: CV-R2 is negative because the dataset is small (<30 sessions).")
    w("  As more sessions are recorded, model accuracy will improve.")
    w("  Re-run the ML dashboard (press M) after accumulating more data.")
    w("")
    w("=" * 68)
    w("  END")
    w("=" * 68)

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


#
# public entry point
#

def export(data: dict, base_dir: str) -> str:
    """
    שומר הכל ל- <base_dir>/machine_learning/
    מחזיר את הנתיב של תיקיית machine_learning.
    """
    ml_dir    = os.path.join(base_dir, "machine_learning")
    plots_dir = os.path.join(ml_dir, "plots")
    os.makedirs(plots_dir, exist_ok=True)

    results   = data["results"]
    best_name = data["best_name"]
    y         = data["y"]
    df        = data["df"]

    #  1. save best model pkl
    pkl_path = os.path.join(ml_dir, "best_model.pkl")
    with open(pkl_path, "wb") as f:
        pickle.dump({
            "model_name": best_name,
            "pipeline":   results[best_name]["model"],
            "cv_mae":     results[best_name]["cv_mae"],
            "cv_r2":      results[best_name]["cv_r2"],
            "train_r2":   results[best_name]["train_r2"],
            "feat_names": results[best_name]["feat_names"],
            "trained_at": datetime.now().isoformat(),
        }, f)

    #  2. analysis report
    report_path = os.path.join(ml_dir, "model_analysis.txt")
    try:
        _write_analysis(data, report_path)
    except Exception as e:
        print(f"[ml_exporter] report error: {e}")

    #  3. plots
    plot_jobs = [
        ("01_feature_importance.png",
         lambda p: _plot_feature_importance(best_name, results, p)),
        ("02_correlation.png",
         lambda p: _plot_correlation(df, y, p)),
        ("03_mae_comparison.png",
         lambda p: _plot_mae_comparison(results, p)),
        ("04_predicted_vs_actual.png",
         lambda p: _plot_pred_vs_actual(best_name, results, y, p)),
        ("05_residuals.png",
         lambda p: _plot_residuals(best_name, results, y, p)),
        ("06_score_distribution.png",
         lambda p: _plot_score_distribution(y, p)),
    ]

    saved_plots = []
    for filename, fn in plot_jobs:
        path = os.path.join(plots_dir, filename)
        try:
            fn(path)
            saved_plots.append(filename)
        except Exception as e:
            print(f"[ml_exporter] plot '{filename}' error: {e}")

    # ── best_generalizer folder ──────────────────────────────────────────────
    gen_dir  = os.path.join(ml_dir, "best_generalizer")
    os.makedirs(gen_dir, exist_ok=True)
    gen_path = os.path.join(gen_dir, "what_drives_your_score.txt")
    try:
        _write_best_generalizer(data, gen_path)
    except Exception as e:
        print(f"[ml_exporter] best_generalizer error: {e}")

    print(f"[ml_exporter] Saved to {ml_dir}")
    print(f"              model   best_model.pkl")
    print(f"              report  model_analysis.txt")
    print(f"              plots   {len(saved_plots)} files in plots/")
    print(f"              best_generalizer  what_drives_your_score.txt")
    return ml_dir