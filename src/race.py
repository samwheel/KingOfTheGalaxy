from enum import IntEnum, StrEnum

class Xeno(IntEnum):
    PHOBIC = -1
    NONE = 0
    PHILIC = 1

class Metabolism(StrEnum):
    GASEOUS = "Gaseous Metabolism"
    LITHIC = "Lithic Metabolism"
    ORGANIC = "Organic Metabolism"
    PHOTOTROPHIC = "Phototropic Metabolism"
    ROBOTIC = "Robotic Metabolism"
    SELF_SUSTAINING = "Self-Sustaining Metabolism"

    def __repr__(self):
        return f"Metabolism.{self.name}"

class Race:
    def __init__(
        self,
        name: str,
        industry: float = 1.00,
        research: float = 1.00,
        influence: float = 1.0,
        stockpile_distribution: float = 0.02,
        population: float = 1.0,
        supply: int = 1,
        fuel: float = 0.0,
        troops: float = 1.0,
        shields: int = 0,
        defense: int = 0,
        stability: float = 0.0,
        tolerance: int = 0,
        stealth: int = 0,
        detection_range: int = 0,
        metabolism: Metabolism = Metabolism.ORGANIC,
        xeno: Xeno = Xeno.NONE,
        pilots: int = 0,
        likes: list = [],
        dislikes: list = []
    ) -> None:
        self.__name: str = name
        self.__industry: float = industry
        self.__research: float = research
        self.__influence: float = influence
        self.__stockpile_distribution: float = stockpile_distribution
        self.__population: float = population
        self.__supply: int = supply
        self.__fuel: float = fuel
        self.__troops: float = troops
        self.__shields: int = shields
        self.__defense: int = defense
        self.__stability: float = stability
        self.__tolerance: int = tolerance
        self.__stealth: float = stealth
        self.__detection_range: int = detection_range
        self.__metabolism: Metabolism = metabolism
        self.__xeno: Xeno = xeno
        self.__pilots: int = pilots
        self.__likes: list = likes
        self.__dislikes: list = dislikes

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return (
            f"Race('{self.name}', {self.industry}, {self.research}, "
            f"{self.influence}, {self.stockpile_distribution}, {self.population}, "
            f"{self.supply}, {self.fuel}, {self.troops}, {self.shields}, "
            f"{self.defense}, {self.stability}, {self.tolerance}, {self.stealth}, "
            f"{self.detection_range}, {repr(self.metabolism)}, {self.xeno}, "
            f"{self.pilots}, {self.likes}, {self.dislikes})"
        )

    @property
    def name(self) -> str:
        return self.__name

    @property
    def industry(self) -> float:
        return self.__industry

    @property
    def research(self) -> float:
        return self.__research

    @property
    def influence(self) -> float:
        return self.__influence

    @property
    def stockpile_distribution(self) -> float:
        return self.__stockpile_distribution

    @property
    def population(self) -> float:
        return self.__population

    @property
    def supply(self) -> int:
        return self.__supply

    @property
    def fuel(self) -> float:
        return self.__fuel

    @property
    def troops(self) -> float:
        return self.__troops

    @property
    def shields(self) -> int:
        return self.__shields

    @property
    def defense(self) -> int:
        return self.__defense

    @property
    def stability(self) -> float:
        return self.__stability

    @property
    def tolerance(self) -> int:
        return self.__tolerance

    @property
    def stealth(self) -> float:
        return self.__stealth

    @property
    def detection_range(self) -> int:
        return self.__detection_range

    @property
    def metabolism(self) -> Metabolism:
        return self.__metabolism

    @property
    def xeno(self) -> Xeno:
        return self.__xeno

    @property
    def pilots(self) -> int:
        return self.__pilots

    @property
    def likes(self) -> list:
        return self.__likes

    @property
    def dislikes(self) -> list:
        return self.__dislikes