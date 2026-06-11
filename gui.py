import tkinter as tk
from game import Game
from country import Country
class GameGUI:
    def __init__(self, game, countries):
        self.game = game
        self.countries = countries
        self.window = tk.Tk()
        self.window.title("Python EU4 Simulator")
        self.window.geometry("600x400")
        self.startFrame = tk.Frame(self.window)
        self.gameFrame = tk.Frame(self.window)

        self.newGameButton = tk.Button(
            self.startFrame,
            text="New Game",
            command=self.startNewGame
        )
        self.exitGameButton = tk.Button(
            self.startFrame,
            text="Exit game",
            command=self.exitGame
        )

        self.startFrame.pack()
        self.newGameButton.pack()
        self.exitGameButton.pack()
        
        self.titleLabel = tk.Label(
            self.gameFrame,
            text="Python EU4 Simulator"
        )
        self.titleLabel.pack()

        self.nextMonthButton = tk.Button(
            self.gameFrame,
            text="Next Month",
            command=self.nextMonth
        )
        self.nextMonthButton.pack()
        self.monthLabel = tk.Label(self.gameFrame, text="Month: 0")
        self.firstCountryDucats = tk.Label(self.gameFrame, text=f"{self.countries[0].name} has {self.countries[0].ducats}")
        self.secondCountryDucats = tk.Label(self.gameFrame, text=f"{self.countries[1].name} has {self.countries[1].ducats}")
        self.monthLabel.pack()
        self.firstCountryDucats.pack()
        self.secondCountryDucats.pack()
        self.firstCountryTroopsLabel = tk.Label(self.gameFrame, text = "")
        self.secondCountryTroopsLabel = tk.Label(self.gameFrame, text = "")
        self.firstCountryTroopsLabel.pack()
        self.secondCountryTroopsLabel.pack()
    def nextMonth(self):
        self.game.advanceMonth(self.countries)
        self.monthLabel.config(text=f"Month: {self.game.monthsPassed}")
        self.refreshDisplay()
    def refreshDisplay(self):
        self.firstCountryDucats.config(text=f"{self.countries[0].name} has {self.countries[0].ducats:.2f} ducats")
        self.secondCountryDucats.config(text=f"{self.countries[1].name} has {self.countries[1].ducats:.2f} ducats")
        self.firstCountryTroopsLabel.config(text=f"{self.countries[0].name} has {self.countries[0].troops} troops")
        self.secondCountryTroopsLabel.config(text=f"{self.countries[1].name} has {self.countries[1].troops} troops")
    def startNewGame(self):
        self.startFrame.pack_forget()
        self.gameFrame.pack()
    def exitGame(self):
        self.window.destroy()
    def run(self):
        self.window.mainloop()
if __name__ == "__main__":
    weakerCountry = Country(
        "WeakCountry",
        4.0,
        "100%",
        10000,
        {"mil": 3, "dip": 3, "admin": 3},
        200,
        0
    )
    strongerCountry = Country(
        "StrongCountry",
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