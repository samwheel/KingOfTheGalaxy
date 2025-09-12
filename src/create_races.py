from race import Race
races: list[Race] = []
races.append(Race(
    "Human",
    influence=1.25
))

with open("races.dat", "w") as race_file:
    for race in races:
        race_file.write(repr(race))