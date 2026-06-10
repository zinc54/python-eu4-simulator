import time
import json
from country import Country
import random
from event_system import EventSystem

class Game:
    def __init__(self):
        self.monthsPassed = 0
        self.eventSys = EventSystem()
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
        print("We are now at month " + str(self.monthsPassed))
    def run(self, countries, maxMonths):
        last_month_time = time.monotonic()
        while self.monthsPassed < maxMonths:
            if time.monotonic() - last_month_time >= 0.05:
                last_month_time = time.monotonic()
                self.advanceMonth(countries)
                if self.monthsPassed % 24 == 0:
                    while True:
                        saveChoice = input("Do you want to save the game? yes/no: ")    
                        if saveChoice.lower() == "yes":
                            self.saveGame(countries, False)
                            break
                        elif saveChoice.lower() == "no":
                            break
                        print("Please type either yes or no.")
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
        self.advisorCosts = {1: 1, 2: 4, 3: 9}
        self.monthlyAdvisorExpenses = 0
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
