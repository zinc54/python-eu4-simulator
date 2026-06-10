class Country:
    def __init__(self, name, morale, discipline, troops, technology, ducats, income, chargeUpfront=True):
        self.name = name
        self.morale = morale
        self.troops = troops
        self.technology = technology
        self.income = income
        self.loans = 0
        self.maxLoans = 10
        self.monthlyInterestPayments = 0
        if isinstance(discipline, str):
            number = discipline.replace("%", "")
            discipline = float(number) / 100
        self.discipline = discipline
        self.costUpfront = (troops / 1000) * 10
        self.monthlyExpenses = (troops / 1000) * 0.2
        self.ducats = ducats
        if chargeUpfront:
            self.ducats -= self.costUpfront
    def toDictionary(self):
        countryData = {
            "name": self.name,
            "morale": self.morale,
            "discipline": self.discipline,
            "troops": self.troops,
            "technology": self.technology,
            "ducats": self.ducats,
            "income": self.income,
            "monthlyInterestPayments": self.monthlyInterestPayments,
            "loans": self.loans
        }
        return countryData
    def calculateDamage(self):
        maxMorale = 5.0
        moralePercentage = self.morale / maxMorale
        levelsAboveBase = self.technology["mil"] - 3
        techDamageBuff = 1 + (levelsAboveBase * 0.25)
        damage = self.troops * self.discipline * moralePercentage * techDamageBuff
        return damage

    def processMonthlyEconomy(self, advisorCosts, pickedCountryName):
        self.advisorCosts = advisorCosts
        if self.name == pickedCountryName:
            self.ducats -= advisorCosts
        self.ducats -= self.monthlyExpenses
        self.ducats += self.income
        self.ducats -= self.monthlyInterestPayments
        while self.ducats < 0:
            print("You need to take a loan! Having more than 10 loans will bankrupt you and end the game!")
            self.loans += 1
            if self.loans > self.maxLoans:
                print("Game over! You are bankrupt!")
                raise SystemExit
            if self.troops >= 40000:
                self.ducats += 200
                print(f"You have taken a 200 ducat loan at 4 percent interest. Current amount of loans: {self.loans}")
                self.monthlyInterestPayments += (200 * 0.04) / 12
            elif self.troops >= 30000:
                self.ducats += 150
                print(f"You have taken a 150 ducat loan at 4 percent interest. Current amount of loans: {self.loans}")
                self.monthlyInterestPayments += (150 * 0.04) / 12
            elif self.troops >= 20000:
                self.ducats += 100
                print(f"You have taken a 100 ducat loan at 4 percent interest. Current amount of loans: {self.loans}")
                self.monthlyInterestPayments += (100 * 0.04) / 12
            else:
                self.ducats += 75
                print(f"You have taken a 75 ducat loan at 4 percent interest. Current amount of loans: {self.loans}")
                self.monthlyInterestPayments += (75 * 0.04) / 12
    def recruitTroops(self, requestedStacks):
        recruitUpfrontCost = requestedStacks * 10
        recruitMonthlyCost = requestedStacks * 0.2
        self.ducats -= recruitUpfrontCost
        self.monthlyExpenses += recruitMonthlyCost
        self.troops += 1000 * requestedStacks
        print(f"You have bought {requestedStacks} stacks of troops for an upfront cost of {recruitUpfrontCost:.2f} and an extra monthly cost of {recruitMonthlyCost:.2f}")

