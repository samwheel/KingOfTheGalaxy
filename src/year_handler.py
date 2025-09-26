from src.observer import Subject


class YearHandler(Subject):
    def __init__(self) -> None:
        super().__init__()
        self.__year:int = 0
    
    @property
    def year(self) -> int:
        return self.__year
    
    def next_year(self) -> None:
        self.__year += 1
        self.update_observers()