from pygame.sprite import Sprite, Group
from pygame import Surface, Color
import pygame

from src.star import Star

class StarView(Sprite):
    def __init__(self, star: Star, radius: int, color: Color = Color("yellow")) -> None:
        super().__init__()
        self.star: Star = star
        self.image: Surface = Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius // 2)
        pygame.draw.line(self.image, color, (radius, 0), (radius, radius*2), radius // 4)
        pygame.draw.line(self.image, color, (0, radius), (radius*2, radius), radius // 4)
        pygame.draw.line(self.image, color, (radius / 2, radius / 2), (radius * 1.5, radius * 1.5), radius // 4)
        pygame.draw.line(self.image, color, (0 + radius / 2, radius * 1.5), (radius * 1.5, radius / 2), radius // 4)
        self.rect = self.image.get_rect(center=star.position)
    
    def draw(self, surface: Surface):
        surface.blit(self.image, self.rect)