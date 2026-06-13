import tkinter as tk
from game import Game
from country import Country
from event_system import EventSystem
import random

class GameGUI:
    def __init__(self, game, countries):
        self.game = game
        self.eventSys = EventSystem()
        self.countries = countries
        self.window = tk.Tk()
        self.window.title("Python EU4 Simulator")
        self.window.geometry("600x400")
        self.createFrames()
        self.buildStartScreen()
        self.buildCountryScreen()
        self.buildGameScreen()
        self.buildAdvisorScreen()
        self.buildEventScreen()
        self.buildRecruitingScreen()
    def buildEventScreen(self):
        self.eventText = tk.Label(
            self.eventFrame,
            text=""
        )
        self.eventChoiceOne = tk.Button(
            self.eventFrame,
            text=""
        )
        self.eventChoiceTwo = tk.Button(
            self.eventFrame,
            text=""
        )
        self.eventText.pack()
        self.eventChoiceOne.pack()
        self.eventChoiceTwo.pack()
    def buildRecruitingScreen(self):
        self.recruitmentQuestion = tk.Label(self.recruitmentFrame, text="How many troops in thousands do you wanna recruit? Type in the box below.")
        self.recruitmentEntry = tk.Entry(self.recruitmentFrame)
        self.recruitmentButton = tk.Button(
            self.recruitmentFrame,
            text="Recruit Troops",
            command=self.showRecruitmentIfYes
        )
        self.recruitmentCancelButton = tk.Button(
            self.recruitmentFrame,
            text="Cancel",
            command=self.cancelRecruitment
        )
        self.recruitmentButton.pack()
        self.recruitmentCancelButton.pack()
    def buildCountryScreen(self):
        self.ottomansButton = tk.Button(
            self.countrySelectionFrame,
            text="Ottomans",
            command=lambda: self.selectCountry("Ottomans")
        )
        self.franceButton = tk.Button(
            self.countrySelectionFrame,
            text="France",
            command=lambda: self.selectCountry("France")
        )
        self.countryConfirmationLabel = tk.Label(self.countrySelectionFrame, text = "")
        self.ottomansButton.pack()
        self.franceButton.pack()
    def buildStartScreen(self):
        self.newGameButton = tk.Button(
            self.startFrame,
            text="New Game",
            command=self.startNewGame
        )
        self.loadGameButton = tk.Button(
            self.startFrame,
            text="Load Game",
            command=self.showLoadedGame
        )
        self.exitGameButton = tk.Button(
            self.startFrame,
            text="Exit game",
            command=self.exitGame
        )
        self.newGameButton.pack()
        self.loadGameButton.pack()
        self.exitGameButton.pack()
        self.startFrame.pack()       
    def createFrames(self):
        self.startFrame = tk.Frame(self.window)
        self.gameFrame = tk.Frame(self.window)
        self.countrySelectionFrame = tk.Frame(self.window)
        self.advisorSelectionFrame = tk.Frame(self.window)
        self.eventFrame = tk.Frame(self.window)
        self.recruitmentFrame = tk.Frame(self.window)
    def buildGameScreen(self):
        self.monthLabel = tk.Label(self.gameFrame, text="Month: 0")
        self.chosenCountryLabel = tk.Label(self.gameFrame, text = f"You are playing as {self.game.pickedCountryName}")
        self.firstCountryDucats = tk.Label(self.gameFrame, text=f"{self.countries[0].name} has {self.countries[0].ducats:.2f} ducats")
        self.secondCountryDucats = tk.Label(self.gameFrame, text=f"{self.countries[1].name} has {self.countries[1].ducats:.2f} ducats")
        self.firstCountryTroopsLabel = tk.Label(self.gameFrame, text = f"{self.countries[0].name} has {self.countries[0].troops} troops")
        self.secondCountryTroopsLabel = tk.Label(self.gameFrame, text = f"{self.countries[1].name} has {self.countries[1].troops} troops")
        self.titleLabel = tk.Label(
            self.gameFrame,
            text="Python EU4 Simulator"
        )
        self.nextMonthButton = tk.Button(
            self.gameFrame,
            text="Next Month",
            command=self.nextMonth
        )
        self.titleLabel.pack()
        self.monthLabel.pack()
        self.firstCountryDucats.pack()
        self.secondCountryDucats.pack()
        self.firstCountryTroopsLabel.pack()
        self.secondCountryTroopsLabel.pack()
        self.nextMonthButton.pack()
    def buildAdvisorScreen(self):
        self.totalAdvisorCost = 0
        self.milAdvisorLabel = tk.Label(self.advisorSelectionFrame, text = "Military Advisor:")
        self.dipAdvisorLabel = tk.Label(self.advisorSelectionFrame, text = "Diplomatic Advisor:")
        self.adminAdvisorLabel = tk.Label(self.advisorSelectionFrame, text = "Administrative Advisor:")
        self.continueButtonAdvisors = tk.Button(self.advisorSelectionFrame, text = "Continue.", command=self.showGameScreen)
        self.militaryAdvisorLevel = tk.IntVar(value=0)
        self.diplomaticAdvisorLevel = tk.IntVar(value=0)
        self.administrativeAdvisorLevel = tk.IntVar(value=0)
        self.militaryDropdown = tk.OptionMenu(
            self.advisorSelectionFrame,
            self.militaryAdvisorLevel,
            0, 1, 2, 3,
            command=self.updateAdvisorCost
        )
        self.diplomaticDropdown = tk.OptionMenu(
            self.advisorSelectionFrame,
            self.diplomaticAdvisorLevel,
            0, 1, 2, 3,
            command=self.updateAdvisorCost
        )
        self.administrativeDropdown = tk.OptionMenu(
            self.advisorSelectionFrame,
            self.administrativeAdvisorLevel,
            0, 1, 2, 3,
            command = self.updateAdvisorCost
        )
        self.advisorCostLabel = tk.Label(self.advisorSelectionFrame, text=f"Total monthly advisor cost: 0 ducats")
        self.milAdvisorLabel.grid(row=0, column = 0)
        self.militaryDropdown.grid(row=0, column=1)
        self.dipAdvisorLabel.grid(row=1, column = 0)
        self.diplomaticDropdown.grid(row=1, column=1)
        self.adminAdvisorLabel.grid(row=2, column=0)
        self.administrativeDropdown.grid(row=2, column=1)
        self.advisorCostLabel.grid(row=3, column=0)
        self.continueButtonAdvisors.grid(row=4, column=0)
    def showLoadedGame(self):
        loadedCountries = self.game.loadGame(False)
        if loadedCountries is False:
            return
        self.countries = loadedCountries

        self.startFrame.pack_forget()
        self.refreshDisplay()

        self.chosenCountryLabel.pack()
        self.gameFrame.pack()
    def nextMonth(self):
        self.game.advanceMonth(self.countries)
        self.refreshDisplay()
        if self.game.monthsPassed % 12 == 0:
            self.showEventScreen()
        elif self.game.monthsPassed % 6 == 0:
            self.showRecruitmentScreen()
    def showRecruitmentScreen(self):
        self.gameFrame.pack_forget()
        self.recruitmentFrame.pack()
    def showRecruitmentIfYes(self):
        self.recruitmentButton.pack_forget()
        self.recruitmentCancelButton.pack_forget()
        self.recruitmentQuestion.pack()
        self.recruitmentEntry.pack()
    def cancelRecruitment(self):
        self.recruitmentFrame.pack_forget()
        self.gameFrame.pack()
    def showEventScreen(self):
        selectedEventText = random.choice(list(self.eventSys.events.keys()))
        options = list(self.eventSys.events[selectedEventText].values())

        self.eventText.config(text=selectedEventText)
        self.eventChoiceOne.config(
            text=f"{options[0]} Consequence: {self.eventSys.eventConsequences[options[0]]['description']}",
            command=lambda: self.chooseEventOption(options[0])
        )
        self.eventChoiceTwo.config(
            text=f"{options[1]} Consequence: {self.eventSys.eventConsequences[options[1]]['description']}",
            command=lambda: self.chooseEventOption(options[1])
        )

        self.gameFrame.pack_forget()
        self.eventFrame.pack()
    def chooseEventOption(self, choice):
        for country in self.countries:
            if country.name == self.game.pickedCountryName:
                self.eventSys.applyEventChoice(country, choice)
                break
        self.eventFrame.pack_forget()
        self.refreshDisplay()
        self.gameFrame.pack()
    def refreshDisplay(self):
        self.monthLabel.config(text=f"Month: {self.game.monthsPassed}")
        self.chosenCountryLabel.config(
            text=f"You are playing as {self.game.pickedCountryName}"
        )
        self.firstCountryDucats.config(text=f"{self.countries[0].name} has {self.countries[0].ducats:.2f} ducats")
        self.secondCountryDucats.config(text=f"{self.countries[1].name} has {self.countries[1].ducats:.2f} ducats")
        self.firstCountryTroopsLabel.config(text=f"{self.countries[0].name} has {self.countries[0].troops} troops")
        self.secondCountryTroopsLabel.config(text=f"{self.countries[1].name} has {self.countries[1].troops} troops")
    def selectCountry(self, countryName):
        self.game.pickedCountryName = countryName
        self.countryConfirmationLabel.config(
            text=f"You have chosen {countryName}"
        )
        self.countryConfirmationLabel.pack()
        self.window.after(500, self.showAdvisorScreen)
    def showAdvisorScreen(self):
        self.countrySelectionFrame.pack_forget()
        self.advisorSelectionFrame.pack()
    def updateAdvisorCost(self, selectedLevel=None):
        militaryLevel = self.militaryAdvisorLevel.get()
        diplomaticLevel = self.diplomaticAdvisorLevel.get()
        administrativeLevel = self.administrativeAdvisorLevel.get()
        milAdvisorCost = self.game.advisorCosts[militaryLevel]
        dipAdvisorCost = self.game.advisorCosts[diplomaticLevel]
        adminAdvisorCost = self.game.advisorCosts[administrativeLevel]
        self.totalAdvisorCost = milAdvisorCost + dipAdvisorCost + adminAdvisorCost
        self.advisorCostLabel.config(text=f"The total advisor cost for your country is: {self.totalAdvisorCost}")
    def showGameScreen(self):
        self.game.monthlyAdvisorExpenses = self.totalAdvisorCost
        self.advisorSelectionFrame.pack_forget()
        self.chosenCountryLabel.config(
            text=f"You are playing as {self.game.pickedCountryName}"
        )
        self.chosenCountryLabel.pack()
        self.gameFrame.pack()
    def startNewGame(self):
        self.startFrame.pack_forget()
        self.countrySelectionFrame.pack()
    def exitGame(self):
        self.window.destroy()
    def run(self):
        self.window.mainloop()
if __name__ == "__main__":
    weakerCountry = Country(
        "France",
        4.0,
        "100%",
        10000,
        {"mil": 3, "dip": 3, "admin": 3},
        200,
        0
    )
    strongerCountry = Country(
        "Ottomans",
        5.0,
        "110%",
        40000,
        {"mil": 5, "dip": 3, "admin": 3},
        700,
        0           
    )
    countries = [weakerCountry, strongerCountry]
    testSave = Game()
    testSave.pickedCountryName = "StrongCountry"
    testSave.monthlyAdvisorExpenses = 0
    gui = GameGUI(testSave, countries)
    gui.run()
