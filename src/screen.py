import pygame
from typing import Any


class Screen:
    BG_COLOR = (15, 15, 25)
    GRID_COLOR = (30, 30, 50)
    HUB_COLORS = {
        "green": (80, 220, 120),
        "blue": (80, 160, 255),
        "red": (255, 100, 100),
        "default": (180, 180, 200),
    }
    CONNECTION_COLOR = (60, 60, 90)
    PATH_COLORS = [
        (255, 220, 50),
        (50, 220, 255),
        (255, 100, 200),
        (100, 255, 150),
        (255, 160, 50),
    ]
    TEXT_COLOR = (220, 220, 240)
    DRONE_RADIUS = 8
    HUB_RADIUS = 22
    FONT_SIZE = 13
    TITLE_FONT_SIZE = 18
    PADDING = 80
    CELL_SIZE = 120

    def __init__(self, width: int = 900, height: int = 1200,
                 title: str = "Fly-In Visualizer") -> None:
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height),
                                              pygame.RESIZABLE | pygame.SCALED)
        pygame.display.set_caption(title)
        self.font = pygame.font.SysFont("monospace", self.FONT_SIZE,
                                        bold=False)
        self.title_font = pygame.font.SysFont("monospace",
                                              self.TITLE_FONT_SIZE,
                                              bold=True)
        self.clock = pygame.time.Clock()
        self.running = True

    def clear(self) -> None:
        self.screen.fill(self.BG_COLOR)

    def draw_text(self, text: str, x: int, y: int,
                  color: Any = None, font: Any = None) -> None:
        color = color or self.TEXT_COLOR
        font = font or self.font
        surface = font.render(text, True, color)
        self.screen.blit(surface, (x, y))

    def flip(self) -> None:
        pygame.display.flip()

    def tick(self, fps: int) -> None:
        self.clock.tick(fps)

    def handle_quit(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
        return self.running

    def quit(self) -> None:
        pygame.quit()
