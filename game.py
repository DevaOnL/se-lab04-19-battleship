"""Setup, input conversion and turn-level feedback for terminal Battleship."""
from board import Board
from ai import AI


class Battleship:
    def __init__(self):
        self.player = Board()
        self.enemy = Board()
        self.ai = AI(Board.SIZE)
        self._setup()

    def _setup(self):
        self.player.place_ship({(1, 1), (1, 2), (1, 3)}, "Cruiser")
        self.player.place_ship({(3, 0), (4, 0)}, "Destroyer")
        self.player.place_ship({(5, 5)}, "Patrol boat")
        self.enemy.place_ship({(2, 2), (2, 3), (2, 4)}, "Cruiser")
        self.enemy.place_ship({(4, 0), (4, 1)}, "Destroyer")
        self.enemy.place_ship({(0, 5)}, "Patrol boat")

    def show(self):
        print("\nFire at row,col (1-6); q to quit.")
        print("Enemy ship cells remaining:", len(self.enemy.ships - self.enemy.shots))
        print("Your ship cells remaining:", len(self.player.ships - self.player.shots))

    @staticmethod
    def feedback(who, pos, result):
        suffix = f" ({result.ship_name})" if result.status == "sunk" else ""
        print(f"{who} fired at {pos[0] + 1},{pos[1] + 1}: {result.status.upper()}!{suffix}")

    def run(self):
        print("Battleship — three ships per fleet (lengths 3, 2, 1).")
        while True:
            self.show()
            try:
                raw = input("> ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye.")
                return
            if raw == "q":
                print("Goodbye.")
                return
            try:
                r, c = map(int, raw.split(","))
                pos = (r - 1, c - 1)
            except ValueError:
                print("Use row,col, for example 2,3.")
                continue
            try:
                result = self.enemy.fire(pos)
            except ValueError as error:
                print(error)
                continue
            self.feedback("You", pos, result)
            if self.enemy.all_sunk():
                print("You sank the fleet. You win!")
                return

            ai_pos = self.ai.choose()
            if ai_pos is None:
                print("AI has no remaining shots. Game over.")
                return
            result = self.player.fire(ai_pos)
            self.ai.observe(ai_pos, result)
            self.feedback("AI", ai_pos, result)
            if self.player.all_sunk():
                print("AI sank your fleet. AI wins!")
                return
