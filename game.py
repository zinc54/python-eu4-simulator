from event_system import EventSystem
from country import Country
from ai_controller import AIController, AIDecision
from battle import Battle
from game_event import GameEvent


class Game:
    def __init__(self):
        self.months_passed = 0
        self.ai_controller = AIController()
        self.event_log: list[GameEvent] = []
        self.event_sys = EventSystem()
        self.running = True
        self.monthly_advisor_expenses = 0
        self.advisor_costs = {
            0: 0,
            1: 1,
            2: 4,
            3: 9,
        }
        self.picked_country_name: str = ""
        self.province_ids: dict[str, list[int]] = {}
        self.name_ids: dict[str, int] = {}
    def run_ai_turns(self, countries: list[Country]) -> None:
        for country in countries:
            if country.name == self.picked_country_name:
                continue

            possible_targets = [
                possible_target
                for possible_target in countries
                if possible_target is not country
            ]
            decision, event_log = self.ai_controller.choose_action(country, possible_targets, self.months_passed)
            self.event_log.extend(event_log)
            self.execute_ai_decision(country, decision)

    def get_month_actions(self) -> list[str]:
        event_time = self.months_passed % 12 == 0
        recruitment_time = self.months_passed % 6 == 0
        month_actions = []
        if event_time and recruitment_time:
            month_actions.append("recruit")
            month_actions.append("event")
        elif event_time:
            month_actions.append("event")
        elif recruitment_time:
            month_actions.append("recruit")
        return month_actions

    def advance_month(self, countries):
        for country in countries:
            country_events = country.process_monthly_economy(
                self.monthly_advisor_expenses,
                self.picked_country_name,
                self.months_passed,
            )
            country.process_monthly_monarch_points()

            self.event_log.extend(country_events)
        self.run_ai_turns(countries)
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
    def player_attacks_ai(self, attacker, defender) -> dict:
        started_battle = Battle(attacker, defender)
        battle_result_info = started_battle.resolve_battle()

        battle_event = GameEvent(self.months_passed, battle_result_info["attacker"]["name"], f"{battle_result_info['attacker']['name']} has attacked {battle_result_info['defender']['name']}!", "battle")
        self.event_log.append(battle_event)

        return battle_result_info
    def recruit_troops(
        self,
        country: Country,
        requested_stacks: str,
    ) -> str:
        result = country.recruit_troops(requested_stacks)

        if result == "success":
            recruitment_event = GameEvent(
                month=self.months_passed,
                actor_name=country.name,
                message=f"{country.name} has recruited {requested_stacks} stacks of troops.",
                category="recruitment",
            )
            self.event_log.append(recruitment_event)

        return result
    def delete_country(self, country_name):
        pass
    def transfer_province(self, result):
        winner = result["winner"]
        loser = result["loser"]
        name_id = self.name_ids[loser]
        lost_province = None

        if len(self.province_ids[loser]) == 0:
            self.delete_country(loser)
            return lost_province, name_id, True
        lost_province = self.province_ids[loser].pop(0)
        self.province_ids[winner].append(lost_province)
        if len(self.province_ids[loser]) == 0:
            return lost_province, name_id, None
        return lost_province, name_id, False
