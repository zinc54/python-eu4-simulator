from event_system import EventSystem
from country import Country
from ai_controller import AIDecision
from battle import Battle

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
        self.picked_country_name: str = ""
    def get_month_action(self):
        if self.months_passed % 12 == 0:
            return "event"
        elif self.months_passed % 6 == 0:
            return "recruitment"
        else:
            return "continue"
    def advance_month(self, countries):
        for country in countries:
            country.process_monthly_economy(self.monthly_advisor_expenses, self.picked_country_name)
        self.months_passed += 1
    def execute_ai_decision(
        self,
        ai_country: Country,
        decision: AIDecision,
    ) -> None:
        if decision.action == "recruit":
            ai_country.recruit_troops(decision.recruit_stacks)

        elif decision.action == "attack" and decision.target is not None:
            battle = Battle(ai_country, decision.target)
            battle.resolve_battle()
