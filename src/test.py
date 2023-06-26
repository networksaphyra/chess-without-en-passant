from piece import Piece
from chessboard import Chessboard
import unittest
import pygame

class TestChess(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((100, 100))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_piece_get_piece(self):
        piece = Piece('w_rook', (3, 3))
        board = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, piece, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]
        ]

        result = piece.get_piece(board, 'w_rook')
        self.assertEqual(result, piece, "Test Failed: Incorrect piece returned.")
        result = piece.get_piece(board, 'b_rook')
        self.assertIsNone(result, "Test Failed: Non-existing piece should return None.")

    def test_piece_get_piece_at(self):
        piece = Piece('w_rook', (3, 3))
        board = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, piece, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]
        ]

        result = piece.get_piece_at(board, 3, 3)
        self.assertEqual(result, piece, "Test Failed: Incorrect piece returned.")
        result = piece.get_piece_at(board, 5, 5)
        self.assertIsNone(result, "Test Failed: Non-existing piece should return None.")

    def test_piece_enemy_piece_controls(self):
        piece = Piece('w_rook', (3, 5))
        enemy_piece = Piece('b_rook', (2, 2))

        board = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, enemy_piece, None, None, None, None, None],
            [None, None, None, piece, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]
        ]

        result = piece.enemy_piece_controls(board, 4, 3)
        self.assertFalse(result, "Test Failed: Expected enemy piece controls to be False.")

        result = piece.enemy_piece_controls(board, 2, 3)
        self.assertTrue(result, "Test Failed: Expected enemy piece controls to be True.")
    
    def test_get_diagonal_moves(self):
        piece = Piece('w_bishop', (3, 3))
        board = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, piece, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]
        ]

        expected_moves = {(2, 2), (1, 1), (0, 0), (4, 4), (5, 5), (6, 6), (7, 7), (2, 4), (1, 5), (0, 6), (4, 2), (5, 1), (6, 0)}
        result = piece.get_diagonal_moves(board, (3, 3))
        self.assertEqual(result, expected_moves, "Test Failed: Incorrect diagonal moves.")

    def test_get_linear_moves(self):
        piece = Piece('w_rook', (3, 3))
        board = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, piece, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]
        ]

        expected_moves = {(2, 3), (1, 3), (0, 3), (4, 3), (5, 3), (6, 3), (7, 3), (3, 2), (3, 1), (3, 0), (3, 4), (3, 5), (3, 6), (3, 7)}
        result = piece.get_linear_moves(board, (3, 3))
        self.assertEqual(result, expected_moves, "Test Failed: Incorrect linear moves.")

    def test_get_knight_moves(self):
        piece = Piece('w_knight', (3, 3))
        board = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, piece, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]
        ]

        expected_moves = {(1, 2), (2, 1), (2, 5), (1, 4), (5, 2), (4, 1), (4, 5), (5, 4)}
        result = piece.get_knight_moves(board, (3, 3))
        self.assertEqual(result, expected_moves, "Test Failed: Incorrect knight moves.")
    
    def test_get_pawn_moves(self):
        piece = Piece('w_pawn', (3, 3))
        board = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, piece, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]
        ]

        expected_moves = {(3, 2), (3, 1)}
        result = piece.get_pawn_moves(board, (3, 3))
        self.assertEqual(result, expected_moves, "Test Failed: Incorrect pawn moves.")

    def test_get_king_moves(self):
        piece = Piece('w_king', (4, 4))
        board = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, piece, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]
        ]

        expected_moves = {(3, 3), (3, 4), (3, 5), (4, 3), (4, 5), (5, 3), (5, 4), (5, 5)}
        result = piece.get_king_moves(board, (4, 4))
        self.assertEqual(result, expected_moves, "Test Failed: Incorrect king moves.")
    
    def test_get_possible_moves(self):
        piece = Piece('w_queen', (3, 3))
        board = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, piece, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]
        ]

        
        expected_moves = {(2, 3), (1, 3), (0, 3), (4, 3), (5, 3), (6, 3), (7, 3), (3, 2), (3, 1), (3, 0), (3, 4), (3, 5), (3, 6), (3, 7),
                          (2, 2), (1, 1), (0, 0), (4, 4), (5, 5), (6, 6), (7, 7), (2, 4), (1, 5), (0, 6), (4, 2), (5, 1), (6, 0)}
        
        result = piece.get_possible_moves(board)
        self.assertEqual(result, expected_moves, "Test Failed: Incorrect possible moves.")

    def test_is_in_check(self):
        piece = Piece('w_king', (4, 4))
        enemy_piece = Piece('b_queen', (2, 4))
        board = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, enemy_piece, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, piece, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]
        ]

        result = piece.is_in_check(board)
        self.assertEqual(result, True, "Test Failed: Incorrect check detection.")

    def test_no_possible_legal_moves(self):
        king = Piece('w_king', (0, 7))
        enemy_piece = Piece('b_queen', (1, 5))
        board = [
            [None, None, None, None, None, None, None, king],
            [None, None, None, None, None, enemy_piece, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]
        ]

        chessboard = Chessboard()
        chessboard.board = board
        result = king.no_possible_legal_moves(chessboard, 'w')
        self.assertEqual(result, True, "Test Failed: Incorrect checkmate detection.")

    def test_get_castling_moves(self):
        king = Piece('w_king', (4, 7))
        rook1 = Piece('w_rook', (1, 7))
        rook2 = Piece('w_rook', (7, 7))
        board = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, rook1, None, None, king, None, None, rook2]
        ]

        result = king.get_castling_moves(board)
        expected_moves = {(6, 7)}
        self.assertEqual(result, expected_moves, "Test Failed: Incorrect castling moves.")

if __name__ == "__main__":
    unittest.main() 