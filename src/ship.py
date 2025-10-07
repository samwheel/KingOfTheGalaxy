from functools import reduce

from src.buildings import Buildable

class ShipPart:
    def __init__(self, speed_bonus: int, armor_bonus: int, shield_bonus: int, damage_bonus: int, fuel_bonus: int) -> None:
        self.speed_bonus = speed_bonus
        self.armor_bonus = armor_bonus
        self.shield_bonus = shield_bonus
        self.damage_bonus = damage_bonus
        self.fuel_bonus = fuel_bonus

class Ship(Buildable):
    def __init__(self, parts: list[ShipPart]) -> None:
        self.parts: list[ShipPart] = parts
    
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
        super().__init__(0, 0, 0, 50, 0)

class TitaniumArmor(ShipPart):
    def __init__(self) -> None:
        super().__init__(0, 500, 0, 0, 0)

class RetroRockets(ShipPart):
    def __init__(self) -> None:
        super().__init__(20, 0, 0, 0, 0)

class HydrogenFuel(ShipPart):
    def __init__(self) -> None:
        super().__init__(0, 0, 0, 0, 5)