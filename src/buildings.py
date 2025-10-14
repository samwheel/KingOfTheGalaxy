class Buildable:
    def __init__(self, location, name: str, build_production: int, build_max_amount: int) -> None:
        self.build_production: int = build_production
        self.build_max_amount: int = build_max_amount
        self.name: str = name
        self.location = location
    
    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

class Building(Buildable):

    def __init__(self, location, name: str = "", build_production: int = 0, build_max_amount: int = 0, production_bonus: float = 0) -> None:
        super().__init__(location, name, build_production, build_max_amount)
        self.__production_bonus: float = production_bonus
    
    @property
    def production_bonus(self) -> float:
        return self.__production_bonus
    
    def __eq__(self, value: object) -> bool:
        return self.__class__ == value.__class__

class IndustrialCenter(Building):
    def __init__(self, location) -> None:
        super().__init__(location, "Industrial Center", 100, 20, 0.05)

    @property
    def production_bonus(self) -> float:
        return super().production_bonus * self.location.population

def get_buildings_list() -> list[type[Building]]:
    return [IndustrialCenter]