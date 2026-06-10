class Battle:
    def __init__(self, attacker, defender):
        self.attacker = attacker
        self.defender = defender
        self.attackerDamage = attacker.calculateDamage()
        self.defenderDamage = defender.calculateDamage()
        self.attackerWon = None
        if self.attackerDamage >= self.defenderDamage:
            print("The attacker has won the battle!")
            defender.morale -= 1
            attacker.morale -= 0.2
            defender.troops -= self.attackerDamage / 10
            attacker.troops -= self.defenderDamage / 30
            self.attackerWon = True
        else:
            print("The defender has won the battle!")
            attacker.morale -= 1.2
            defender.morale -= 0.1
            attacker.troops -= self.defenderDamage / 10
            defender.troops -= self.attackerDamage / 30
            self.attackerWon = False