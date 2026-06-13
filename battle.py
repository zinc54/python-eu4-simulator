class Battle:
    def __init__(self, attacker, defender):
        self.attacker = attacker
        self.defender = defender
        self.attackerDamage = attacker.calculateDamage()
        self.defenderDamage = defender.calculateDamage()
        self.attackerWon = None
    def resolveBattle(self):
        if self.attackerDamage >= self.defenderDamage:
            print("The attacker has won the battle!")
            self.defender.morale -= 1
            self.attacker.morale -= 0.2
            self.defender.troops -= self.attackerDamage / 10
            self.attacker.troops -= self.defenderDamage / 30
            self.attackerWon = True
        else:
            print("The defender has won the battle!")
            self.attacker.morale -= 1.2
            self.defender.morale -= 0.1
            self.attacker.troops -= self.defenderDamage / 10
            self.defender.troops -= self.attackerDamage / 30
            self.attackerWon = False