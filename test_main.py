import json
from country import Country
from game import Game
from battle import Battle

# These testing countries start with only 10 ducats after buying their armies.
# Low income makes loans and bankruptcy happen quickly.
def main():
    save_one = Game()
    while True:
        try:
            start_choice = int(input("1. New Game\n2. Load Game\nChoose: "))
        except ValueError:
            print("Input a whole number that is 1 or 2. ")
            continue
        if start_choice == 1:
            ottomans = Country("Ottomans", 3.8, "105%", 40000, {"mil": 4, "dip": 3, "admin": 5}, 710, 0)
            france = Country("France", 4.5, "105%", 32000, {"mil": 4, "dip": 4, "admin": 3}, 330, 0)
            countries = [ottomans, france]
            print(ottomans.to_dictionary())
            save_one.advisor_setup()
            save_one.run(countries, 100)
            break
        elif start_choice == 2:
            countries = []
            try:
                countries = save_one.load_game(False)
                if countries != False:
                    save_one.run(countries, 100)
            except FileNotFoundError:
                print("No save file was found")
                continue
            except json.JSONDecodeError:
                print("The save file contains an invalid JSON.")
                continue
            except KeyError as missing_key:
                print("The save file is missing required data:", missing_key)
                continue
            break
        print("You need to pick 1 or 2 as a whole number.")
if __name__ == "__main__":
    main()
