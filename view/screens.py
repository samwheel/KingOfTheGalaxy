import pygame

from src.observer import Observer
from src.planet import Planet

class Screen(pygame.sprite.Sprite, Observer):
    def __init__(self) -> None:
        self.current_planet: Planet | None = None

    def update(self, event) -> None:
        pass

    def set_current_planet(self, planet: Planet | None) -> None:
        self.current_planet = planet

    def draw(self, surface: pygame.Surface) -> None:
        pass