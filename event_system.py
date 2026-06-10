import random

class EventSystem:
    def __init__(self):
        self.eventConsequences = {
                            "We are blessed!": {
                                "description": "Gain 100 ducats",
                                "effects": {
                                    "ducats": 100
                                }
                            },
                            "We need to invest long term!": {
                                "description": "Lose 50 ducats but gain 2 income",
                                "effects": {
                                    "ducats": -50,
                                    "income": 2
                                }
                            },
                            "Use the Military as Workforce": {
                                "description": "Lose 5000 troops",
                                "effects": {
                                    "troops": -5000
                                }
                            },
                            "Spend Money": {
                                "description": "Lose 100 ducats",
                                "effects": {
                                    "ducats": -100
                                }
                            },
                            "Stop Them!": {
                                "description": "Lose 150 ducats",
                                "effects": {
                                    "ducats": -150
                                }
                            },
                            "It is too expensive": {
                                "description": "Lose 1 ducat of income per month",
                                "effects": {
                                    "income": -1
                                }
                            }
                        }
        self.events = {
            "Our Embracing of Mercantilist policies is making it harder for other nations to compete with our merchants, meaning more profits for us.": {1: "Stop Them!", 2: "It is too expensive"},
            "This year's harvests have been exceptional! Rarely in our nation's history has the earth brought forth so much of its bounty. The populace are already interpreting this as a sign of divine favor for our rule.": {1: "We are blessed!", 2: "We need to invest long term!"},
            "People are finding lots of ways of getting around paying taxes and fees on moving goods, smuggling them past our authorities through a variety of clandestine channels. This is cutting into our income, but stopping it would cost quite a lot in the short-term.": {1: "Use the Military as Workforce", 2: "Spend Money"}
        }
    def showRandomEvent(self, country):

        printableEvents = list(self.events.keys())
        selectedEvent = random.choice(printableEvents)
        print(selectedEvent)
        options =  list(self.events[selectedEvent].values())
        for eachOption in options:
            print(eachOption)
        while True:
            try:
                print(f"Consequence of choice 1: {self.eventConsequences[options[0]]['description']}.")
                print(f"Consequence of choice 2: {self.eventConsequences[options[1]]['description']}.")
                playerChoice = int(input(f"Press 1 for choice: {options[0]}  Press 2 for choice: {options[1]}"))

                if playerChoice in [1,2]:
                    self.applyEventChoice(country, options[playerChoice - 1])
                    break
                else:
                    print("Please choose 1 or 2, not any other number.")
                    continue
            except ValueError:
                print("Please only input a whole number that is 1 or 2.")
                continue
    def applyEventChoice(self, country, choice):
        effects = self.eventConsequences[choice]["effects"]
        for stat, amount in effects.items():
            currentValue = getattr(country, stat)
            setattr(country, stat, currentValue + amount)
