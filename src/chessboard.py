from chessConfiguration import Configuration
from piece import Piece
from audio import Audio
import pygame


class Chessboard:
    def __init__(self):
        self.config = Configuration()
        self.audio = Audio()

        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()
        self.turn = 'w'

    def setup_board(self):
        """
        Sets up the chessboard with the initial piece positions.
        """
        for piece_name, positions in self.config.start_piece_pos.items():
            for position in positions:
                piece = Piece(piece_name, position)
                x, y = position
                self.board[x][y] = piece

    def move_piece(self, piece: Piece, new_position: tuple[int, int]):
        """
        Moves a piece on the chessboard to a new position.

        Args:
            piece (Piece): The piece to be moved.
            new_position (tuple[int, int]): The new position (x, y) of the piece.
        """
        old_x, old_y = piece.position
        new_x, new_y = new_position

        self.board[old_x][old_y] = None
        self.board[new_x][new_y] = piece
        piece.position = new_position

    def get_square_at_pixel(self, pixel_pos: tuple[float, float]):
        """
        Returns the (x, y) coordinates of the chessboard square corresponding to the given pixel position.

        Args:
            pixel_pos (tuple[float, float]): The pixel position (x, y) on the screen.

        Returns:
            tuple[int, int]: The (x, y) coordinates of the chessboard square.
        """
        x = int(pixel_pos[0] // self.config.square_size)
        y = int(pixel_pos[1] // self.config.square_size)

        return x, y

    def highlight_check(self, screen: pygame.Surface, board, king: Piece):
        """
        Highlights the square of the king if it is in check.

        Args:
            screen (pygame.Surface): The surface on which to draw the highlight.
            board: The chessboard configuration.
            king (Piece): The king piece.

        """
        if king.is_in_check(board):
            king_x, king_y = king.position
            check_color_surface = self.config.get_square_color_surface()
            check_color_surface.fill(self.config.check_color)
            check_rect = pygame.Rect(
                king_x * self.config.square_size, king_y * self.config.square_size, self.config.square_size,
                self.config.square_size)
            screen.blit(check_color_surface, check_rect)
            pygame.display.update()

    def highlight_squares(self, screen: pygame.Surface, piece: Piece):
        """
        Highlights the possible move squares for the selected piece.

        Args:
            screen (pygame.Surface): The surface on which to draw the highlights.
            piece (Piece): The selected piece.
        """
        for pos in piece.possible_moves:
            x, y = pos
            color_surface = self.config.get_square_color_surface()
            color_surface.fill(self.config.red if self.board[x][y] is not None else self.config.blue)
            rect = pygame.Rect(x * self.config.square_size, y * self.config.square_size,
                               self.config.square_size, self.config.square_size)
            screen.blit(color_surface, rect)

        pygame.display.update()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

    def click_on_piece(self, screen: pygame.Surface):
        """
        Handles the user's click on a piece and triggers corresponding actions.

        Args:
            screen (pygame.Surface): The game screen.

        Returns:
            str or bool: The result of the game (win/lose/draw) or False if the game is ongoing.
        """
        while True:
            event = pygame.event.wait()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed_square = self.get_square_at_pixel(pygame.mouse.get_pos())
                x, y = pressed_square
                piece = self.board[x][y]

                if piece and piece.piece_name[0] == self.turn:
                    if piece.update_piece(screen, self):
                        self.turn = 'w' if self.turn == 'b' else 'b'
                        king = piece.get_piece(self.board, self.turn + '_king')

                        if king.is_in_check(self.board, False) and king.no_possible_legal_moves(self, self.turn):
                            return f'{"Black" if self.turn == "w" else "White"} Wins by Checkmate'

                        if king.no_possible_legal_moves(self, self.turn):
                            return 'Draw by Stalemate'
                        return False

    def display_board(self, screen: pygame.Surface):
        """
        Displays the chessboard on the screen.

        Args:
            screen (pygame.Surface): The game screen.
        """
        for x in range(8):
            for y in range(8):
                if (x + y) % 2 == 0:
                    image = pygame.image.load(self.config.get_path('light_square')).convert_alpha()
                else:
                    image = pygame.image.load(self.config.get_path('dark_square')).convert_alpha()
                screen.blit(image, (x * self.config.square_size, y * self.config.square_size))

                piece = self.board[x][y]
                if piece is not None:
                    screen.blit(piece.image, piece.rect)
