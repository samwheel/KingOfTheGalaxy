from src.year_handler import YearHandler
from src.planet import Planet

class Empire:
    def __init__(self, name:str = "", emperor_name:str = "") -> None:
        self.name:str = name
        self.emperor_name: str = emperor_name
        self.year_handler = YearHandler()
        self.planets: list[Planet] = []
    
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