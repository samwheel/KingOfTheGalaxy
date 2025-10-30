from src.ship import *
from src.year_handler import YearHandler
from src.planet import Planet
from src.build_handler import BuildHandler

class Empire:
    def __init__(self, name:str = "", emperor_name:str = "", color: str = "blue") -> None:
        self.name:str = name
        self.emperor_name: str = emperor_name
        self.year_handler = YearHandler()
        self.planets: list[Planet] = []
        self.build_handler: BuildHandler = BuildHandler(self)
        self.year_handler.add_observer(self.build_handler)
        self.color: str = color
        self.ships: list[Ship] = []
        self.ship_models: list[Ship] = [Ship("Scout MK.1", [RetroRockets(), HydrogenFuel()])]
    
    def __str__(self) -> str:
        return f"Empire {self.name}, Emperor {self.emperor_name}"
    
    @property
    def industry(self) -> float:
        industry = 0
        for planet in self.planets:
            industry += planet.industry
        
        return industry

    def add_planet(self, planet: Planet) -> None:
        self.planets.append(planet)
        self.year_handler.add_observer(planet)
        planet.empire = self
    
    def add_ship(self, ship: Ship) -> None:
        self.ships.append(ship)
        self.year_handler.add_observer(ship)