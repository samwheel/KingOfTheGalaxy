import pygame
import math

from src.empire import Empire

class ProductionView(pygame.sprite.Sprite):
    def __init__(self, empire: Empire):
        super().__init__()
        self.empire: Empire = empire
        self.image = pygame.Surface((300, 400))
        self.image.fill(pygame.Color("lightgray"))
        self.rect: pygame.Rect = self.image.get_rect(topleft=(0, 100))
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)
        industry_text = self.font.render(f"Total Industry: {math.floor(self.empire.industry * 10 + 0.5) / 10}", True, pygame.Color("black"))
        surface.blit(industry_text, (self.rect.x + 10, self.rect.y + 10))