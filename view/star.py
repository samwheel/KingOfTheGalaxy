from pygame.sprite import Sprite, Group
from pygame import Surface, Color
import pygame

from view.planet import PlanetView

class Star(Sprite):
    def __init__(self, x: int, y: int, radius:int, color: Color = Color("yellow"), planets: list[PlanetView] = []) -> None:
        super().__init__()
        self.planets: list[PlanetView] = planets
        self.image: Surface = Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius // 2)
        pygame.draw.line(self.image, color, (radius, 0), (radius, radius*2), radius // 4)
        pygame.draw.line(self.image, color, (0, radius), (radius*2, radius), radius // 4)
        pygame.draw.line(self.image, color, (radius / 2, radius / 2), (radius * 1.5, radius * 1.5), radius // 4)
        pygame.draw.line(self.image, color, (0 + radius / 2, radius * 1.5), (radius * 1.5, radius / 2), radius // 4)
        self.rect = self.image.get_rect(center=(x, y))
    
    def draw(self, surface: Surface):
        surface.blit(self.image, self.rect)