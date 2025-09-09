from enum import StrEnum
from race import Race

class Focus(StrEnum):
    PRODUCTION = "production"
    RESEARCH = "research"
    GROWTH = "growth"
    DEFENSE = "defense"
    INFLUENCE = "influence"

class Planet:
    def __init__(self, name:str, race:Race, focus:Focus = Focus.PRODUCTION) -> None:
        self.name: str = name
        self.race: Race = race
        self.focus: Focus = focus
    
    def __repr__(self) -> str:
        return f"Planet('{self.name}', {self.focus})"
