from random import choice

def random_planet_name() -> str:
    name_list:list[str] = []
    with open("names.txt", "r") as names:
        name_list = names.readlines()
        return choice(name_list)

class Planet:
    def __init__(self, name:str = random_planet_name()) -> None:
        self.name: str = name