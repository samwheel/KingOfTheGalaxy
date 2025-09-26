from pygame import Surface
from pygame import draw
from pygame import sprite
from pygame import Color
import pygame

from src.planet import Planet, Focus
from pygame_helper import basic_sprite, button

class PlanetView(sprite.Sprite):
    def __init__(self, radius: int, color: Color, planet: Planet, padding: int = 10) -> None:
        super().__init__()
        self.image = None
        self.__sprites = sprite.Group()

        # Add planet logo
        planet_surface = Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        draw.circle(planet_surface, color, (radius, radius), radius)
        planet_sprite = basic_sprite.BasicSprite(planet_surface, 0, 0)
        self.__sprites.add(planet_sprite)

        # Add planet name
        font = pygame.font.Font(None, 36)
        text_surface = font.render(planet.name, True, Color("white"))
        text_sprite = basic_sprite.BasicSprite(text_surface, radius * 2 + padding, radius - text_surface.get_height() // 2)
        self.__sprites.add(text_sprite)

        # Add focus button
        focus_button = button.Button(Color("black"), planet.focus, radius * 2 + padding, radius + padding, action=lambda: self.change_focus())
        self.__sprites.add(focus_button)
        self.planet = planet

    def change_focus(self, focus: Focus | None = None) -> None:
        focus_order = [Focus.INDUSTRY, Focus.RESEARCH, Focus.INFLUENCE, Focus.GROWTH, Focus.DEFENSE]
        self.planet.focus = focus if focus else focus_order[(focus_order.index(self.planet.focus) + 1) % len(focus_order)]
        for sprite in self.__sprites.sprites():
            sprite.__setattr__("text", self.planet.focus) if isinstance(sprite, button.Button) else None

    def move(self, x: int, index: int = 0) -> None:
        for sprite in self.__sprites.sprites():
            sprite.move(x, 50 + index * 160)
    
    def update(self, event) -> None:
        for sprite in self.__sprites.sprites():
            sprite.update(event)

    def draw(self, surface) -> None:
        for sprite in self.__sprites.sprites():
            sprite.draw(surface)