from pygame import font, Color, Surface, sprite
import pygame

class Button(sprite.Sprite):
    def __init__(self, color: Color, text: str, x: int, y: int, action = lambda: None) -> None:
        super().__init__()
        self.font = font.Font(None, 36)
        self.color = color
        self.text = text
        self.surface = self.font.render(text, True, color)
        self.rect = self.surface.get_rect()
        self.rect.topleft = (x, y)
        self.x: int = x
        self.y: int = y
        self.action = action
    
    def move(self, x:int, y:int) -> None:
        self.rect.topleft = (x + self.x + 5, y + self.y + 5)
    
    def update(self, event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()
    
    def draw(self, surface: Surface) -> None:
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect(topleft=self.rect.topleft)
        self.rect.inflate_ip(10, 10)
        self.surface = Surface(self.rect.size)
        self.surface.fill("gray")
        self.surface.blit(self.font.render(self.text, True, self.color), (5, 5))
        surface.blit(self.surface, self.rect)

class ImageButton(sprite.Sprite):
    def __init__(self, color: Color, image: Surface, x: int, y: int, action = lambda: None) -> None:
        super().__init__()
        self.color: Color = color
        self.surface: Surface = image
        self.rect: pygame.Rect = self.surface.get_rect()
        self.rect.topleft = (x, y)
        self.x: int = x
        self.y: int = y
        self.action = action
    
    def move(self, x:int, y:int) -> None:
        self.rect.topleft = (x + self.x, y + self.y)
    
    def update(self, event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()
    
    def draw(self, surface: Surface) -> None:
        background: Surface = Surface(self.rect.inflate(10, 10).size)
        background.fill(self.color)
        surface.blit(background, self.rect)
        surface.blit(self.surface, self.rect)