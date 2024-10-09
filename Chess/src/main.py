import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move

class Main:

    def __init__(self):
        # khởi tạo bàn cờ
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        self.game = Game()

    # vòng lặp của game
    def mainloop(self):

        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        board = self.game.board

        while True:
            # show
            game.show_background(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if dragger.is_dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                # click 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse_pos(event.pos)
                    
                    clicked_row = dragger.mouse_y // SQSIZE
                    clicked_col = dragger.mouse_x // SQSIZE

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece

                        if piece.color == game.next_player:
                            board.calculate_moves(piece, clicked_row, clicked_col)
                            dragger.save_initial_pos(event.pos)
                            dragger.drag_piece(piece)
                            # show
                            game.show_background(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                
                # drag 
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    game.set_hover(motion_row, motion_col)

                    if dragger.is_dragging:
                        # update mouse position
                        dragger.update_mouse_pos(event.pos)
                        # show
                        game.show_background(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        # blit
                        dragger.update_blit(screen)
                # release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.is_dragging:
                        dragger.update_mouse_pos(event.pos)

                        release_row = dragger.mouse_y // SQSIZE
                        release_col = dragger.mouse_x // SQSIZE

                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(release_row, release_col)
                        move = Move(initial, final)

                        if board.valid_move(dragger.piece, move):
                            captured = board.squares[release_row][release_col].has_piece()
                            # move
                            board.move(dragger.piece, move)
                            # sound
                            game.play_sound(captured)
                            # show
                            game.show_background(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            # change turn
                            game.next_turn()

                    dragger.undrag_piece()
                # check nút bấm t để đồi màu nền 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        game.change_theme()
                # exit
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() 

            pygame.display.update()    

main = Main()
main.mainloop()