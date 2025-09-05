from empire import Empire

def main() -> None:
    print("Welcome to KingOfTheGalaxy!")
    empire_name:str = input("What would you like to call your empire?: ")
    emperor_name:str = input("What is your emperor's name?:")
    player_empire:Empire = Empire(empire_name, emperor_name)

    while True:
        command: list[str] = input("Enter a command: ").lower().strip().split()
        match command:
            case ["exit"]:
                print("Exiting...")
                print("Thank you for playing King Of The Galaxy.")
                break

            case ["empire"]:
                print(player_empire)

            case _:
                print("I don't understand that command.")

if (__name__ == "__main__"):
    main()