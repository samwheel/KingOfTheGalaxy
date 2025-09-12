from enum import StrEnum
from src.race import Race

class Focus(StrEnum):
    PRODUCTION = "production"
    RESEARCH = "research"
    GROWTH = "growth"
    DEFENSE = "defense"
    INFLUENCE = "influence"

class Planet:
    def __init__(self, name:str, race:Race, population: int, focus:Focus = Focus.PRODUCTION) -> None:
        self.name: str = name
        self.race: Race = race
        self.focus: Focus = focus
        self.population:int = population
    
    def __str__(self) -> str:
        return f"Planet {self.name} focused on {self.focus}"
    
    def __repr__(self) -> str:
        return f"Planet('{self.name}', {repr(self.race)}, {self.population}, {self.focus})"