import pygame
from pygame import Surface
import math

from src.empire import Empire
from src.planet import Planet
from src.buildings import get_buildings_list, Building
from src.observer import Observer

from pygame_helper.button import Button

class ProductionView(pygame.sprite.Sprite, Observer):
    def __init__(self, empire: Empire):
        super().__init__()
        self.empire: Empire = empire
        self.image = pygame.Surface((500, 800))
        self.image.fill(pygame.Color("lightgray"))
        self.rect: pygame.Rect = self.image.get_rect(topleft=(0, 100))
        self.font = pygame.font.Font(None, 36)
        self.__current_planet: Planet | None = None
        self.building_list_buttons: list[Button] = []

    def set_current_planet(self, planet: Planet):
        self.__current_planet = planet
    
    def update(self, event) -> None:
        for button in self.building_list_buttons:
            button.update(event)
    
    def observer_update(self) -> None:
        for button in self.building_list_buttons:
            button.observer_update()

    def draw(self, surface: Surface) -> None:
        surface.blit(self.image, self.rect)
        industry_text = self.font.render(f"Total Industry: {math.floor(self.empire.industry * 10 + 0.5) / 10}", True, pygame.Color("black"))
        surface.blit(industry_text, (self.rect.x + 10, self.rect.y + 10))
        build_list_text: list[Surface] = [self.font.render(f"{building_tuple[0].planet.name}: ({building_tuple[0]}, {round(building_tuple[1], 1)})", True, pygame.color.Color("black")) for building_tuple in self.empire.build_handler.build_list]
        for building_text in build_list_text:
            surface.blit(building_text, (self.rect.x + 10, self.rect.y + 60 + 50 * build_list_text.index(building_text)))
        
        def add_to_list(building_type: type[Building]):
            self.empire.build_handler.build(building_type(self.__current_planet))


        pygame.draw.rect(surface, pygame.Color("white"), pygame.Rect(self.rect.bottomright[0] + 10, self.rect.bottomright[1] - 100, 500, 100))
        self.building_list_buttons: list[Button] = [Button(pygame.Color("black"), str(building(self.__current_planet)), self.rect.bottomright[0] + 30, self.rect.bottomright[1] - 80 + 50 * get_buildings_list().index(building), lambda: add_to_list(building)) for building in get_buildings_list()]
        for building_button in self.building_list_buttons:
            building_button.draw(surface)