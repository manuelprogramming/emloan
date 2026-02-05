from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Details:
    living_space: float
    year_built: Optional[int] = None
    year_renovated: Optional[int] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    street: Optional[str] = None
    street_number: Optional[str] = None
    floor: Optional[int] = None
    rooms: Optional[int] = None

    def to_dict(self) -> dict:
        return asdict(
            self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}
        )
