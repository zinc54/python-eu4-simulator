from country import Country
from dataclasses import dataclass


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
    ) -> AIDecision:
        if (
            ai_country.income > 10 or ai_country.ducats > 500
        ) and ai_country.troops < 10000:
            return AIDecision(action="recruit", recruit_stacks=1)
        for country in possible_targets:
            if ai_country.troops > country.troops * 1.5:
                return AIDecision(action="attack", target=country)
        return AIDecision(action="wait")
