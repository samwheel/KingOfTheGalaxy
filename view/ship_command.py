import pygame

from src.ship import Ship

from view.screens import Screen

class ShipCommandView(Screen):
    def __init__(self, ship: Ship) -> None:
        super().__init__()
        self.ship: Ship = ship
    
    def draw(self, surface: pygame.Surface) -> None:
        font = pygame.font.Font(None, 30)
        lines = [
            f"Ship Command",
            f"-------------",
            f"Location: {self.ship.location}",
            f"Destination: {self.ship.destination}",
            f"Speed: {self.ship.speed}",
        ]
        for i, line in enumerate(lines):
            text_surf: pygame.Surface = font.render(line, True, pygame.Color("white"))
            surface.blit(text_surf, (10, 10 + i * 30))