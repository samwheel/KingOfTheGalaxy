class Race:
    def __init__(self, name:str, production_bonus:float) -> None:
        self.__name: str = name
        self.__production_bonus:float = production_bonus

    def __str__(self) -> str:
        return self.name
        
    def __repr__(self) -> str:
        return f"Race('{self.name}', {self.production_bonus})"

    @property
    def name(self) -> str:
        return self.__name

    @property
    def production_bonus(self) -> float:
        return self.__production_bonus