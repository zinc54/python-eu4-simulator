import time
import json
from country import Country
from event_system import EventSystem
import msvcrt

class Game:
    def __init__(self):
        self.monthsPassed = 0
        self.eventSys = EventSystem()
        self.running = True
        self.monthlyAdvisorExpenses = 0
        self.advisorCosts = {
            0: 0,
            1: 1,
            2: 4,
            3: 9
        }
    def saveGame(self, countries, testing):
        countryDataList = []
        for country in countries:
            countryDataList.append(country.toDictionary())
        gameData = {
            "playerCountry": self.pickedCountryName,
            "monthlyAdvisorExpenses": self.monthlyAdvisorExpenses,
            "monthsPassed": self.monthsPassed,
            "countries": countryDataList
        }
        if testing == False:
            with open("save_game.json", "w") as saveFile:
                json.dump(gameData, saveFile, indent=4)
        elif testing == True:
            with open("test_save_game.json", "w") as saveFile:
                json.dump(gameData, saveFile, indent=4)                    
    def loadGame(self, testing):
        countries = []
        try:
            if testing == False:
                with open("save_game.json", "r") as saveFile:
                    loadedData = json.load(saveFile)
            elif testing == True:
                with open("test_save_game.json", "r") as saveFile:
                    loadedData = json.load(saveFile)                
            self.pickedCountryName = loadedData["playerCountry"]
            self.monthlyAdvisorExpenses = loadedData["monthlyAdvisorExpenses"]
            self.monthsPassed = loadedData["monthsPassed"]
            for countryData in loadedData["countries"]:
                loadedCountry = self.loadCountry(countryData)
                countries.append(loadedCountry)
            return countries
        except FileNotFoundError:
            print("No save file was found")
            return False
        except json.JSONDecodeError:
            print("The save file contains an invalid JSON.")
            return False
        except KeyError as missingKey:
            print("The save file is missing required data:", missingKey)
            return False
    def advanceMonth(self, countries):
        for country in countries:
            country.processMonthlyEconomy(self.monthlyAdvisorExpenses, self.pickedCountryName)
            print(f"{country.name} has {country.ducats:.2f} ducats left!")
        self.monthsPassed += 1
    def pauseMenu(self, playerInput, countries, testing):
        if playerInput == 1:
            return None
        elif playerInput == 2:
            self.saveGame(countries, testing)
        elif playerInput == 3:
            loadAbleCountries = self.loadGame(testing)
            if loadAbleCountries != False:
                return loadAbleCountries
        elif playerInput == 4:
            self.running = False
            print("Exiting game. Goodbye!")
            raise SystemExit
    def run(self, countries, maxMonths):
        last_month_time = time.monotonic()
        while self.monthsPassed < maxMonths:
            if time.monotonic() - last_month_time >= 0.05:
                last_month_time = time.monotonic()
                self.advanceMonth(countries)
                if msvcrt.kbhit():
                    key = msvcrt.getch()
                    if key == b"\x1b":
                        print("1. Continue")
                        print("2. Save Game")
                        print("3. Load Game")
                        print("4. Exit Game")
                        while True:
                            try:
                                playerInput = int(input("Choose which option by entering a number 1 through 4: "))
                                if playerInput in [1,2,3,4]:
                                    result = self.pauseMenu(playerInput, countries, False)
                                    if result is not None:
                                        countries = result
                                    break
                                else:
                                    print("Please only input a whole number 1 through 4: ")
                                    continue
                            except ValueError:
                                print("Please only input a number.")
                                continue
                if self.monthsPassed % 12 == 0:
                    for country in countries:
                        if country.name == self.pickedCountryName:
                            self.eventSys.showRandomEvent(country) 
                if self.monthsPassed % 6 == 0:
                    while True:
                        recruitChoice = input("Do you want to recruit more troops? yes/no: ")
                        if recruitChoice.lower() == "yes":
                            for country in countries:
                                if country.name == self.pickedCountryName:
                                    while True:
                                        try:
                                            requestedStacks = int(input(f"How many stacks of troops do you wanna recruit. One stack is 1000 troops. You have {country.ducats:.2f} ducats."))
                                            if requestedStacks <= 0:
                                                print("You can't buy 0 or less stacks of troops. Please input a positive whole number.")
                                                continue
                                            else:
                                                if requestedStacks * 10 <= country.ducats:
                                                    country.recruitTroops(requestedStacks)
                                                    break
                                                else:
                                                    print(f"You don't have enough money to buy all these troops. You have {country.ducats:.2f} and each stack of troops cost 10 ducats upfront." )
                                                    continue
                                        except ValueError:
                                            print("Please only input a number.")
                                            continue
                            break
                        elif recruitChoice.lower() == "no":
                            break
                        print("You need to input yes or no. Please try again.")
    def loadCountry(self, countryData):
        loadedCountry = Country(
            countryData["name"],
            countryData["morale"],
            countryData["discipline"],
            countryData["troops"],
            countryData["technology"],
            countryData["ducats"],
            countryData["income"],
            False
        )
        loadedCountry.loans = countryData["loans"]
        loadedCountry.monthlyInterestPayments = countryData["monthlyInterestPayments"]
        print("You have now loaded into a new save!")
        return loadedCountry
    def askAdvisorLevel(self, advisorType):
        while True:
            try:
                chosenLevel = int(input(f"What level of {advisorType} advisor? 1, 2 or 3?"))
                if chosenLevel in [1,2,3]:
                    return chosenLevel
                print("Pick 1, 2 or 3.")
            except ValueError:
                print("Pick a whole number that is either 1, 2 or 3 please.")
    def advisorSetup(self):
        self.advisors = {}
        while True:
            self.pickedCountryName = input("Which country do you want to play as: ")
            if self.pickedCountryName.lower() == "ottomans":
                self.pickedCountryName = "Ottomans"
                break
            elif self.pickedCountryName.lower() == "france":
                self.pickedCountryName = "France"
                break
            print("Please type a valid country name that exists.")
        milAdvisorLevel = self.askAdvisorLevel("military")
        dipAdvisorLevel = self.askAdvisorLevel("diplomatic")
        adminAdvisorLevel = self.askAdvisorLevel("administrative")
        self.monthlyAdvisorExpenses += self.advisorCosts[milAdvisorLevel]
        self.monthlyAdvisorExpenses += self.advisorCosts[dipAdvisorLevel]
        self.monthlyAdvisorExpenses += self.advisorCosts[adminAdvisorLevel]
