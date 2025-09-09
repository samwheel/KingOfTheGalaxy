from race import Race
races: list[Race] = []
races.append(Race("Human", 1.00))

with open("races.dat", "w") as race_file:
    for race in races:
        race_file.write(repr(race))