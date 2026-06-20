import random
from typing import TypedDict

class EventConsequence(TypedDict):
    description: str
    effects: dict[str, int]

class EventSystem():
    def __init__(self):
        self.event_consequences: dict[str, EventConsequence] = {
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
    def show_random_event(self, country):

        printable_events = list(self.events.keys())
        selected_event = random.choice(printable_events)
        print(selected_event)
        options =  list(self.events[selected_event].values())
        for each_option in options:
            print(each_option)
        while True:
            try:
                print(f"Consequence of choice 1: {self.event_consequences[options[0]]['description']}.")
                print(f"Consequence of choice 2: {self.event_consequences[options[1]]['description']}.")
                player_choice = int(input(f"Press 1 for choice: {options[0]}  Press 2 for choice: {options[1]}"))

                if player_choice in [1,2]:
                    self.apply_event_choice(country, options[player_choice - 1])
                    break
                else:
                    print("Please choose 1 or 2, not any other number.")
                    continue
            except ValueError:
                print("Please only input a whole number that is 1 or 2.")
                continue
    def apply_event_choice(self, country, choice):
        effects = self.event_consequences[choice]["effects"]
        for stat, amount in effects.items():
            current_value = getattr(country, stat)
            setattr(country, stat, current_value + amount)
