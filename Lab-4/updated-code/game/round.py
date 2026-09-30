import random
import pygame

class Round:
    def __init__(self, min_wait_ms=1000, max_wait_ms=3000):
        self.wait_delay_ms = random.randint(min_wait_ms, max_wait_ms)
        self.state = "waiting"  # "waiting" -> "go" -> "result"
        self.start_time = pygame.time.get_ticks()
        self.go_time = None
        self.reaction_ms = None
        self.false_start = False

    def update(self):
        if self.state == "waiting":
            now = pygame.time.get_ticks()
            if now - self.start_time >= self.wait_delay_ms:
                self.state = "go"
                # The engine stamps go_time after displaying the green frame.

    def mark_go(self, now=None):
        """Start reaction timing once the green cue has been presented."""
        if self.state == "go" and self.go_time is None:
            self.go_time = pygame.time.get_ticks() if now is None else now

    def register_input(self, now=None):
        """Register a response; return milliseconds, or None for a false start."""
        if self.state == "waiting":
            self.false_start = True
            self.state = "result"
            return None

        if self.state != "go" or self.go_time is None:
            return None

        now = pygame.time.get_ticks() if now is None else now
        self.reaction_ms = max(0, now - self.go_time)
        self.state = "result"
        return self.reaction_ms
