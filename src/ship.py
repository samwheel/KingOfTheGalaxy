from functools import reduce

from src.buildings import Buildable
from src.star import Star
from src.observer import Observer

class ShipPart:
    def __init__(self, speed_bonus: int, armor_bonus: int, shield_bonus: int, damage_bonus: int, fuel_bonus: int, cost: int, build_max_amount: int) -> None:
        self.speed_bonus: int = speed_bonus
        self.armor_bonus: int = armor_bonus
        self.shield_bonus: int = shield_bonus
        self.damage_bonus: int = damage_bonus
        self.fuel_bonus: int = fuel_bonus
        self.cost: int = cost
        self.build_max_amount: int = build_max_amount

class Ship(Buildable, Observer):
    def __init__(self, name: str, parts: list[ShipPart], location: Star | tuple[int, int] | None = None) -> None:
        super().__init__(location, name, reduce(lambda x, y: x + y, [part.cost for part in parts]), reduce(lambda x, y: max(x, y), [part.build_max_amount for part in parts]))
        self.parts: list[ShipPart] = parts
        self.current_fuel: int = self.fuel
        self.location: Star | tuple[int, int] | None = location
        self.destination: Star | tuple[int, int] | None = None
    
    def observer_update(self) -> None:
        if self.location != self.destination and self.destination != None:
            self.location = self.destination
    
    def clone(self) -> 'Ship':
        return Ship(self.name, self.parts.copy(), self.location)
    
    @property
    def speed(self) -> int:
        return reduce(lambda x, y: x + y, [part.speed_bonus for part in self.parts])
    
    @property
    def armor(self) -> int:
        return reduce(lambda x, y: x + y, [part.armor_bonus for part in self.parts])
    
    @property
    def shield(self) -> int:
        return reduce(lambda x, y: x + y, [part.shield_bonus for part in self.parts])
    
    @property
    def damage(self) -> int:
        return reduce(lambda x, y: x + y, [part.damage_bonus for part in self.parts])
    
    @property
    def fuel(self) -> int:
        return reduce(lambda x, y: x + y, [part.fuel_bonus for part in self.parts])
    
class Laser(ShipPart):
    def __init__(self) -> None:
        super().__init__(0, 0, 0, 50, 0, 50, 50)

class TitaniumArmor(ShipPart):
    def __init__(self) -> None:
        super().__init__(0, 500, 0, 0, 0, 100, 100)

class RetroRockets(ShipPart):
    def __init__(self) -> None:
        super().__init__(20, 0, 0, 0, 0, 75, 75)

class HydrogenFuel(ShipPart):
    def __init__(self) -> None:
        super().__init__(0, 0, 0, 0, 5, 25, 25)