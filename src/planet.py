from enum import StrEnum
from src.race import Race
from src.observer import Observer
from src.buildings import Building

class Focus(StrEnum):
    INDUSTRY = "Industry"
    RESEARCH = "Research"
    GROWTH = "Growth"
    DEFENSE = "Defense"
    INFLUENCE = "Influence"

planet_types: tuple[str, str, str, str, str, str, str, str, str] = (
    "Terran",
    "Desert",
    "Tundra",
    "Barren",
    "Radiated",
    "Inferno",
    "Toxic",
    "Swamp",
    "Ocean"
)

class Planet(Observer):
    def __init__(self, name:str, planet_type: str, race:Race|None = None, population: float = 0, focus:Focus = Focus.INDUSTRY) -> None:
        self.name: str = name
        self.race: Race|None = race
        self.focus: Focus = focus
        self.population: float = population
        self.type: str = planet_type
        self.empire: object|None = None
        if race != None:
            self.max_population: int = -abs(planet_types.index(race.prefered_planet) - planet_types.index(planet_type))
            self.max_population = self.max_population * 5 + 5 if self.max_population > -4 else -10
        else:
            self.max_population: int = 0
        self.buildings: list[Building] = []
    
    def __str__(self) -> str:
        return f"Planet {self.name} focused on {self.focus}"
    
    def __repr__(self) -> str:
        return f"Planet('{self.name}', {repr(self.race)}, {self.population}, {self.type}, {self.focus})"

    @property
    def industry(self) -> float:
        if self.race != None:
            industry_from_focus: float = self.race.industry * self.population if self.focus == Focus.INDUSTRY else 0.0
            industry: float = industry_from_focus
            for building in self.buildings:
                industry += building.production_bonus
            return industry
        else:
            return 0
    
    def observer_update(self) -> None:
        if self.race != None:
            self.population += self.race.population * self.population * (.04 if self.focus == Focus.GROWTH else .02)
            if self.population > self.max_population:
                self.population = self.max_population