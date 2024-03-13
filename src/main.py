import pygame
import sys

from const import *
from game import Game

class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Normal Chess")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        
        self.game = Game()
    
    def mainloop(self):
        
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        
        while True:
            # show methods
            game.show_bg(screen)
            game.show_moves(screen)   
            game.show_pieces(screen)
            
            if dragger.dragging:
                dragger.update_blit(screen)
            
            for event in pygame.event.get():
                # quit application
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    # if clicked square has a piece ? 
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        board.calc_moves(piece, clicked_row, clicked_col)
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(piece)
                        # show methods
                        game.show_bg(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                    
                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # show method
                        game.show_bg(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)

                        dragger.update_blit(screen)
                
                # click release 
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragger.undrag_piece()
                    
            pygame.display.update()   
    
main = Main()
main.mainloop()
