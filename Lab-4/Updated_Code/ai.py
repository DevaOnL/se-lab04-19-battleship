"""Random search followed by adjacent targeting, with no board access or output."""
from collections import deque
import random

from board import valid_coordinate


class AI:
    def __init__(self, size=6):
        if type(size) is not int or size <= 0:
            raise ValueError("Board size must be a positive integer.")
        self.size = size
        self.tried = set()
        self.targets = deque()

    def choose(self):
        while self.targets:
            pos = self.targets.popleft()
            if pos not in self.tried:
                self.tried.add(pos)
                return pos
        options = [(r, c) for r in range(self.size) for c in range(self.size)
                   if (r, c) not in self.tried]
        if not options:
            return None
        pos = random.choice(options)
        self.tried.add(pos)
        return pos

    def observe(self, pos, result):
        """Learn only from the result of the actual shot selected by choose()."""
        if not valid_coordinate(pos, self.size) or pos not in self.tried:
            raise ValueError("Feedback must refer to a selected coordinate.")
        if result.status == "sunk":
            self.targets.clear()
        elif result.status == "hit":
            r, c = pos
            for neighbor in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if (valid_coordinate(neighbor, self.size)
                        and neighbor not in self.tried and neighbor not in self.targets):
                    self.targets.append(neighbor)
