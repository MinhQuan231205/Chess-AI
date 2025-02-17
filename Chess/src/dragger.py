import pygame
from const import *

class Dragger:

    def __init__(self):
        self.is_dragging = False
        self.piece = None
        self.mouse_x = 0
        self.mouse_y = 0
        self.initial_row = 0
        self.initial_col = 0

    def update_blit(self, surface):
        self.piece.set_texture(size = 128)
        texture = self.piece.texture
        img = pygame.image.load(texture)
        img_center = self.mouse_x, self.mouse_y
        self.piece.texture_rect = img.get_rect(center = img_center)
        surface.blit(img, self.piece.texture_rect)
    

    def update_mouse_pos(self, pos):
        self.mouse_x, self.mouse_y = pos 

    def save_initial_pos(self, pos):
        self.initial_col = pos[0] // SQSIZE
        self.initial_row = pos[1] // SQSIZE

    def drag_piece(self, piece):
        self.piece = piece
        self.is_dragging = True

    def undrag_piece(self):
        self.piece = None
        self.is_dragging = False