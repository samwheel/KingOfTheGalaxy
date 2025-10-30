import pygame

from view.planet import PlanetView
from view.ship import ShipView
from view.star import StarView
from view.screens import Screen
from view.view_control_interface import ViewControlInterface

from src.planet import Planet
from src.star import Star

class ViewController(ViewControlInterface):
    def __init__(self) -> None:
        super().__init__()
        self.show_planet_view: bool = False
        self.planet_view_group: list[Planet] = []
    
    def update_views(self, stars: list[Star], player_empire, screen, widgets) -> None:
        for star in stars:
            StarView(star).draw(screen)
        
        for ship in player_empire.ships:
            ship_view = ShipView(ship, player_empire)
            ship_view.draw(screen)
            ship_view.observer_update(view_controller=self)
            
        if self.show_planet_view:
            pygame.draw.rect(screen, (50, 50, 50), pygame.rect.Rect(1400, 50, 350, 900))
            for index, planet in enumerate(self.planet_view_group):
                planet_view = PlanetView(planet)
                planet_view.move(1400, index)
                planet_view.draw(screen)
                planet_view.observer_update()
        
        if self.current_view:
            self.current_view.draw(screen)
            self.current_view.set_current_planet(None)
            try:
                self.current_view.set_current_planet(self.planet_view_group[0])
            except IndexError:
                pass

            self.current_view.observer_update()
        
        for widget in widgets:
            widget.move(0, 0)
            widget.draw(screen)