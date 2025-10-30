import pygame
from pygame import Surface
import math

from src.empire import Empire
from src.planet import Planet
from src.buildings import get_buildings_list, Building
from src.ship import Ship
from src.star import Star

from view.screens import Screen

from pygame_helper.button import Button

class ProductionView(Screen):
    def __init__(self, empire: Empire):
        super().__init__()
        self.empire: Empire = empire
        self.image = pygame.Surface((500, 850))
        self.image.fill(pygame.Color("lightgray"))
        self.rect: pygame.Rect = self.image.get_rect(topleft=(0, 100))
        self.font = pygame.font.Font(None, 36)
        self.building_list_buttons: list[Button] = []
        self.ship_buttons: list[Button] = []

    def update(self, event) -> None:
        for button in self.building_list_buttons:
            button.update(event)
        
        for button in self.ship_buttons:
            button.update(event)
    
    def observer_update(self) -> None:
        for button in self.building_list_buttons:
            button.observer_update()
        
        for button in self.ship_buttons:
            button.observer_update()

    def draw(self, surface: Surface) -> None:
        surface.blit(self.image, self.rect)
        industry_text = self.font.render(f"Total Industry: {math.floor(self.empire.industry * 10 + 0.5) / 10}", True, pygame.Color("black"))
        surface.blit(industry_text, (self.rect.x + 10, self.rect.y + 10))
        build_list_text: list[Surface] = [self.font.render(f"{building_tuple[0].location.name}: ({building_tuple[0]}, {round(building_tuple[1], 1)})", True, pygame.color.Color("black")) for building_tuple in self.empire.build_handler.build_list]
        for building_text in build_list_text:
            surface.blit(building_text, (self.rect.x + 10, self.rect.y + 60 + 50 * build_list_text.index(building_text)))
        
        def add_to_list(building_type: type[Building]):
            self.empire.build_handler.build(building_type(self.current_planet))


        pygame.draw.rect(surface, pygame.Color("white"), pygame.Rect(self.rect.bottomright[0] + 10, self.rect.bottomright[1] - 150, 500, 150))
        self.building_list_buttons: list[Button] = [Button(pygame.Color("black"), str(building(self.current_planet)), self.rect.bottomright[0] + 30, self.rect.bottomright[1] - 130 + 35 * get_buildings_list().index(building), lambda: add_to_list(building)) for building in get_buildings_list()]
        for building_button in self.building_list_buttons:
            building_button.draw(surface)
        
        self.ship_buttons = []

        def create_new_ship(ship: Ship) -> None:
            new_ship: Ship = ship.clone()
            if self.current_planet is not None and isinstance(self.current_planet.star, Star):
                new_ship.location = self.current_planet.star
                self.empire.build_handler.build(new_ship)

        for ship in self.empire.ship_models:
            ship_button = Button(pygame.Color("black"), str(ship), self.rect.bottomright[0] + 30, self.rect.bottomright[1] - 130 + 35 * (len(self.building_list_buttons) + self.empire.ship_models.index(ship)), lambda: create_new_ship(ship))
            ship_button.draw(surface)
            self.ship_buttons.append(ship_button)