"""Fleet state. All internal coordinates are zero-based (row, column) tuples."""
from dataclasses import dataclass, field
from typing import FrozenSet, Optional, Set, Tuple

Coordinate = Tuple[int, int]


def valid_coordinate(pos, size):
    return (isinstance(pos, tuple) and len(pos) == 2
            and all(type(value) is int and 0 <= value < size for value in pos))


@dataclass
class Ship:
    name: str
    cells: FrozenSet[Coordinate]
    hits: Set[Coordinate] = field(default_factory=set)

    @property
    def sunk(self):
        return self.cells <= self.hits


@dataclass(frozen=True)
class ShotResult:
    status: str  # "hit", "miss", or "sunk"
    ship_name: Optional[str] = None


class Board:
    SIZE = 6

    def __init__(self):
        self.fleet = []
        self.shots = set()

    @property
    def ships(self):
        """The occupied cells of all ships, retained for board inspection."""
        return set().union(*(ship.cells for ship in self.fleet))

    def place_ship(self, cells, name=None):
        cells = list(cells)
        if self.shots:
            raise ValueError("Cannot place ships after firing begins.")
        if not cells or any(not valid_coordinate(cell, self.SIZE) for cell in cells):
            raise ValueError("Ship cells must be valid board coordinates.")
        if len(set(cells)) != len(cells):
            raise ValueError("Ship cells must be distinct.")
        cells = frozenset(cells)
        rows = {r for r, _ in cells}
        cols = {c for _, c in cells}
        straight = len(rows) == 1 or len(cols) == 1
        contiguous = (max(rows) - min(rows) + 1) * (max(cols) - min(cols) + 1) == len(cells)
        if not straight or not contiguous:
            raise ValueError("Ships must occupy a straight, contiguous line.")
        if cells & self.ships:
            raise ValueError("Ships cannot overlap.")
        name = name or f"Ship {len(self.fleet) + 1}"
        if any(ship.name == name for ship in self.fleet):
            raise ValueError("Ship names must be unique.")
        self.fleet.append(Ship(name, cells))

    def fire(self, pos):
        """Apply one valid, previously untried shot without printing feedback."""
        if not valid_coordinate(pos, self.SIZE):
            raise ValueError("Outside board or invalid coordinate.")
        if pos in self.shots:
            raise ValueError("Already fired there.")
        self.shots.add(pos)
        for ship in self.fleet:
            if pos in ship.cells:
                ship.hits.add(pos)
                return ShotResult("sunk" if ship.sunk else "hit", ship.name)
        return ShotResult("miss")

    def all_sunk(self):
        return bool(self.fleet) and all(ship.sunk for ship in self.fleet)
