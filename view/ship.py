import pygame

from src.ship import Ship
from src.empire import Empire
from src.observer import Observer

from view.ship_command import ShipCommandView

class ShipView(pygame.sprite.Sprite, Observer):
    def __init__(self, ship: Ship, empire: Empire) -> None:
        super().__init__()
        self.ship: Ship = ship
        self.position: tuple[int, int] = (0, 0)
        self.update_position()
        self.empire: Empire = empire
    
    def update_position(self) -> None:
        if self.ship.location is None:
            self.position = (0, 0)
        elif isinstance(self.ship.location, tuple):
            self.position = self.ship.location
        elif hasattr(self.ship.location, "position"):
            self.position = self.ship.location.position
        else:
            self.position = (0, 0)
    
    def observer_update(self, view_controller = None) -> None:
        if self.ship.location != self.ship.destination and self.ship.destination is not None:
            self.ship.location = self.ship.destination
            self.update_position()

        if self.ship.location == self.ship.destination:
            self.ship.destination = None
        
        if self.ship.location is None:
            self.position = (0, 0)
        
        surface = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.draw(surface)
        
        if surface.get_rect().collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                ship_command_view = ShipCommandView(self.ship)
                view_controller.current_view = ship_command_view
            

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.polygon(surface, pygame.Color(self.empire.color), [(self.position[0] + 15, self.position[1] - 50), (self.position[0] + 10, self.position[1] - 40), (self.position[0] + 20, self.position[1] - 40)])