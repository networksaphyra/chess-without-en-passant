from pathlib import Path
import pygame


class Configuration:
    def __init__(self):
        # File paths for various game assets
        self.paths = {
            'w_king': Path('../assets/w_king_1x.png'),
            'w_queen': Path('../assets/w_queen_1x.png'),
            'w_rook': Path('../assets/w_rook_1x.png'),
            'w_bishop': Path('../assets/w_bishop_1x.png'),
            'w_knight': Path('../assets/w_knight_1x.png'),
            'w_pawn': Path('../assets/w_pawn_1x.png'),

            'b_king': Path('../assets/b_king_1x.png'),
            'b_queen': Path('../assets/b_queen_1x.png'),
            'b_rook': Path('../assets/b_rook_1x.png'),
            'b_pawn': Path('../assets/b_pawn_1x.png'),
            'b_bishop': Path('../assets/b_bishop_1x.png'),
            'b_knight': Path('../assets/b_knight_1x.png'),

            'light_square': Path('../assets/square brown light_1x.png'),
            'dark_square': Path('../assets/square brown dark_1x.png'),

            'menu_bg': Path('../assets/menu_bg_1.jpeg'),
            'font': Path('../assets/GODOFWAR.TTF'),

            'capture': Path('../assets/capture.mp3'),
            'castle': Path('../assets/castle.mp3'),
            'check': Path('../assets/check.mp3'),
            'game': Path('../assets/game.mp3'),
            'move': Path('../assets/move.mp3'),
            'promote': Path('../assets/promote.mp3')
        }

        # Starting positions for each chess piece
        self.start_piece_pos = {
            'w_pawn': [(i, 6) for i in range(8)],
            'w_knight': [(1, 7), (6, 7)],
            'w_bishop': [(2, 7), (5, 7)],
            'w_rook': [(0, 7), (7, 7)],
            'w_queen': [(3, 7)],
            'w_king': [(4, 7)],

            'b_pawn': [(i, 1) for i in range(8)],
            'b_knight': [(1, 0), (6, 0)],
            'b_bishop': [(2, 0), (5, 0)],
            'b_rook': [(0, 0), (7, 0)],
            'b_queen': [(3, 0)],
            'b_king': [(4, 0)],
        }

        self.wait_time = 1  # Wait time between switching main menu and chessboard (in seconds)
        self.button_font_size = 48  # Font size for buttons
        self.result_font_size = 35  # Font size for displaying results

        self.square_size = 80  # Size of each chessboard square
        self.transparency = 164  # Transparency value for colors

        # Color definitions
        self.white = (255, 255, 255, self.transparency)  # White piece color
        self.red = (220, 20, 60, self.transparency)  # Red color for highlights
        self.blue = (65, 105, 225, self.transparency)  # Blue color for highlights
        self.check_color = (229, 57, 53, self.transparency)  # Color for indicating check

    def get_square_color_surface(self):
        """
        Returns a Pygame surface with the dimensions of a chessboard square.
        """
        return pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)

    def get_path(self, asset: str):
        """
        Returns the file path for a given asset name.

        Args:
            asset (str): Name of the asset.

        Returns:
            Path: File path for the asset.
        """
        return self.paths[asset]
