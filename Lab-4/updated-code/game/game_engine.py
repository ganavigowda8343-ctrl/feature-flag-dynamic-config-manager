import array
import math
import pygame
from .round import Round

# Game Engine

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (90, 90, 90)
GREEN = (40, 180, 90)
BLUE = (50, 90, 170)
DARK_BLUE = (28, 45, 86)
YELLOW = (255, 220, 90)

DIFFICULTIES = {
    "Easy": {"min_wait_ms": 1000, "max_wait_ms": 2500, "rounds_total": 5},
    "Medium": {"min_wait_ms": 1500, "max_wait_ms": 3500, "rounds_total": 8},
    "Hard": {"min_wait_ms": 2000, "max_wait_ms": 5000, "rounds_total": 10},
}

class GameEngine:
    def __init__(self, width, height, rounds_total=8, min_wait_ms=1500, max_wait_ms=3500):
        self.width = width
        self.height = height
        self.difficulty = "Medium"
        self.screen_state = "playing"
        self.exit_requested = False
        self.min_wait_ms = min_wait_ms
        self.max_wait_ms = max_wait_ms
        self.rounds_total = rounds_total
        self.reaction_times = []
        self.round = Round(self.min_wait_ms, self.max_wait_ms)
        self.result_shown_at = None
        self.result_pause_ms = 800

        self.font = pygame.font.SysFont("Arial", 30)
        self.big_font = pygame.font.SysFont("Arial", 46)
        self.small_font = pygame.font.SysFont("Arial", 21)
        self.game_over = False
        self._initialize_audio()

    def _initialize_audio(self):
        """Create short synthesized cues; audio is optional on unsupported systems."""
        self.sounds = {}
        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init(frequency=22050, size=-16, channels=1)
            self.sounds = {
                "go": self._make_tone(880, 120),
                "false_start": self._make_tone(190, 220),
                "session_end": self._make_tone(660, 300),
            }
        except (pygame.error, OSError):
            self.sounds = {}

    @staticmethod
    def _make_tone(frequency, duration_ms):
        sample_rate = 22050
        sample_count = int(sample_rate * duration_ms / 1000)
        amplitude = 7000
        samples = array.array(
            "h",
            (
                int(amplitude * math.sin(2 * math.pi * frequency * index / sample_rate))
                for index in range(sample_count)
            ),
        )
        return pygame.mixer.Sound(buffer=samples.tobytes())

    def _play_sound(self, name):
        sound = self.sounds.get(name)
        if sound is not None:
            try:
                sound.play()
            except (pygame.error, OSError):
                pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q):
            self.exit_requested = True
            return

        is_click = event.type == pygame.MOUSEBUTTONDOWN
        is_space = event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
        is_confirm = event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER)

        if self.screen_state == "playing" and (is_click or is_space):
            if self.round.state not in ("waiting", "go"):
                return
            reaction_ms = self.round.register_input()
            self.reaction_times.append(reaction_ms)
            self.result_shown_at = pygame.time.get_ticks()
            if self.round.false_start:
                self._play_sound("false_start")
        elif self.screen_state == "results" and (is_click or is_space or is_confirm):
            self.screen_state = "difficulty_menu"
        elif self.screen_state == "difficulty_menu":
            if event.type == pygame.KEYDOWN:
                key_difficulties = {
                    pygame.K_1: "Easy",
                    pygame.K_2: "Medium",
                    pygame.K_3: "Hard",
                }
                selected = key_difficulties.get(event.key)
                if selected is not None:
                    self._start_session(selected)
            elif is_click:
                for name, rect in self._difficulty_buttons().items():
                    if rect.collidepoint(event.pos):
                        self._start_session(name)
                        break

    def handle_input(self):
        # Reserved for continuously-held-key input; every action here
        # is a discrete click/keypress, handled in handle_event.
        pass

    def update(self):
        if self.screen_state != "playing":
            return

        self.round.update()

        if self.round.state == "result":
            now = pygame.time.get_ticks()
            if self.result_shown_at is not None and now - self.result_shown_at >= self.result_pause_ms:
                self._start_next_round()

    def after_present(self):
        """Begin timing and play the cue only after the green frame is displayed."""
        if self.screen_state == "playing" and self.round.state == "go" and self.round.go_time is None:
            self.round.mark_go(pygame.time.get_ticks())
            self._play_sound("go")

    def _start_next_round(self):
        if len(self.reaction_times) >= self.rounds_total:
            self.game_over = True
            self.screen_state = "results"
            self._play_sound("session_end")
            return
        self.round = Round(self.min_wait_ms, self.max_wait_ms)
        self.result_shown_at = None

    def _start_session(self, difficulty):
        settings = DIFFICULTIES[difficulty]
        self.difficulty = difficulty
        self.rounds_total = settings["rounds_total"]
        self.min_wait_ms = settings["min_wait_ms"]
        self.max_wait_ms = settings["max_wait_ms"]
        self.reaction_times = []
        self.round = Round(self.min_wait_ms, self.max_wait_ms)
        self.result_shown_at = None
        self.game_over = False
        self.screen_state = "playing"

    def average_reaction_ms(self):
        valid_reactions = [value for value in self.reaction_times if value is not None]
        if not valid_reactions:
            return 0
        return round(sum(valid_reactions) / len(valid_reactions))

    def render(self, screen):
        if self.screen_state == "results":
            self._render_results(screen)
            return
        if self.screen_state == "difficulty_menu":
            self._render_difficulty_menu(screen)
            return

        if self.round.state == "waiting":
            bg = GRAY
            message = "Wait for green..."
        elif self.round.state == "go":
            bg = GREEN
            message = "Click now!"
        else:
            bg = BLUE
            message = "False start!" if self.round.false_start else f"{self.round.reaction_ms} ms"

        screen.fill(bg)

        text_surf = self.big_font.render(message, True, WHITE)
        text_rect = text_surf.get_rect(center=(self.width // 2, self.height // 2))
        screen.blit(text_surf, text_rect)

        round_num = min(len(self.reaction_times) + 1, self.rounds_total)
        round_text = self.font.render(f"Round {round_num}/{self.rounds_total}", True, WHITE)
        screen.blit(round_text, (10, 10))

        avg_text = self.font.render(f"Avg: {self.average_reaction_ms()} ms", True, WHITE)
        screen.blit(avg_text, (self.width - 190, 10))

        difficulty_text = self.small_font.render(self.difficulty, True, WHITE)
        screen.blit(difficulty_text, (10, self.height - 32))

    def _render_results(self, screen):
        screen.fill(DARK_BLUE)
        title = self.big_font.render("Session Results", True, WHITE)
        screen.blit(title, title.get_rect(center=(self.width // 2, 42)))

        difficulty = self.font.render(f"{self.difficulty}  |  {self.rounds_total} rounds", True, YELLOW)
        screen.blit(difficulty, difficulty.get_rect(center=(self.width // 2, 89)))

        row_height = 21
        start_y = 122
        for index, reaction_ms in enumerate(self.reaction_times):
            if reaction_ms is None:
                result = "False start"
            else:
                result = f"{reaction_ms} ms"
            row = self.small_font.render(f"Round {index + 1}:  {result}", True, WHITE)
            screen.blit(row, row.get_rect(center=(self.width // 2, start_y + index * row_height)))

        valid_reactions = [value for value in self.reaction_times if value is not None]
        average = "No valid reactions" if not valid_reactions else f"Average: {self.average_reaction_ms()} ms"
        average_text = self.font.render(average, True, YELLOW)
        screen.blit(average_text, average_text.get_rect(center=(self.width // 2, self.height - 58)))
        prompt = self.small_font.render("Space / click: replay options    Esc / Q: quit", True, WHITE)
        screen.blit(prompt, prompt.get_rect(center=(self.width // 2, self.height - 22)))

    def _difficulty_buttons(self):
        button_width = min(155, (self.width - 80) // 3)
        gap = 15
        total_width = button_width * 3 + gap * 2
        left = (self.width - total_width) // 2
        button_y = self.height // 2 - 15
        return {
            name: pygame.Rect(left + index * (button_width + gap), button_y, button_width, 120)
            for index, name in enumerate(DIFFICULTIES)
        }

    def _render_difficulty_menu(self, screen):
        screen.fill(DARK_BLUE)
        title = self.big_font.render("Choose Difficulty", True, WHITE)
        screen.blit(title, title.get_rect(center=(self.width // 2, 80)))

        buttons = self._difficulty_buttons()
        for index, (name, settings) in enumerate(DIFFICULTIES.items(), start=1):
            rect = buttons[name]
            pygame.draw.rect(screen, BLUE, rect, border_radius=10)
            pygame.draw.rect(screen, WHITE, rect, width=2, border_radius=10)
            name_text = self.font.render(f"{index}. {name}", True, WHITE)
            rounds_text = self.small_font.render(f"{settings['rounds_total']} rounds", True, WHITE)
            wait_text = self.small_font.render(
                f"{settings['min_wait_ms'] / 1000:g}-{settings['max_wait_ms'] / 1000:g}s wait",
                True,
                WHITE,
            )
            screen.blit(name_text, name_text.get_rect(center=(rect.centerx, rect.y + 35)))
            screen.blit(rounds_text, rounds_text.get_rect(center=(rect.centerx, rect.y + 68)))
            screen.blit(wait_text, wait_text.get_rect(center=(rect.centerx, rect.y + 94)))

        prompt = self.small_font.render("Press 1, 2, or 3 / click a difficulty    Esc / Q: quit", True, WHITE)
        screen.blit(prompt, prompt.get_rect(center=(self.width // 2, self.height - 32)))
