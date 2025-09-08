from src.empire import Empire
from random import choice
from src.planet import Planet
from src.planet import Focus

def random_planet_name() -> str:
    name_list:list[str] = []
    with open("names.txt", "r") as names:
        name_list = names.readlines()
        return choice(name_list)

def main() -> None:
    print("Welcome to KingOfTheGalaxy!")
    empire_name:str = input("What would you like to call your empire?: ")
    emperor_name:str = input("What is your emperor's name?:")
    player_empire:Empire = Empire(empire_name, emperor_name)
    current_planet:Planet = Planet("Sol I")

    while True:
        command: list[str] = input("Enter a command: ").lower().strip().split()
        match command:
            case ["exit"]:
                print("Exiting...")
                print("Thank you for playing King Of The Galaxy.")
                break

            case ["view", "planet"]:
                print(f"{current_planet.name} focused on {current_planet.focus}")

            case ["change", "planet", "focus", "to", focus]:
                current_planet.focus = Focus(focus)
                print(f"{current_planet.name} focus changed to {current_planet.focus}")

            case ["empire"]:
                print(player_empire)

            case _:
                print("I don't understand that command.")

if (__name__ == "__main__"):
    main()