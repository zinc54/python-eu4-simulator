import json
from country import Country
from game import Game
from battle import Battle

# These testing countries start with only 10 ducats after buying their armies.
# Low income makes loans and bankruptcy happen quickly.
def main():
    save1 = Game()
    while True:
        try:
            startChoice = int(input("1. New Game\n2. Load Game\nChoose: "))
        except ValueError:
            print("Input a whole number that is 1 or 2. ")
            continue
        if startChoice == 1:
            Ottomans = Country("Ottomans", 3.8, "105%", 40000, {"mil": 4, "dip": 3, "admin": 5}, 710, 0)
            France = Country("France", 4.5, "105%", 32000, {"mil": 4, "dip": 4, "admin": 3}, 330, 0)
            countries = [Ottomans, France]
            print(Ottomans.toDictionary())
            save1.advisorSetup()
            save1.run(countries, 100)
            break
        elif startChoice == 2:
            countries = []
            try:
                countries = save1.loadGame(False)
                if countries != False:
                    save1.run(countries, 100)
            except FileNotFoundError:
                print("No save file was found")
                continue
            except json.JSONDecodeError:
                print("The save file contains an invalid JSON.")
                continue
            except KeyError as missingKey:
                print("The save file is missing required data:", missingKey)
                continue
            break
        print("You need to pick 1 or 2 as a whole number.")
if __name__ == "__main__":
    main()
