from dataclasses import dataclass
from typing import cast
from game_event import GameEvent


@dataclass
class Country:
    name: str
    morale: float
    discipline: float | str
    troops: int
    technology: dict[str, int]
    ducats: float
    income: float
    charge_upfront: bool = True
    loans: int = 0
    max_loans: int = 10
    monthly_interest_payments: float = 0

    def __post_init__(self):
        if isinstance(self.discipline, str):
            number = self.discipline.replace("%", "")
            self.discipline = float(number) / 100
        self.cost_upfront = (self.troops / 1000) * 10
        self.monthly_expenses = (self.troops / 1000) * 0.2
        if self.charge_upfront:
            self.ducats -= self.cost_upfront
    def to_dictionary(self):
        country_data = {
            "name": self.name,
            "morale": self.morale,
            "discipline": self.discipline,
            "troops": self.troops,
            "technology": self.technology,
            "ducats": self.ducats,
            "income": self.income,
            "monthlyInterestPayments": self.monthly_interest_payments,
            "loans": self.loans
        }
        return country_data
    def calculate_damage(self):
        max_morale = 5.0
        morale_percentage = self.morale / max_morale
        levels_above_base = self.technology["mil"] - 3
        tech_damage_buff = 1 + (levels_above_base * 0.25)
        discipline = cast(float, self.discipline)
        damage = self.troops * discipline  * morale_percentage * tech_damage_buff
        return damage
    def add_loan(self, loan_size: int, interest: float, months_passed: int) -> None:
        self.ducats += loan_size
        loan_event = GameEvent(
            month=months_passed,
            actor_name=self.name,
            message=f"{self.name} took a {loan_size}-ducat loan at {interest * 100}% annual interest.",
            category="loan",
        )
        self.event_log.append(loan_event)
        self.monthly_interest_payments += (loan_size * interest) / 12
    def process_monthly_economy(
        self,
        advisor_costs,
        picked_country_name,
        months_passed: int,
    ) -> list[GameEvent]:
        self.event_log: list[GameEvent] = []
        self.months_passed = months_passed
        self.advisor_costs = advisor_costs
        if self.name == picked_country_name:
            self.ducats -= advisor_costs
        self.ducats -= self.monthly_expenses
        self.ducats += self.income
        self.ducats -= self.monthly_interest_payments
        interest = 0.04
        while self.ducats < 0:
            print("You need to take a loan! Having more than 10 loans will bankrupt you and end the game!")
            self.loans += 1
            if self.loans > self.max_loans:
                print("Game over! You are bankrupt!")
                raise SystemExit
            if self.troops >= 40000:
                self.add_loan(200, interest, months_passed)
            elif self.troops >= 30000:
                self.add_loan(150, interest, months_passed)
            elif self.troops >= 20000:
                self.add_loan(100, interest, months_passed)
            else:
                self.add_loan(75, interest, months_passed)
        return self.event_log
    def calculate_recruitment_cost(self, requested_stacks: int) -> int:
        return requested_stacks * 10
    def recruit_troops(self, requested_stacks):
        try:
            requested_stacks = int(requested_stacks)
            recruit_upfront_cost = self.calculate_recruitment_cost(requested_stacks)
        except ValueError:
            return "invalid_input"
        if recruit_upfront_cost > self.ducats:
            return "too_expensive"
        elif requested_stacks <= 0:
            return "invalid_amount"
        else:
            recruit_monthly_cost = requested_stacks * 0.2
            self.ducats -= recruit_upfront_cost
            self.monthly_expenses += recruit_monthly_cost
            self.troops += 1000 * requested_stacks
            print(f"You have bought {requested_stacks} stacks of troops for an upfront cost of {recruit_upfront_cost:.2f} and an extra monthly cost of {recruit_monthly_cost:.2f}")
            return "success"

