from chessConfiguration import Configuration
from audio import Audio
import pygame


class Piece:
    def __init__(self, piece_name: str, position: tuple[int, int]):
        """
        Initializes a chess piece with its name and position on the board.

        Args:
            piece_name (str): The name of the chess piece.
            position (tuple[int, int]): The position of the chess piece on the board.
        """
        self.config = Configuration()
        self.audio = Audio()
        self.piece_name = piece_name
        self.piece_path = self.config.get_path(self.piece_name)

        self.image = pygame.image.load(self.piece_path)
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.x, self.y = position
        self.rect = self.image.get_rect(center=((self.x + 0.5) * self.config.square_size, (self.y + 0.5) * self.config.square_size))

        self.on_starting_square = True
        self.position = position
        self.possible_moves = set()

    def get_piece(self, board, piece_name: str):
        """
        Returns the chess piece with the given name from the board.

        Args:
            board: The current chessboard.
            piece_name (str): The name of the chess piece to find.

        Returns:
            The chess piece with the given name if found, None otherwise.
        """
        for x in range(8):
            for y in range(8):
                if board[x][y] is not None and board[x][y].piece_name == piece_name:
                    return board[x][y]
        
        return None

    def get_piece_at(self, board, x: int, y: int):
        """
        Returns the chess piece at the given position on the board.

        Args:
            board: The current chessboard.
            x (int): The x-coordinate of the position.
            y (int): The y-coordinate of the position.

        Returns:
            The chess piece at the given position if present, None otherwise.
        """
        return board[x][y]
    
    def enemy_piece_controls(self, board, x: int, y: int):
        """
        Checks if there is an enemy piece that controls the given position on the board.

        Args:
            board: The current chessboard.
            x (int): The x-coordinate of the position.
            y (int): The y-coordinate of the position.

        Returns:
            True if there is an enemy piece controlling the position, False otherwise.
        """
        enemy_piece = 'b' if self.piece_name[0] == 'w' else 'w'

        for pos_x in range(8):
            for pos_y in range(8):
                if board[pos_x][pos_y] is not None and board[pos_x][pos_y].piece_name[0] == enemy_piece:
                    possible_moves = board[pos_x][pos_y].get_possible_moves(board)
                    if (x, y) in possible_moves:
                        return True
        return False

    def get_diagonal_moves(self, board, position: tuple[int, int]):
        """
        Calculates the possible diagonal moves for a given position on the chessboard.

        Args:
            board: The chessboard representation.
            position: The current position of the piece.

        Returns:
            A set of possible diagonal moves.

        """
        possible_moves = set()
        directions = [-1, 1]

        for x in directions:
            for y in directions:
                coord_x, coord_y = position
                while 0 <= coord_x + x <= 7 and 0 <= coord_y + y <= 7:
                    coord_x += x
                    coord_y += y
                    if board[coord_x][coord_y] is not None:
                        if board[coord_x][coord_y].piece_name[0] != self.piece_name[0]:
                            possible_moves.add((coord_x, coord_y))
                        break
                    possible_moves.add((coord_x, coord_y))

        return possible_moves

    def get_linear_moves(self, board, position: tuple[int, int]):
        """
        Calculates the possible linear (horizontal and vertical) moves for a given position on the chessboard.

        Args:
            board: The chessboard representation.
            position: The current position of the piece.

        Returns:
            A set of possible linear moves.

        """
        possible_moves = set()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for x, y in directions:
            coord_x, coord_y = position
            while 0 <= coord_x + x <= 7 and 0 <= coord_y + y <= 7:
                coord_x += x
                coord_y += y
                if board[coord_x][coord_y] is not None:
                    if board[coord_x][coord_y].piece_name[0] != self.piece_name[0]:
                        possible_moves.add((coord_x, coord_y))
                    break
                possible_moves.add((coord_x, coord_y))
        
        return possible_moves


    def get_knight_moves(self, board, position: tuple[int, int]):
        """
        Calculates the possible knight moves for a given position on the chessboard.

        Args:
            board: The chessboard representation.
            position: The current position of the piece.

        Returns:
            A set of possible knight moves.

        """
        possible_moves = set()
        directions = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
        pos_x, pos_y = position

        for x, y in directions:
            new_x = pos_x + x
            new_y = pos_y + y

            if 0 <= new_x <= 7 and 0 <= new_y <= 7:
                if board[new_x][new_y] is not None:
                    if board[new_x][new_y].piece_name[0] != self.piece_name[0]:
                        possible_moves.add((new_x, new_y))
                else:
                    possible_moves.add((new_x, new_y))

        return possible_moves

    def pawn_promotion(self, screen: pygame.Surface, board):
        """
        Handles pawn promotion when a pawn reaches the opposite end of the board.

        Args:
            screen: The Pygame surface for rendering.
            board: The chessboard representation.

        Returns:
            The newly promoted piece.

        """
        piece_color = self.piece_name[0] + '_'
        possible_pieces = ['queen', 'rook', 'bishop', 'knight']
        possible_pieces_rect = []
        x, y = self.position

        change_by = (1 if y == 0 else -1)

        for piece in possible_pieces:
            piece_image = pygame.image.load(self.config.get_path(piece_color + piece))
            piece_image = pygame.transform.scale(piece_image, (64, 64))

            piece_rect = piece_image.get_rect()
            piece_rect.center = ((x + 0.5) * self.config.square_size, (y + 0.5) * self.config.square_size)
            screen.blit(piece_image, piece_rect)
            possible_pieces_rect.append(piece_rect)

            y += change_by

        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(1)
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for i in range(4):
                        if possible_pieces_rect[i].collidepoint(mouse_pos):
                            new_x, new_y = self.position
                            new_piece = Piece(piece_color + possible_pieces[i], (new_x, new_y))
                            board[new_x][new_y] = new_piece
                            return
                    
    def get_pawn_moves(self, board, position: tuple[int, int]):
        """
        Calculates the possible moves for a pawn at a given position on the chessboard.

        Args:
            board: The chessboard representation.
            position: The current position of the pawn.

        Returns:
            A set of possible pawn moves.

        """
        possible_moves = set()
        directions = [1, 2] if self.piece_name[0] == 'b' else [-1, -2]
        x, y = position
        val = 1 if self.piece_name[0] == 'b' else -1

        if 0 < y < 7:
            if x < 7:
                if board[x + 1][y + val] is not None: 
                    if board[x + 1][y + val].piece_name[0] != self.piece_name[0]:
                        possible_moves.add((x + 1, y + val))            
            if x > 0:
                if board[x - 1][y + val] is not None:
                    if board[x - 1][y + val].piece_name[0] != self.piece_name[0]:
                        possible_moves.add((x - 1, y + val))

        for move_number in range(2 if self.on_starting_square else 1):
            if 0 <= y + directions[move_number] <= 7 and not board[x][y + directions[move_number]]:
                possible_moves.add((x, y + directions[move_number]))
            else:
                break

        return possible_moves


    def get_king_moves(self, board, position: tuple[int, int]):
        """
        Calculates the possible moves for a king at a given position on the chessboard.

        Args:
            board: The chessboard representation.
            position: The current position of the king.

        Returns:
            A set of possible king moves.

        """
        possible_moves = set()
        directions = [-1, 0, 1]
        pos_x, pos_y = position

        for x in directions:
            for y in directions:
                if x == y == 0:
                    continue
                if 0 <= pos_x + x <= 7 and 0 <= pos_y + y <= 7:
                    if not (board[pos_x + x][pos_y + y] is not None and board[pos_x + x][pos_y + y].piece_name[0] == self.piece_name[0]):
                        possible_moves.add((pos_x + x, pos_y + y))

        return possible_moves


    def get_possible_moves(self, board):
        """
        Calculates the possible moves for a piece on the chessboard.

        Args:
            board: The chessboard representation.

        Returns:
            A set of possible moves for the piece.

        """
        possible_moves = set()
        piece_name = self.piece_name.split('_')[-1]

        if piece_name == 'rook' or piece_name == 'queen':
            possible_moves |= self.get_linear_moves(board, self.position)        
        if piece_name == 'bishop' or piece_name == 'queen':
            possible_moves |= self.get_diagonal_moves(board, self.position)
        if piece_name == 'knight':
            possible_moves |= self.get_knight_moves(board, self.position)
        if piece_name == 'pawn':
            possible_moves |= self.get_pawn_moves(board, self.position)
        if piece_name == 'king':
            possible_moves |= self.get_king_moves(board, self.position)

        return possible_moves

    def is_in_check(self, board, experimental=True):
        """
        Checks if the piece is currently in check.

        Args:
            board (list): The current chessboard state.
            experimental (bool): Whether to play an audio cue when in check.

        Returns:
            bool: True if the piece is in check, False otherwise.
        """
        piece_color = self.piece_name[0]
        for x in range(8):
            for y in range(8):
                if board[x][y] is not None and board[x][y].piece_name[0] != piece_color:
                    piece_moves = board[x][y].get_possible_moves(board)
                    if self.position in piece_moves:
                        if not experimental:
                            self.audio.play_check()
                        return True
        return False

    def no_possible_legal_moves(self, chessboard, turn: str):
        """
        Checks if the current player has any legal moves.

        Args:
            chessboard (Chessboard): The chessboard object.
            turn (str): The current player's turn.

        Returns:
            bool: True if the current player has no legal moves, False otherwise.
        """
        for x in range(8):
            for y in range(8):
                piece = chessboard.board[x][y]
                if piece is not None and piece.piece_name[0] == turn:
                    possible_moves = piece.get_possible_moves(chessboard.board)
                    legal_moves = piece.get_legal_moves(chessboard, possible_moves)
                    if legal_moves:
                        return False
        return True


    def get_castling_moves(self, board):
        """
        Get the castling moves available for the king.

        Args:
            board (list): The current chessboard state.

        Returns:
            set: A set of castling moves (tuples) available for the king.
        """
        castling_moves = set()
        piece_color = self.piece_name[0]
        x1, x2, y = 0, 7, 0 if piece_color == 'b' else 7

        if not self.is_in_check(board):
            if self.on_starting_square and board[x1][y]:
                if board[x1][y].piece_name == piece_color + '_rook' and board[x1][y].on_starting_square:
                    if board[x1 + 1][y] is None and board[x1 + 2][y] is None and board[x1 + 3][y] is None and not self.enemy_piece_controls(board, x1 + 3, y) and not self.enemy_piece_controls(board, x1 + 2, y):
                        castling_moves.add((x1 + 2, y))
            if self.on_starting_square and board[x2][y]:
                if board[x2][y].piece_name == piece_color + '_rook' and board[x2][y].on_starting_square:
                    if board[x2 - 1][y] is None and board[x2 - 2][y] is None and not self.enemy_piece_controls(board, x2 - 2, y):
                        castling_moves.add((x2 - 1, y))

        return castling_moves


    def castle(self, chessboard_instance, rook):
        """
        Perform castling move for the king and rook.

        Args:
            chessboard_instance (Chessboard): The chessboard object.
            rook (Piece): The rook piece involved in castling.
        """
        rook_x, rook_y = rook.position

        king_pos_x = rook_x - 1 if rook_x == 7 else rook_x + 2 
        rook_pos_x = 3 if king_pos_x == 2 else 5

        chessboard_instance.move_piece(self, (king_pos_x, rook_y))
        chessboard_instance.move_piece(rook, (rook_pos_x, rook_y))

        self.rect.center = ((king_pos_x + 0.5) * self.config.square_size, (rook_y + 0.5) * self.config.square_size)
        rook.rect.center = ((rook_pos_x + 0.5) * self.config.square_size, (rook_y + 0.5) * self.config.square_size)
        rook.on_starting_square = False

        self.audio.play_castle()

    def get_legal_moves(self, chessboard_instance, possible_moves: set):
        """
        Get the legal moves for the piece.

        Args:
            chessboard_instance (Chessboard): The chessboard object.
            possible_moves (set): The set of possible moves for the piece.

        Returns:
            set: The set of legal moves for the piece.
        """
        current_position = self.position
        legal_moves = possible_moves
        piece_color = self.piece_name[0]
        moves_to_remove = set()

        for move in possible_moves:
            x, y = move
            piece_on_square = chessboard_instance.board[x][y]
            chessboard_instance.move_piece(self, move)
            king = self.get_piece(chessboard_instance.board, piece_color + '_king')
            if king.is_in_check(chessboard_instance.board):
                moves_to_remove.add(move)

            chessboard_instance.move_piece(self, current_position)
            if piece_on_square is not None:
                chessboard_instance.move_piece(piece_on_square, piece_on_square.position)

        legal_moves -= moves_to_remove
        return legal_moves


    def update_piece(self, screen: pygame.Surface, chessboard_instance):
        """
        Update the piece's position and handle game events.

        Args:
            screen (pygame.Surface): The game screen surface.
            chessboard_instance (Chessboard): The chessboard object.
        """
        while True:
            piece_name = self.piece_name.split('_')[-1]
            piece_color = self.piece_name[0]

            if piece_name == 'king':
                castling_moves = self.get_castling_moves(chessboard_instance.board)
                possible_moves = self.get_possible_moves(chessboard_instance.board) | castling_moves
            else:
                possible_moves = self.get_possible_moves(chessboard_instance.board)

            self.possible_moves = self.get_legal_moves(chessboard_instance, possible_moves)

            king = self.get_piece(chessboard_instance.board, piece_color + '_king')
            chessboard_instance.highlight_check(screen, chessboard_instance.board, king)
            chessboard_instance.highlight_squares(screen, self)

            castled = False
            promoted = False
            pressed_square = chessboard_instance.get_square_at_pixel(pygame.mouse.get_pos())
            x, y = pressed_square

            if chessboard_instance.board[x][y] is not None:
                piece_on_square = True
            else:
                piece_on_square = False

            if pressed_square in self.possible_moves:
                if piece_name == 'king' and pressed_square in castling_moves:
                    x, y = 0 if pressed_square[0] == 2 else 7, self.position[1]
                    rook = self.get_piece_at(chessboard_instance.board, x, y)
                    self.castle(chessboard_instance, rook)
                    castled = True
                else:
                    x, y = pressed_square
                    chessboard_instance.move_piece(self, pressed_square)

                    if piece_name == 'pawn' and (self.position[1] == 7 or self.position[1] == 0):
                        chessboard_instance.display_board(screen)
                        self.pawn_promotion(screen, chessboard_instance.board)
                        promoted = True
                    else:
                        self.rect.center = ((x + 0.5) * self.config.square_size, (y + 0.5) * self.config.square_size)

                if promoted:
                    self.audio.play_promote()
                elif castled:
                    self.audio.play_castle()
                elif piece_on_square:
                    self.audio.play_capture()
                else:
                    self.audio.play_move()

                self.on_starting_square = False
                return True

            else:
                chessboard_instance.display_board(screen)
                pygame.display.update()
                return False
    