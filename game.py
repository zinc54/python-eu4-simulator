from event_system import EventSystem

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

    def advance_month(self, countries):
        for country in countries:
            country.process_monthly_economy(self.monthly_advisor_expenses, self.picked_country_name)
        self.months_passed += 1
