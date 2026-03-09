"""
stats_recorder.py
-----------------
עוקב אחר סטטיסטיקות המשחק ושומר ב-data/record.csv
שדות חדשים:
  - kills_by_enemy  : מילון  {שם_אויב: מספר_הריגות}
  - kills_by_bb     : כמה אויבים הרג BB
  - kills_by_trump  : כמה אויבים הרג Trump
  - boss_fight_duration_sec : זמן (שניות) ממפגש עם הבוס עד ניצחון/מוות
"""
import csv, os, json
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
CSV_PATH = os.path.join(DATA_DIR, "record.csv")

FIELDNAMES = [
    "id", "score",
    "date", "time", "session_duration_sec",
    "stage_reached", "reached_boss", "defeated_boss", "outcome",
    "enemies_killed",
    "kills_by_bb", "kills_by_trump",
    "kills_by_enemy",           # JSON: {"Nasrallah": 5, "Fouad-Shukr": 3}
    "boss_fight_duration_sec",  # שניות בשלב הבוס
    "trump_activations",
    "b2_collected", "arr_collected", "halo_collected",
    "antibombs_collected", "energy_spheres_collected",
    "ammo_pickups_collected", "weapon_pickups_collected",
    "damage_x_hits", "total_lasers_fired", "lives_lost",
]


def _get_next_id(rows):
    if not rows: return 1
    max_id = 0
    for r in rows:
        try: max_id = max(max_id, int(r.get("id", 0)))
        except: pass
    return max_id + 1


def calculate_score(
    stage_reached, outcome, game_time_sec,
    enemies_killed, lives_lost, total_lasers,
    defeated_boss=False, boss_fight_sec=0.0,
    kills_by_bb=0, kills_by_trump=0,
):
    """
    ניקוד חדש — שלב הבוס הוא הגורם המכריע.

    stage_score      = stage × 1000
    victory_bonus    = 8000  (רק ניצחון)
    boss_speed_bonus = max(0, 10000 - boss_fight_sec × 50)  ← הכי גדול אם ניצחת מהר
    speed_bonus      = max(0, 3000 × stage / (minutes+1))
    enemy_bonus      = enemies × 10
    accuracy_bonus   = (enemies/lasers) × 500  אם > 30%
    character_bonus  = bb_kills × 5 + trump_kills × 8  (trump חזק יותר = פחות נקודות)
    life_penalty     = lives × 150
    """
    stage_score   = stage_reached * 1_300
    victory_bonus = 15_000 if outcome == "victory" else 0

    # בוס — הגורם המכריע
    if defeated_boss:
        boss_speed_bonus = max(0, int(10_000 - boss_fight_sec * 50))
    else:
        boss_speed_bonus = 0

    minutes      = game_time_sec / 60.0
    speed_bonus  = max(0, int(3_000 * stage_reached / max(0.5, minutes)))
    enemy_bonus  = enemies_killed * 200

    lasers   = max(1, total_lasers)
    accuracy = enemies_killed / lasers
    accuracy_bonus = int(accuracy * 500) if accuracy > 0.3 else 0

    character_bonus = kills_by_bb * 25 + kills_by_trump * 50

    life_penalty = lives_lost * 220

    total = (stage_score + victory_bonus + boss_speed_bonus
             + speed_bonus + enemy_bonus + accuracy_bonus
             + character_bonus - life_penalty) - 5000
    return max(0, total)


