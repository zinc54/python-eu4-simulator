import time
import json
from country import Country
from event_system import EventSystem
import msvcrt

class Game:
    def __init__(self):
        self.months_passed = 0
        self.event_sys = EventSystem()
        self.running = True
        self.monthly_advisor_expenses = 0
        self.advisor_costs = {
            0: 0,
            1: 1,
            2: 4,
            3: 9
        }
    def save_game(self, countries, testing):
        country_data_list = []
        for country in countries:
            country_data_list.append(country.to_dictionary())
        game_data = {
            "playerCountry": self.picked_country_name,
            "monthlyAdvisorExpenses": self.monthly_advisor_expenses,
            "monthsPassed": self.months_passed,
            "countries": country_data_list
        }
        if testing == False:
            with open("save_game.json", "w") as save_file:
                json.dump(game_data, save_file, indent=4)
        elif testing == True:
            with open("test_save_game.json", "w") as save_file:
                json.dump(game_data, save_file, indent=4)
    def load_game(self, testing):
        countries = []
        try:
            if testing == False:
                with open("save_game.json", "r") as save_file:
                    loaded_data = json.load(save_file)
            elif testing == True:
                with open("test_save_game.json", "r") as save_file:
                    loaded_data = json.load(save_file)
            self.picked_country_name = loaded_data["playerCountry"]
            self.monthly_advisor_expenses = loaded_data["monthlyAdvisorExpenses"]
            self.months_passed = loaded_data["monthsPassed"]
            for country_data in loaded_data["countries"]:
                loaded_country = self.load_country(country_data)
                countries.append(loaded_country)
            print("You have loaded into a new save.")
            return countries
        except FileNotFoundError:
            print("No save file was found")
            return False
        except json.JSONDecodeError:
            print("The save file contains an invalid JSON.")
            return False
        except KeyError as missing_key:
            print("The save file is missing required data:", missing_key)
            return False
    def advance_month(self, countries):
        for country in countries:
            country.process_monthly_economy(self.monthly_advisor_expenses, self.picked_country_name)
        self.months_passed += 1
    def pause_menu(self, player_input, countries, testing):
        if player_input == 1:
            return None
        elif player_input == 2:
            self.save_game(countries, testing)
        elif player_input == 3:
            loadable_countries = self.load_game(testing)
            if loadable_countries != False:
                return loadable_countries
        elif player_input == 4:
            self.running = False
            print("Exiting game. Goodbye!")
            raise SystemExit
    def run(self, countries, max_months):
        last_month_time = time.monotonic()
        while self.months_passed < max_months:
            if time.monotonic() - last_month_time >= 0.05:
                last_month_time = time.monotonic()
                self.advance_month(countries)
                if msvcrt.kbhit():
                    key = msvcrt.getch()
                    if key == b"\x1b":
                        print("1. Continue")
                        print("2. Save Game")
                        print("3. Load Game")
                        print("4. Exit Game")
                        while True:
                            try:
                                player_input = int(input("Choose which option by entering a number 1 through 4: "))
                                if player_input in [1,2,3,4]:
                                    result = self.pause_menu(player_input, countries, False)
                                    if result is not None:
                                        countries = result
                                    break
                                else:
                                    print("Please only input a whole number 1 through 4: ")
                                    continue
                            except ValueError:
                                print("Please only input a number.")
                                continue
                if self.months_passed % 12 == 0:
                    for country in countries:
                        if country.name == self.picked_country_name:
                            self.event_sys.show_random_event(country)
                if self.months_passed % 6 == 0:
                    while True:
                        recruit_choice = input("Do you want to recruit more troops? yes/no: ")
                        if recruit_choice.lower() == "yes":
                            for country in countries:
                                if country.name == self.picked_country_name:
                                    while True:
                                        try:
                                            requested_stacks = int(input(f"How many stacks of troops do you wanna recruit. One stack is 1000 troops. You have {country.ducats:.2f} ducats."))
                                            if requested_stacks <= 0:
                                                print("You can't buy 0 or less stacks of troops. Please input a positive whole number.")
                                                continue
                                            else:
                                                if requested_stacks * 10 <= country.ducats:
                                                    country.recruit_troops(requested_stacks)
                                                    break
                                                else:
                                                    print(f"You don't have enough money to buy all these troops. You have {country.ducats:.2f} and each stack of troops cost 10 ducats upfront." )
                                                    continue
                                        except ValueError:
                                            print("Please only input a number.")
                                            continue
                            break
                        elif recruit_choice.lower() == "no":
                            break
                        print("You need to input yes or no. Please try again.")
    def load_country(self, country_data):
        loaded_country = Country(
            country_data["name"],
            country_data["morale"],
            country_data["discipline"],
            country_data["troops"],
            country_data["technology"],
            country_data["ducats"],
            country_data["income"],
            False
        )
        loaded_country.loans = country_data["loans"]
        loaded_country.monthly_interest_payments = country_data["monthlyInterestPayments"]
        return loaded_country
    def ask_advisor_level(self, advisor_type):
        while True:
            try:
                chosen_level = int(input(f"What level of {advisor_type} advisor? 1, 2 or 3?"))
                if chosen_level in [1,2,3]:
                    return chosen_level
                print("Pick 1, 2 or 3.")
            except ValueError:
                print("Pick a whole number that is either 1, 2 or 3 please.")
    def advisor_setup(self):
        self.advisors = {}
        while True:
            self.picked_country_name = input("Which country do you want to play as: ")
            if self.picked_country_name.lower() == "ottomans":
                self.picked_country_name = "Ottomans"
                break
            elif self.picked_country_name.lower() == "france":
                self.picked_country_name = "France"
                break
            print("Please type a valid country name that exists.")
        mil_advisor_level = self.ask_advisor_level("military")
        dip_advisor_level = self.ask_advisor_level("diplomatic")
        admin_advisor_level = self.ask_advisor_level("administrative")
        self.monthly_advisor_expenses += self.advisor_costs[mil_advisor_level]
        self.monthly_advisor_expenses += self.advisor_costs[dip_advisor_level]
        self.monthly_advisor_expenses += self.advisor_costs[admin_advisor_level]
