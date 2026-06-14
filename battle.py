class Battle:
    def __init__(self, attacker, defender):
        self.attacker = attacker
        self.defender = defender
        self.attacker_damage = attacker.calculate_damage()
        self.defender_damage = defender.calculate_damage()
        self.attacker_won = None
    def resolve_battle(self):
        if self.attacker_damage >= self.defender_damage:
            print("The attacker has won the battle!")
            self.defender.morale -= 1
            self.attacker.morale -= 0.2
            self.defender.troops -= self.attacker_damage / 10
            self.attacker.troops -= self.defender_damage / 30
            self.attacker_won = True
        else:
            print("The defender has won the battle!")
            self.attacker.morale -= 1.2
            self.defender.morale -= 0.1
            self.attacker.troops -= self.defender_damage / 10
            self.defender.troops -= self.attacker_damage / 30
            self.attacker_won = False