class StatsRecorder:
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.reset()

    def reset(self):
        self.start_time          = None
        self.enemies_killed      = 0
        self.trump_activations   = 0
        self.b2_collected        = 0
        self.arr_collected       = 0
        self.halo_collected      = 0
        self.antibombs_collected = 0
        self.energy_spheres      = 0
        self.ammo_pickups        = 0
        self.weapon_pickups      = 0
        self.damage_x_hits       = 0
        self.total_lasers_fired  = 0
        self.lives_lost          = 0
        self._saved              = False
        self._last_score         = 0
        # חדש
        self.kills_by_enemy: dict = {}   # {enemy_name: count}
        self.kills_by_bb    = 0
        self.kills_by_trump = 0
        self._boss_start_time = None     # מתי התחיל שלב הבוס
        self.boss_fight_sec   = 0.0

    def start_session(self):
        self.start_time = datetime.now()
        self._saved     = False

    def start_boss_fight(self):
        """קרא כשמתחיל שלב הבוס."""
        self._boss_start_time = datetime.now()

    def end_boss_fight(self):
        """קרא כשהבוס מת או השחקן מת בשלב הבוס."""
        if self._boss_start_time:
            self.boss_fight_sec = (datetime.now() - self._boss_start_time).total_seconds()
            self._boss_start_time = None

    @property
    def elapsed(self):
        if self.start_time is None: return 0.0
        return (datetime.now() - self.start_time).total_seconds()

    # ── event trackers ───────────────────────────────────────────────────────
    def on_enemy_killed(self, enemy_name="", player_state="bb"):
        self.enemies_killed += 1
        if enemy_name:
            self.kills_by_enemy[enemy_name] = self.kills_by_enemy.get(enemy_name, 0) + 1
        if player_state == "trump":
            self.kills_by_trump += 1
        else:
            self.kills_by_bb += 1

    def on_trump_activated(self): self.trump_activations  += 1
    def on_laser_fired(self):     self.total_lasers_fired += 1
    def on_life_lost(self):       self.lives_lost         += 1

    def on_powerup_collected(self, kind):
        mapping = {
            "b2_bomb":       "b2_collected",
            "arrow_bomb":    "arr_collected",
            "halo_bomb":     "halo_collected",
            "antibomb":      "antibombs_collected",
            "energy_sphere": "energy_spheres",
            "ammo_pickup":   "ammo_pickups",
            "weapon_pickup": "weapon_pickups",
            "damage_x":      "damage_x_hits",
        }
        attr = mapping.get(kind)
        if attr:
            setattr(self, attr, getattr(self, attr) + 1)

    # ── score ────────────────────────────────────────────────────────────────
    def get_score(self, stage_reached, outcome):
        score = calculate_score(
            stage_reached   = stage_reached,
            outcome         = outcome,
            game_time_sec   = self.elapsed,
            enemies_killed  = self.enemies_killed,
            lives_lost      = self.lives_lost,
            total_lasers    = self.total_lasers_fired,
            defeated_boss   = (outcome == "victory"),
            boss_fight_sec  = self.boss_fight_sec,
            kills_by_bb     = self.kills_by_bb,
            kills_by_trump  = self.kills_by_trump,
        )
        self._last_score = score
        return score

    # ── save ─────────────────────────────────────────────────────────────────
    def save(self, stage_reached, outcome):
        now = datetime.now()
        if self.start_time is None: self.start_time = now
        duration = self.elapsed

        score = calculate_score(
            stage_reached  = stage_reached,
            outcome        = outcome,
            game_time_sec  = duration,
            enemies_killed = self.enemies_killed,
            lives_lost     = self.lives_lost,
            total_lasers   = self.total_lasers_fired,
            defeated_boss  = (outcome == "victory"),
            boss_fight_sec = self.boss_fight_sec,
            kills_by_bb    = self.kills_by_bb,
            kills_by_trump = self.kills_by_trump,
        )
        self._last_score = score

        try:
            os.makedirs(DATA_DIR, exist_ok=True)
            existing_rows = []
            if os.path.isfile(CSV_PATH):
                with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
                    for row in csv.DictReader(f):
                        existing_rows.append(row)

            next_id = _get_next_id(existing_rows)

            new_row = {
                "id":                        next_id,
                "score":                     score,
                "date":                      now.strftime("%Y-%m-%d"),
                "time":                      now.strftime("%H:%M:%S"),
                "session_duration_sec":      round(duration, 1),
                "stage_reached":             stage_reached,
                "reached_boss":              stage_reached >= 11,
                "defeated_boss":             outcome == "victory",
                "outcome":                   outcome,
                "enemies_killed":            self.enemies_killed,
                "kills_by_bb":               self.kills_by_bb,
                "kills_by_trump":            self.kills_by_trump,
                "kills_by_enemy":            json.dumps(self.kills_by_enemy, ensure_ascii=False),
                "boss_fight_duration_sec":   round(self.boss_fight_sec, 1),
                "trump_activations":         self.trump_activations,
                "b2_collected":              self.b2_collected,
                "arr_collected":             self.arr_collected,
                "halo_collected":            self.halo_collected,
                "antibombs_collected":       self.antibombs_collected,
                "energy_spheres_collected":  self.energy_spheres,
                "ammo_pickups_collected":    self.ammo_pickups,
                "weapon_pickups_collected":  self.weapon_pickups,
                "damage_x_hits":             self.damage_x_hits,
                "total_lasers_fired":        self.total_lasers_fired,
                "lives_lost":                self.lives_lost,
            }

            existing_rows.append(new_row)
            existing_rows.sort(key=lambda r: int(r.get("score", 0)), reverse=True)

            with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore")
                writer.writeheader()
                for r in existing_rows:
                    writer.writerow(r)

            self._saved = True
            print(f"[stats] Saved — score: {score:,}  →  {CSV_PATH}")
            return True

        except Exception as e:
            print(f"[stats] ERROR saving: {e}")
            return False