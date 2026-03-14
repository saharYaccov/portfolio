"""
main.py – Freedom Force: The Reckoning
=======================================
Flow:
    1. TitleScreen  — Space → start game,  R → rules
    2. RulesScreen  — Back  → title
    3. Game.run()   — takes over completely (its own loop)

Note: Game creates its OWN pygame window in __init__.
      We therefore do NOT call pygame.display.set_mode() here.
      We only run the pre-game screens using a temporary surface,
      then let Game.__init__ create the real window.
"""

import sys
import os
import pygame

# ── make sure src/ is on the path ─────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR  = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from src.screens import TitleScreen, RulesScreen, MobileControls, AboutScreen


def _start_background_music():
    """
    Load and start looping background music from the assets folder (if available).
    Runs safely even if the mixer or file is missing.
    """
    assets_dir = os.path.join(BASE_DIR, "assets")
    if not os.path.isdir(assets_dir):
        return

    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        # Check both assets/ and assets/sounds/ directories
        search_dirs = [
            assets_dir,
            os.path.join(assets_dir, "sounds")
        ]
        
        for search_dir in search_dirs:
            if not os.path.isdir(search_dir):
                continue
            for name in os.listdir(search_dir):
                if name.lower().endswith((".ogg", ".mp3", ".wav")):
                    path = os.path.join(search_dir, name)
                    try:
                        pygame.mixer.music.load(path)
                        pygame.mixer.music.set_volume(0.6)
                        pygame.mixer.music.play(-1)  # loop forever
                        print(f"[audio] background music loaded from {path}")
                        return
                    except Exception as e:
                        print(f"[audio] failed to load {path}: {e}")
        print("[audio] no music file found in assets/ or assets/sounds/")
    except Exception as e:
        print(f"[audio] mixer init / play failed: {e}")

SCREEN_W = 1280
SCREEN_H = 720
FPS      = 60


def run_pre_screens():
    """
    Show TitleScreen + optional RulesScreen.
    Returns the chosen device ("pc" or "mobile") when the user
    presses Space to start, or None if they quit.
    """
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Freedom Force – The Reckoning")
    clock = pygame.time.Clock()

    # start global background music for the whole game session (if available)
    _start_background_music()

    title  = TitleScreen(screen, clock)
    rules  = None
    about  = None
    state  = "title"   # "title" | "rules" | "about"

    while True:
        if state == "title":
            result = title.update()
            title.draw()

            if result == "start":
                device = title.get_device()
                difficulty = title.get_difficulty()
                # destroy this window — Game will create its own
                pygame.display.quit()
                return device, difficulty

            elif result == "rules":
                rules = RulesScreen(screen, clock)
                state = "rules"

            elif result == "about":
                about = AboutScreen(screen, clock)
                state = "about"

        elif state == "rules":
            result = rules.update()
            rules.draw()

            if result == "back":
                # rebuild title keeping device + difficulty choice
                saved_device = title.get_device()
                saved_diff   = title.get_difficulty()
                title = TitleScreen(screen, clock)
                title.device = saved_device
                title.difficulty = saved_diff
                state = "title"

        elif state == "about":
            result = about.update()
            about.draw()

            if result == "back":
                saved_device = title.get_device()
                saved_diff   = title.get_difficulty()
                title = TitleScreen(screen, clock)
                title.device = saved_device
                title.difficulty = saved_diff
                state = "title"

        clock.tick(FPS)


def main():
    result = run_pre_screens()

    if result is None:
        sys.exit()

    device, difficulty = result

    # ── configure difficulty-dependent enemy behaviour ─────────────────────
    try:
        from src.enemy import set_difficulty
        set_difficulty(difficulty)
    except Exception as e:
        print(f"[difficulty] failed to configure enemies: {e}")

    # ── launch the real game ───────────────────────────────────────────────
    # Game.__init__ calls pygame.init() + creates its own display window.
    from src.game_loop import Game

    game = Game(base_dir=BASE_DIR, difficulty=difficulty)

    # if mobile — attach on-screen controls
    if device == "mobile":
        _run_with_mobile(game)
    else:
        game.run()   # standard PC loop


def _run_with_mobile(game):
    """
    Wrap Game.run() for mobile: inject on-screen buttons.
    We monkey-patch the event loop inside game so mobile buttons
    are processed alongside keyboard events.
    """
    overlay = MobileControls(game.screen)

    # Save original _handle_event
    _orig_handle = game._handle_event

    def _patched_handle(event):
        overlay.handle_event(event)
        _orig_handle(event)

    game._handle_event = _patched_handle

    # Save original _draw
    _orig_draw = game._draw

    def _patched_draw(dt):
        _orig_draw(dt)
        overlay.draw()
        # inject held mobile keys as synthetic key states
        # (optional enhancement — currently overlay only handles events)

    game._draw = _patched_draw

    game.run()


if __name__ == "__main__":
    main()