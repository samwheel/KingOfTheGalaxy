from random import randint

from pygame.sprite import Sprite
from pygame import Surface
import pygame

from src.star import Star
from src.empire import Empire

class StarView(Sprite):
    def __init__(self, star: Star) -> None:
        super().__init__()
        self.star: Star = star
        color: str = "white"
        for planet in self.star.planets:
            if isinstance(planet.empire, Empire):
                color = planet.empire.color
                break
        
        self.text: Surface = pygame.font.Font(None, 32).render(self.star.name, True, color)
        self.image: Surface = Surface((self.text.get_width() + 2, star.radius*2 + self.text.get_height() + 20), pygame.SRCALPHA)
        self.rect: pygame.Rect = self.image.get_rect(center=star.position)
        pygame.draw.circle(self.image, star.color, (self.rect.size[0] / 2, star.radius), star.radius // 2)
        pygame.draw.line(self.image, star.color, (self.rect.size[0] / 2, 0), (self.rect.size[0] / 2, star.radius * 2), star.radius // 4)
        pygame.draw.line(self.image, star.color, (self.rect.size[0] / 2 - star.radius, star.radius), (self.rect.size[0] / 2 + star.radius, star.radius), star.radius // 4)
        pygame.draw.line(self.image, star.color, (self.rect.size[0] / 2 - star.radius / 2, star.radius / 2), (self.rect.size[0] / 2 + star.radius * .5, star.radius * 1.5), star.radius // 4)
        pygame.draw.line(self.image, star.color, (self.rect.size[0] / 2 + star.radius / 2, star.radius / 2), (self.rect.size[0] / 2 - star.radius * .5, star.radius * 1.5), star.radius // 4)
        self.image.blit(self.text, (0, 25))
    
    def draw(self, surface: Surface) -> None:
        surface.blit(self.image, self.rect)