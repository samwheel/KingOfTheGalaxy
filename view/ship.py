import pygame

from src.ship import Ship
from src.empire import Empire

class ShipView(pygame.sprite.Sprite):
    def __init__(self, ship: Ship, empire: Empire) -> None:
        super().__init__()
        self.ship: Ship = ship
        if ship.location is None:
            self.position: tuple[int, int] = (0, 0)
        elif isinstance(ship.location, tuple):
            self.position: tuple[int, int] = ship.location
        elif hasattr(ship.location, "position"):
            self.position: tuple[int, int] = ship.location.position
        else:
            self.position: tuple[int, int] = (0, 0)
        self.empire: Empire = empire
        
    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(pygame.font.Font(None, 24).render("^", True, pygame.Color(self.empire.color)), (self.position[0] + 10, self.position[1] - 40))