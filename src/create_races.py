from src.race import Race, Metabolism
from src.planet import planet_types

def create_races() -> list[Race]:
    races: list[Race] = [
        Race(
            "Human",
            planet_types[0],
            influence=1.25
        ),
        Race(
            "snarho", 
            prefered_planet="Inferno",
            industry=1.25, 
            research=.75, 
            influence=1.5,
            population=.75,
            troops=1.25,
            tolerance=-1,
            stealth=-5,
            detection_range=10,
            pilots=1
        ),
        Race(
            name = "skanonoki",
            prefered_planet = "Tundra",
            industry = .75,
            research = 1.5,
            influence = .75,
            stability = 5,
            tolerance = 1,
            metabolism = Metabolism.SELF_SUSTAINING
        )
    ]
    return races