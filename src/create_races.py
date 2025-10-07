from src.race import Race
def create_races() -> list[Race]:
    races: list[Race] = []
    races.append(Race(
        "Human",
        influence=1.25
    ))
    races.append(Race(
        "snarho", 
        industry=1.25, 
        research=.75, 
        influence=1.5,
        population=.75,
        troops=1.25,
        tolerance=-1,
        stealth=-5,
        detection_range=10,
        pilots=1
        ))
    return races