import pygame

class BasicSprite(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x:int, y:int) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.x: int = x
        self.y: int = y
    
    def move(self, x: int, y: int) -> None:
        self.rect.topleft = (x + self.x, y + self.y)
    
    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)