from src.planet import Planet

class Empire:
    def __init__(self, name: str, color: str, planets: list[Planet] | None = None):
        self.name: str = name
        self.color: str = color.lower()
        self.planets: list[Planet] = planets if planets is not None else []
        self.production: dict[str, float] = {"population": 0.2, "GDP": 0.2, "research": 0.2, "defense": 0.2}

    def increase_population_production(self, amount: float):
        self.production["population"] += amount
    
    def increase_GDP_production(self, amount: float):
        self.production["GDP"] += amount
    
    def increase_research_production(self, amount: float):
        self.production["research"] += amount
    
    def increase_defense_production(self, amount: float):
        self.production["defense"] += amount

    def __str__(self) -> str:
        return self.name

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "color": self.color,
            "planets": [planet.name for planet in self.planets],
            "production": self.production
        }