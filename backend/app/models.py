from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Vessel:
    id: int
    name: str
    size: float
    type: str  # container, tanker, passenger
    draft: float
    eta: str   # e.g., "0830"
    etd: str   # e.g., "0910"

@dataclass
class Berth:
    location: str
    depth: float
    equipment: List[str]