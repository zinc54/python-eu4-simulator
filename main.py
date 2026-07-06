from country import Country
from game import Game
from gui_app import GameGUI

def main():
    weaker_country = Country(
        "France",
        4.0,
        "100%",
        10000,
        {"mil": 3, "dip": 3, "admin": 3},
        200,
        0
    )
    stronger_country = Country(
        "Ottomans",
        5.0,
        "110%",
        40000,
        {"mil": 5, "dip": 3, "admin": 3},
        700,
        0
    )
    countries = [weaker_country, stronger_country]

    game = Game()
    game.picked_country_name = ""
    game.monthly_advisor_expenses = 0
    gui = GameGUI(game, countries)
    gui.run()

if __name__ == "__main__":
    main()