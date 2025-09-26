from enum import StrEnum
from typing import Literal
from src.race import Race
from src.observer import Observer

class Focus(StrEnum):
    INDUSTRY = "Industry"
    RESEARCH = "Research"
    GROWTH = "Growth"
    DEFENSE = "Defense"
    INFLUENCE = "Influence"

class Planet(Observer):
    def __init__(self, name:str, race:Race, population: float, focus:Focus = Focus.INDUSTRY) -> None:
        self.name: str = name
        self.race: Race = race
        self.focus: Focus = focus
        self.population: float = population
    
    def __str__(self) -> str:
        return f"Planet {self.name} focused on {self.focus}"
    
    def __repr__(self) -> str:
        return f"Planet('{self.name}', {repr(self.race)}, {self.population}, {self.focus})"

    @property
    def industry(self) -> float:
        industry_from_focus: float = self.race.industry * self.population if self.focus == Focus.INDUSTRY else 0.0
        industry: float = industry_from_focus
        return industry
    
    def update(self) -> None:
        self.population += self.race.population * self.population * .04