from chessConfiguration import Configuration
from chessboard import Chessboard
from audio import Audio
from time import sleep
import pygame


class Main:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 640, 640
        self.FPS = 1
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        self.config = Configuration()
        self.chessboard = Chessboard()
        self.audio = Audio()
        self.game_started = False

        self.result = ''

        pygame.display.set_caption('Chess')

    def reset_game(self):
        """
        Resets the chessboard and game state.
        """
        self.chessboard = Chessboard()
        self.game_started = False

    def display_menu(self):
        """
        Displays the main menu screen.
        """
        background = self.config.get_path('menu_bg')
        background = pygame.transform.scale(pygame.image.load(background).convert_alpha(), (self.WIDTH, self.HEIGHT))
        self.screen.blit(background, (0, 0))

        font_path = self.config.get_path('font')
        button_font = pygame.freetype.Font(font_path, self.config.button_font_size)

        play_text, play_text_rect = button_font.render('Play', self.config.white)
        play_text_rect.center = (self.WIDTH // 2, self.HEIGHT // 2)

        quit_text, quit_text_rect = button_font.render('Quit', self.config.white)
        quit_text_rect.center = (self.WIDTH // 2, self.HEIGHT // 2 + 100)

        self.screen.blit(play_text, play_text_rect)
        self.screen.blit(quit_text, quit_text_rect)
        result_font = pygame.freetype.Font(font_path, self.config.result_font_size)

        if self.result:
            result_text, result_text_rect = result_font.render(self.result, self.config.white)
        else:
            result_text, result_text_rect = result_font.render('Chess, But Without En Passant', self.config.white)

        result_text_rect.midtop = (self.WIDTH // 2, self.HEIGHT // 4)
        self.screen.blit(result_text, result_text_rect)

        sleep(self.config.wait_time)
        pygame.display.update()

        while True:
            event = pygame.event.wait()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_text_rect.collidepoint(pygame.mouse.get_pos()):
                    self.reset_game()
                    return
                elif quit_text_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    exit(1)

    def update_display(self):
        """
        Updates the game display and handles events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(1)

        if not self.game_started:
            self.audio.play_game()
            self.display_menu()
            self.game_started = True

        self.chessboard.display_board(self.screen)
        pygame.display.flip()
        self.clock.tick(self.FPS)

        game_result = self.chessboard.click_on_piece(self.screen)
        if game_result:
            self.result = game_result
            self.chessboard.display_board(self.screen)
            pygame.display.update()
            self.game_started = False

    def start_game(self):
        """
        Starts the chess game loop.
        """
        while True:
            self.update_display()


if __name__ == '__main__':
    game = Main()
    game.start_game()
