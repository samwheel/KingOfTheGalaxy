from pygame import Surface
from pygame import draw
from pygame import sprite
from pygame import Color
import pygame
import math

from src.planet import Planet, Focus
from src.observer import Observer
from src.resource_helper import resourcePath

from pygame_helper import basic_sprite, button

class PlanetView(sprite.Sprite, Observer):
    def __init__(self, planet: Planet) -> None:
        super().__init__()
        self.image = None
        self.__sprites = sprite.Group()
        padding = 10
        radius = 50

        # Add planet logo
        planet_surface = pygame.image.load("images/" + planet.type + ".png") 
        planet_sprite = basic_sprite.BasicSprite(planet_surface, 5, 5)
        self.__sprites.add(planet_sprite)

        # Add planet name
        font = pygame.font.Font(None, 36)
        text_surface: Surface = font.render(planet.name, True, Color("white"))
        text_sprite = basic_sprite.BasicSprite(text_surface, radius * 2 + padding, radius - text_surface.get_height())
        self.__sprites.add(text_sprite)

        # Add focus button
        focus_button = button.Button(Color("black"), planet.focus, radius * 2 + padding, radius + padding, action=lambda: self.change_focus(), update_function=lambda: setattr(focus_button, "text", planet.focus))
        self.__sprites.add(focus_button)
        self.planet = planet

        # Planet population
        population_text = button.Button(Color("black"), f"Pop {planet.population}", padding, radius * 2 + padding * 2, update_function=lambda: setattr(population_text, "text", f"Pop {math.floor(planet.population * 10 + 0.5) / 10}"))
        self.__sprites.add(population_text)

        # Planet Production
        production_button = button.ImageButton(
            Color("gray"), 
            button.create_button_surface(pygame.image.load("images/production_icon.png"), str(math.floor(planet.industry * 10 + 0.5) / 10)), 
            padding + 120, 
            radius * 2 + padding * 2, 
            update_function=lambda: setattr(production_button, "surface", button.create_button_surface(pygame.image.load(resourcePath("images/production_icon.png")), str(math.floor(planet.industry * 10 + 0.5) / 10))))
        self.__sprites.add(production_button)
        
        self.building_sprites: list[sprite.Sprite] = []

    def change_focus(self, focus: Focus | None = None) -> None:
        focus_order = [Focus.INDUSTRY, Focus.RESEARCH, Focus.INFLUENCE, Focus.GROWTH, Focus.DEFENSE]
        self.planet.focus = focus if focus else focus_order[(focus_order.index(self.planet.focus) + 1) % len(focus_order)]

    def move(self, x: int, index: int = 0) -> None:
        self.__sprites.remove(self.building_sprites)
        self.building_sprites = []
        for building in self.planet.buildings:
            building_sprite = basic_sprite.BasicSprite(pygame.font.Font(None, 32).render(f"{building}", True, Color("white")), self.planet.buildings.index(building) * 50, 200)
            self.building_sprites.append(building_sprite)
        self.__sprites.add(self.building_sprites)

        for sprite in self.__sprites.sprites():
            sprite.move(x, 50 + index * 160)
    
    def update(self, event) -> None:
        for sprite in self.__sprites.sprites():
            sprite.update(event)
    
    def observer_update(self) -> None:
        for sprite in self.__sprites:
            if isinstance(sprite, Observer):
                sprite.observer_update()

    def draw(self, surface) -> None:
        for sprite in self.__sprites:
            sprite.draw(surface)