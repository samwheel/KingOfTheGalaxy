from src.planet import Planet

class Empire:
    def __init__(self, name: str, color: str, planets: list[Planet] | None = None):
        self.name: str = name
        self.color: str = color.lower()
        self.planets: list[Planet] = planets if planets is not None else []
        self.production: dict[str, int] = {"population": 1, "GDP": 1, "research": 1, "defense": 1}

    def increase_population_production(self, amount: int):
        self.production["population"] += amount
    
    def increase_GDP_production(self, amount: int):
        self.production["GDP"] += amount
    
    def increase_research_production(self, amount: int):
        self.production["research"] += amount
    
    def increase_defense_production(self, amount: int):
        self.production["defense"] += amount

    def __str__(self) -> str:
        return self.name