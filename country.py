class Country:
    def __init__(self, name, morale, discipline, troops, technology, ducats, income, charge_upfront=True):
        self.name = name
        self.morale = morale
        self.troops = troops
        self.technology = technology
        self.income = income
        self.loans = 0
        self.max_loans = 10
        self.monthly_interest_payments = 0
        if isinstance(discipline, str):
            number = discipline.replace("%", "")
            discipline = float(number) / 100
        self.discipline = discipline
        self.cost_upfront = (troops / 1000) * 10
        self.monthly_expenses = (troops / 1000) * 0.2
        self.ducats = ducats
        if charge_upfront:
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
        damage = self.troops * self.discipline * morale_percentage * tech_damage_buff
        return damage

    def process_monthly_economy(self, advisor_costs, picked_country_name):
        self.advisor_costs = advisor_costs
        if self.name == picked_country_name:
            self.ducats -= advisor_costs
        self.ducats -= self.monthly_expenses
        self.ducats += self.income
        self.ducats -= self.monthly_interest_payments
        while self.ducats < 0:
            print("You need to take a loan! Having more than 10 loans will bankrupt you and end the game!")
            self.loans += 1
            if self.loans > self.max_loans:
                print("Game over! You are bankrupt!")
                raise SystemExit
            if self.troops >= 40000:
                self.ducats += 200
                print(f"You have taken a 200 ducat loan at 4 percent interest. Current amount of loans: {self.loans}")
                self.monthly_interest_payments += (200 * 0.04) / 12
            elif self.troops >= 30000:
                self.ducats += 150
                print(f"You have taken a 150 ducat loan at 4 percent interest. Current amount of loans: {self.loans}")
                self.monthly_interest_payments += (150 * 0.04) / 12
            elif self.troops >= 20000:
                self.ducats += 100
                print(f"You have taken a 100 ducat loan at 4 percent interest. Current amount of loans: {self.loans}")
                self.monthly_interest_payments += (100 * 0.04) / 12
            else:
                self.ducats += 75
                print(f"You have taken a 75 ducat loan at 4 percent interest. Current amount of loans: {self.loans}")
                self.monthly_interest_payments += (75 * 0.04) / 12
    def recruit_troops(self, requested_stacks):
        try:
            requested_stacks = int(requested_stacks)
        except ValueError:
            return "invalid_input"
        if requested_stacks * 10 > self.ducats:
            return "too_expensive"
        elif requested_stacks <= 0:
            return "invalid_amount"
        else:
            recruit_upfront_cost = requested_stacks * 10
            recruit_monthly_cost = requested_stacks * 0.2
            self.ducats -= recruit_upfront_cost
            self.monthly_expenses += recruit_monthly_cost
            self.troops += 1000 * requested_stacks
            print(f"You have bought {requested_stacks} stacks of troops for an upfront cost of {recruit_upfront_cost:.2f} and an extra monthly cost of {recruit_monthly_cost:.2f}")
            return "success"

