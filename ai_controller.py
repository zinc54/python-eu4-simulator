from country import Country
from dataclasses import dataclass
from game_event import GameEvent


@dataclass
class AIDecision:
    action: str
    target: Country | None = None
    recruit_stacks: int = 0


class AIController:
    def choose_action(
        self,
        ai_country: Country,
        possible_targets: list[Country],
        months_passed: int = 0,
    ) -> tuple[AIDecision, list[GameEvent]]:
        recruited_stacks = 3
        recruitment_cost = ai_country.calculate_recruitment_cost(recruited_stacks)
        self.event_log: list[GameEvent] = []
        if (ai_country.income > 10 or ai_country.ducats > 500) and (ai_country.ducats >= recruitment_cost) and (ai_country.troops < 10000):
            recruit_event = GameEvent(months_passed, ai_country.name, f"Month {months_passed}: {ai_country.name} has recruited {recruited_stacks} stacks of troops!", "recruitment")
            self.event_log.append(recruit_event)
            return AIDecision(action="recruit", recruit_stacks=recruited_stacks), self.event_log
        for country in possible_targets:
            if ai_country.troops > country.troops * 1.5:
                battle_event = GameEvent(months_passed, ai_country.name, f"Month {months_passed}: {ai_country.name} has attacked {country.name}!", "battle")
                self.event_log.append(battle_event)
                return AIDecision(action="attack", target=country), self.event_log
        return AIDecision(action="wait"), self.event_log
