from src.buildings import Buildable, Building
from src.observer import Observer
from src.ship import Ship

class BuildHandler(Observer):
    def __init__(self, empire) -> None:
        self.empire = empire
        self.__build_list: list[tuple[Buildable, float]] = []

    def build(self, building: Buildable):
        try:
            try:
                self.__build_list.index((building, 0))
            except ValueError:
                if isinstance(building, Building):
                    building.location.buildings.index(building)
                elif isinstance(building, Ship):
                    self.__build_list.append((building, 0))
        except ValueError:
            self.__build_list.append((building, 0))
            pass
        except AttributeError:
            pass
    
    @property
    def build_list(self) -> list[tuple[Buildable, float]]:
        return self.__build_list
    
    def observer_update(self) -> None:
        industry: float = float(self.empire.industry)
        for building, build_industry in self.__build_list:
            new_build_industry: float = 0
            if industry + build_industry > building.build_production and building.build_max_amount + build_industry > building.build_production:
                new_build_industry = building.build_production - build_industry
            elif industry > building.build_max_amount:
                new_build_industry = building.build_max_amount
            else:
                new_build_industry = industry
            
            industry -= new_build_industry
            build_index: int = self.build_list.index((building, build_industry))
            if new_build_industry + build_industry < building.build_production:
                self.__build_list[build_index] = (building, new_build_industry + build_industry)
            else:
                if isinstance(building, Ship):
                    self.empire.ships.append(building.clone())
                elif isinstance(building, Building):
                    building.location.buildings.append(building)
                self.__build_list.remove((building, build_industry))