from src.star import Star
from src.technology import Technology

class Game:
    def __init__(self, starmap: list[Star], tech_tree: list[Technology]):
        self.starmap: list[Star] = starmap
        self.tech_tree: list[Technology] = tech_tree