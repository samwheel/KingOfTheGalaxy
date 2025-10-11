from src.planet import Planet
from src.buildings import Buildable

class Star:
    def __init__(self, name: str, position: tuple[int, int], planets: list[Planet]) -> None:
        self.name: str = name
        self.position: tuple[int, int] = position
        self.planets: list[Planet] = planets
        for planet in self.planets:
            planet.name = name + " " + "I" * self.planets.index(planet)
        self.ships: list[Buildable] = []