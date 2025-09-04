from empire import Empire

def main() -> None:
    print("Welcome to KingOfTheGalaxy!")
    empire_name:str = input("What would you like to call your empire?: ")
    player_empire:Empire = Empire(empire_name)

    while True:
        command: list[str] = input("Enter a command: ").lower().strip().split()
        match command:
            case ["exit"]:
                print("Exiting...")
                print("Thank you for playing King Of The Galaxy.")
                break

            case ["empire", "name"]:
                print(player_empire.name)

            case _:
                print("Huh? I don't understand that command.")

if (__name__ == "__main__"):
    main()