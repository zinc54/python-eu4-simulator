class Battle:
    def __init__(self, attacker, defender):
        self.attacker = attacker
        self.defender = defender
        self.attacker_damage = attacker.calculate_damage()
        self.defender_damage = defender.calculate_damage()
        self.attacker_won = None
    def resolve_battle(self):
        attacker_troops_before = self.attacker.troops
        attacker_morale_before = self.attacker.morale
        defender_troops_before = self.defender.troops
        defender_morale_before = self.defender.morale
        if self.attacker_damage >= self.defender_damage:
            print("The attacker has won the battle!")
            self.defender.morale -= 1
            below_zero_defender = self.defender.morale <= 0
            if not below_zero_defender:
                self.attacker.morale -= 0.2
            self.defender.troops -= self.attacker_damage / 10
            self.attacker.troops -= self.defender_damage / 30
            if self.defender.troops < 0:
                self.defender.troops = 0
            if self.attacker.troops < 0:
                self.attacker.troops = 0
            if below_zero_defender:
                self.defender.morale = 0
            self.attacker_won = True
        else:
            print("The defender has won the battle!")
            self.attacker.morale -= 1.2
            below_zero_attacker = self.attacker.morale <= 0
            if not below_zero_attacker:
                self.defender.morale -= 0.1
            self.attacker.troops -= self.defender_damage / 10
            self.defender.troops -= self.attacker_damage / 30
            if self.defender.troops < 0:
                self.defender.troops = 0
            if self.attacker.troops < 0:
                self.attacker.troops = 0
            if below_zero_attacker:
                self.attacker.morale = 0
            self.attacker_won = False
        battle_result = {
            "winner": "unknown",
            "attacker": {
                "name": self.attacker.name,
                "before": {
                    "troops": attacker_troops_before,
                    "morale": attacker_morale_before,
                },
                "after": {
                    "troops": self.attacker.troops,
                    "morale": self.attacker.morale,
                },
            },
            "defender": {
                "name": self.defender.name,
                "before": {
                    "troops": defender_troops_before,
                    "morale": defender_morale_before,
                },
                "after": {
                    "troops": self.defender.troops,
                    "morale": self.defender.morale,
                },
            },
        }
        if self.attacker_won:
            battle_result["winner"] = self.attacker.name
        else:
            battle_result["winner"] = self.defender.name
        return battle_result
