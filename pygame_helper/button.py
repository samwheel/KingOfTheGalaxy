from pygame import font, Color, Surface, sprite
import pygame

from src.observer import Observer

def create_button_surface(image: Surface, value: str) -> Surface:
    surface = Surface((100, 35))
    surface.fill(Color("gray"))
    surface.blit(image, (5, 5))
    prod_text = pygame.font.Font(None, 36).render(value, True, Color("black"))
    surface.blit(prod_text, (40, 5))
    return surface

class Button(sprite.Sprite, Observer):
    def __init__(self, color: Color, text: str, x: int, y: int, action = lambda: None, update_function = lambda: None) -> None:
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
        self.update_function = update_function
    
    def move(self, x:int, y:int) -> None:
        self.rect.topleft = (x + self.x + 5, y + self.y + 5)
    
    def update(self, event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()
    
    def observer_update(self) -> None:
        self.update_function()
    
    def draw(self, surface: Surface) -> None:
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect(topleft=self.rect.topleft)
        self.rect.inflate_ip(10, 10)
        self.surface = Surface(self.rect.size)
        self.surface.fill("gray")
        self.surface.blit(self.font.render(self.text, True, self.color), (5, 5))
        surface.blit(self.surface, self.rect)

class ImageButton(sprite.Sprite, Observer):
    def __init__(self, color: Color, image: Surface, x: int, y: int, action = lambda: None, update_function = lambda: None) -> None:
        super().__init__()
        self.color: Color = color
        self.surface: Surface = image
        self.rect: pygame.Rect = self.surface.get_rect()
        self.rect.topleft = (x, y)
        self.x: int = x
        self.y: int = y
        self.action = action
        self.update_function = update_function
    
    def move(self, x:int, y:int) -> None:
        self.rect.topleft = (x + self.x, y + self.y)
    
    def update(self, event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()
    
    def observer_update(self) -> None:
        self.update_function()
    
    def draw(self, surface: Surface) -> None:
        background: Surface = Surface(self.rect.size)
        background.fill(self.color)
        surface.blit(background, self.rect)
        surface.blit(self.surface, self.rect)