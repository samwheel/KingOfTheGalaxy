import pygame

from src.ship import Ship
from src.empire import Empire
from src.observer import Observer

from view.ship_command import ShipCommandView
from view.view_control_interface import ViewControlInterface

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
    
    def observer_update(self, view_controller: ViewControlInterface|None = None) -> None:
        if self.ship.location == self.ship.destination:
            self.ship.destination = None

        if self.ship.location != self.position:
            self.update_position()
        
        if self.ship.location is None:
            self.position = (0, 0)

        if abs(pygame.mouse.get_pos()[0] - self.position[0] - 12) < 20 and abs(pygame.mouse.get_pos()[1] - self.position[1] + 45) < 20:
            if pygame.mouse.get_pressed()[0]:
                if view_controller:
                    ship_command_view = ShipCommandView(self.ship)
                    view_controller.current_view = ship_command_view
            

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.polygon(surface, pygame.Color(self.empire.color), [(self.position[0] + 15, self.position[1] - 50), (self.position[0] + 10, self.position[1] - 40), (self.position[0] + 20, self.position[1] - 40)])