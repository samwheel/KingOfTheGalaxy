from random import choice, randint

from src.planet import Planet
from src.buildings import Buildable

class Star:
    def __init__(self, name: str, position: tuple[int, int], planets: list[Planet]) -> None:
        self.name: str = name
        self.position: tuple[int, int] = position
        self.planets: list[Planet] = planets
        for index, planet in enumerate(self.planets):
            planet.name = self.name + " " + "I" * (index + 1)
        self.ships: list[Buildable] = []
        self.color: str = choice(["red", "green", "blue"])
        self.radius: int = randint(10, 15)