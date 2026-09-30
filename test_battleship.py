"""Behavioral regression tests: python -m unittest -v."""
import contextlib
import io
import unittest
from unittest.mock import patch

from ai import AI
from board import Board, ShotResult
from game import Battleship


class BoardTests(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.place_ship([(0, 0), (0, 1)], 'Two')
        self.board.place_ship([(5, 5)], 'One')

    def test_every_cell_hit_or_miss(self):
        occupied = self.board.ships
        for r in range(Board.SIZE):
            for c in range(Board.SIZE):
                result = self.board.fire((r, c))
                self.assertEqual(result.status != 'miss', (r, c) in occupied)
        self.assertTrue(self.board.all_sunk())

    def test_individual_damage_and_complete_fleet(self):
        self.assertEqual(self.board.fire((0, 0)).status, 'hit')
        self.assertEqual(self.board.fleet[0].hits, {(0, 0)})
        self.assertFalse(self.board.fleet[1].hits)
        self.assertEqual(self.board.fire((0, 1)), ShotResult('sunk', 'Two'))
        self.assertFalse(self.board.all_sunk())
        self.assertEqual(self.board.fire((5, 5)), ShotResult('sunk', 'One'))
        self.assertTrue(self.board.all_sunk())

    def test_repeated_hit_and_miss_do_not_mutate_state(self):
        for pos in [(0, 0), (2, 2)]:
            self.board.fire(pos)
            previous = self.board.shots.copy()
            with self.assertRaisesRegex(ValueError, 'Already fired'):
                self.board.fire(pos)
            self.assertEqual(self.board.shots, previous)

    def test_invalid_coordinates_do_not_consume_shots(self):
        for pos in [(-1, 0), (6, 0), (0, 6), '1,1', (1,), [1, 1], (1.0, 2), (True, 2), None]:
            with self.subTest(pos=pos), self.assertRaises(ValueError):
                self.board.fire(pos)
        self.assertFalse(self.board.shots)

    def test_invalid_ship_placements_are_atomic(self):
        before = self.board.ships
        for cells in [[], [(6, 0)], [(0, 0)], [(1, 1), (2, 2)], [(1, 1), (1, 3)], [(2, 2), (2, 2)]]:
            with self.subTest(cells=cells), self.assertRaises(ValueError):
                self.board.place_ship(cells)
            self.assertEqual(self.board.ships, before)

    def test_no_placement_after_shooting(self):
        self.board.fire((3, 3))
        with self.assertRaises(ValueError):
            self.board.place_ship([(2, 2)])

    def test_empty_board_is_not_a_completed_game(self):
        self.assertFalse(Board().all_sunk())

    def test_board_operations_are_silent(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.board.fire((0, 0))
            self.board.fire((0, 1))
            self.board.fire((3, 3))
        self.assertEqual(output.getvalue(), '')


class AITests(unittest.TestCase):
    def test_no_repeats_and_exhaustion(self):
        ai = AI()
        choices = [ai.choose() for _ in range(36)]
        self.assertEqual(set(choices), {(r, c) for r in range(6) for c in range(6)})
        self.assertIsNone(ai.choose())
        self.assertIsNone(ai.choose())

    def test_hit_prioritizes_untried_neighbor(self):
        ai = AI()
        with patch('ai.random.choice', return_value=(2, 2)):
            pos = ai.choose()
        ai.observe(pos, ShotResult('hit'))
        with patch('ai.random.choice', side_effect=AssertionError('Must target neighbors')):
            next_pos = ai.choose()
        self.assertEqual(abs(next_pos[0] - 2) + abs(next_pos[1] - 2), 1)
        self.assertNotEqual(pos, next_pos)

    def test_corner_targets_and_stale_candidates(self):
        ai = AI(2)
        with patch('ai.random.choice', return_value=(0, 0)):
            pos = ai.choose()
        ai.observe(pos, ShotResult('hit'))
        self.assertEqual(set(ai.targets), {(1, 0), (0, 1)})
        ai.targets.append((0, 0))
        choices = [ai.choose() for _ in range(3)]
        self.assertEqual(set(choices), {(1, 0), (0, 1), (1, 1)})
        self.assertIsNone(ai.choose())

    def test_selection_and_feedback_are_silent(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            ai = AI()
            pos = ai.choose()
            ai.observe(pos, ShotResult('hit'))
            ai.choose()
        self.assertEqual(output.getvalue(), '')

    def test_sunk_clears_obsolete_targets(self):
        ai = AI()
        pos = ai.choose()
        ai.observe(pos, ShotResult('hit'))
        ai.observe(pos, ShotResult('sunk'))
        self.assertFalse(ai.targets)

    def test_size_validation(self):
        for size in [0, -1, True, 1.5]:
            with self.assertRaises(ValueError):
                AI(size)


class GameTests(unittest.TestCase):
    def play(self, game, commands):
        output = io.StringIO()
        with patch('builtins.input', side_effect=commands), contextlib.redirect_stdout(output):
            game.run()
        return output.getvalue()

    def test_player_coordinates_repeat_and_one_feedback_per_shot(self):
        game = Battleship()
        with patch('ai.random.choice', return_value=(0, 0)) as choose:
            output = self.play(game, ['3,3', '3,3', 'q'])
        self.assertEqual(game.enemy.shots, {(2, 2)})
        self.assertEqual(game.player.shots, {(0, 0)})
        self.assertEqual(choose.call_count, 1)
        self.assertEqual(output.count('You fired at 3,3: HIT!'), 1)
        self.assertEqual(output.count('AI fired at 1,1: MISS!'), 1)
        self.assertIn('Already fired there.', output)
        self.assertIn('Enemy ship cells remaining: 5', output)

    def test_ai_hit_uses_exact_chosen_coordinate(self):
        game = Battleship()
        with patch('ai.random.choice', return_value=(1, 1)):
            output = self.play(game, ['1,1', 'q'])
        self.assertIn('AI fired at 2,2: HIT!', output)
        self.assertEqual(game.player.fleet[0].hits, {(1, 1)})

    def test_invalid_input_and_quit_do_not_advance_turn(self):
        game = Battleship()
        with patch.object(game.ai, 'choose') as choose:
            output = self.play(game, ['', 'abc', '1', '1,2,3', '1.5,2', '0,1', '7,1', '1,-1', ' Q '])
        choose.assert_not_called()
        self.assertFalse(game.enemy.shots)
        self.assertIn('Goodbye.', output)
        self.assertNotIn('fired at', output)

    def test_player_win_stops_before_extra_ai_turn(self):
        game = Battleship()
        # Isolate victory flow from the random opponent.
        game.enemy = Board()
        game.enemy.place_ship([(5, 5)], 'Last ship')
        with patch.object(game.ai, 'choose') as choose:
            output = self.play(game, ['6,6'])
        choose.assert_not_called()
        self.assertEqual(output.count('SUNK!'), 1)
        self.assertIn('You win!', output)

    def test_ai_win_stops_game(self):
        game = Battleship()
        game.player = Board()
        game.player.place_ship([(0, 0)], 'Last ship')
        with patch('ai.random.choice', return_value=(0, 0)):
            output = self.play(game, ['1,1'])
        self.assertTrue(game.player.all_sunk())
        self.assertEqual(output.count('AI fired at 1,1: SUNK!'), 1)
        self.assertIn('AI wins!', output)

    def test_ai_exhaustion_is_graceful(self):
        game = Battleship()
        game.ai.tried = {(r, c) for r in range(6) for c in range(6)}
        output = self.play(game, ['1,1'])
        self.assertIn('AI has no remaining shots.', output)

    def test_eof_and_keyboard_interrupt_quit(self):
        for signal in [EOFError, KeyboardInterrupt]:
            output = self.play(Battleship(), [signal])
            self.assertIn('Goodbye.', output)


if __name__ == '__main__':
    unittest.main()
