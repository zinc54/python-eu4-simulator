from dataclasses import dataclass

@dataclass
class Province:
    stable_id: str
    original_country: str
    current_owner: str
    row: int
    column: int