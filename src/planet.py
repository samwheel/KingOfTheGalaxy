from enum import StrEnum

class Focus(StrEnum):
    PRODUCTION = "production"
    RESEARCH = "research"
    GROWTH = "growth"
    DEFENSE = "defense"
    INFLUENCE = "influence"

class Planet:
    def __init__(self, name:str, focus:Focus = Focus.PRODUCTION) -> None:
        self.name: str = name
        self.focus: Focus = focus
    
    def __repr__(self) -> str:
        return f"Planet({self.name}, {self.focus})"