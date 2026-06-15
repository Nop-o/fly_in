import pygame
from typing import Any


class Screen:
    PATH_COLORS = [
        pygame.Color("yellow"),
        pygame.Color("aquamarine1"),
        pygame.Color("pink"),
        pygame.Color("green"),
        pygame.Color("orange"),
    ]
    DRONE_RADIUS = 8

    def __init__(self, width: int = 900, height: int = 1200,
                 title: str = "Fly-In Visualizer") -> None:
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height),
                                              pygame.RESIZABLE)
        pygame.display.set_caption(title)
        self.font = pygame.font.SysFont("monospace", 13, bold=False)
        self.title_font = pygame.font.SysFont("monospace", 18, bold=True)
        self.clock = pygame.time.Clock()

    def clear_last_frame(self) -> None:
        """Clear the last frame, recover it with a black screen"""
        self.screen.fill(pygame.Color("black"))

    def draw_text(self, text: str, x: int, y: int,
                  color: tuple[int, int, int] = pygame.Color("gray44"),
                  font: Any = None) -> None:
        """Draw text into the simulation"""
        if font is None:
            font = self.font

        surface = font.render(text, True, color)
        self.screen.blit(surface, (x, y))

    def set_fps(self, fps: int) -> None:
        """"Set simualtion FPS (Frame Per Second)"""
        self.clock.tick(fps)

    @staticmethod
    def display_on_screen() -> None:
        """Display everything that you prepared to the screen"""
        pygame.display.flip()

    @staticmethod
    def exit_simulation() -> None:
        """Exit simulation"""
        pygame.quit()
