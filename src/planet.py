planet_environments = ["Terran", "Ocean", "Swamp", "Toxic", "Volcanic", "Radiated", "Barren", "Tundra", "Desert", "Asteroid", "Gas Giant"]

class Planet:
    def __init__(self, name:str, environment: str = "Terran", population: float = 0):
        self.name: str = name
        self.population: float = population
        self.environment: str = environment.title()
        if self.environment not in planet_environments:
            raise ValueError(f"Invalid environment '{self.environment}' for planet '{self.name}'. Must be one of {planet_environments}.")
        self.statistics: dict[str, float] = {"population": 0, "GDP": 0, "research": 0, "defense": 0}

    def __str__(self) -> str:
        return self.name

    def to_dict(self):
        return {
            "name": self.name,
            "population": self.population,
            "environment": self.environment,
            "statistics": self.statistics
        }