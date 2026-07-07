from game import Game
from gui_app import GameGUI
from country_data_loader import CountryDataLoader

def main():
    try:
        data_loader = CountryDataLoader()
        countries, map_data = data_loader.load_countries_data()
    except ValueError as error:
        print(error)
        return

    game = Game()
    game.picked_country_name = ""
    game.monthly_advisor_expenses = 0
    gui = GameGUI(game, countries, map_data)
    gui.run()

if __name__ == "__main__":
    main()
