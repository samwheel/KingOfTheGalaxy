from src.empire import Empire
from random import choice
from src.planet import Planet
from src.planet import Focus
from src.race import Race, Metabolism

def get_races() -> dict[str, Race]:
    races: dict[str, Race] = {}

    with open("src/races.dat") as race_file:
        for line in race_file:
            new_race: Race = eval(line)
            races[new_race.name.lower()] = new_race

    return races

def random_planet_name() -> str:
    name_list:list[str] = []
    with open("src/names.txt", "r") as names:
        name_list = [name.strip() for name in names.readlines()]
        return choice(name_list) + " " + "I" * choice(range(1, 3))

def main() -> None:
    print("Welcome to KingOfTheGalaxy!")
    empire_name:str = input("What would you like to call your empire?: ")
    emperor_name:str = input("What is your emperor's name?: ")
    player_empire:Empire = Empire(empire_name, emperor_name)

    race_list: dict[str, Race] = get_races()
    print("Race options:")
    for key in race_list:
        print(f"    {key}")
    starting_race:Race|None = None
    while starting_race == None:
        race_choice: str = input("Race?: ").lower().strip()
        try:
            starting_race = race_list[race_choice]
        except KeyError:
            print(f"Race option {race_choice} does not exist. Would you like to try again?")

    current_planet:Planet = Planet(random_planet_name(), starting_race, 1, 10)
    player_empire.planets.append(current_planet)
    player_empire.year_handler.add_observer(current_planet)

    while True:
        command: list[str] = input("Enter a command: ").lower().strip().split()
        match command:
            case ["exit"]:
                print("Exiting...")
                print("Thank you for playing King Of The Galaxy.")
                break

            case ["view", "planet"]:
                print(f"{current_planet.name} focused on {current_planet.focus}")

            case ["planet", "race"]:
                print(current_planet.race)
            
            case ["planet", "population"]:
                print(current_planet.population)
            
            case ["planet", "industry"]:
                print(current_planet.industry)

            case ["change", "planet", "focus", "to", focus]:
                current_planet.focus = Focus(focus)
                print(f"{current_planet.name} focus changed to {current_planet.focus}")

            case ["empire"]:
                print(player_empire)
            
            case ["empire", "industry"]:
                print(player_empire.industry)
            
            case ["current", "year"]:
                print(player_empire.year_handler.year)

            case ["next", "year"]:
                print("Advancing year:")
                player_empire.year_handler.next_year()
                print(f"Current year: {player_empire.year_handler.year}")

            case _:
                print("I don't understand that command.")

if (__name__ == "__main__"):
    main()