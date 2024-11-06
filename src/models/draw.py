import pygame
from constants import *

class Button:
    def __init__():
        pass
    pass

class Card:
    def __init__(self, element, x, y):
        self.element = element
        self.xpos = x
        self.ypos = y

    def draw_card(self, screen, coef=1):
        coordenates = [(self.xpos+coef,self.ypos+coef), 
                       (self.xpos+SQUARE_WIDTH-coef, self.ypos+coef), 
                       (self.xpos+SQUARE_WIDTH-coef, self.ypos+SQUARE_HEIGHT-coef), 
                       (self.xpos+coef, self.ypos+SQUARE_HEIGHT-coef)]
        if not self.element:
            name_text = FONT_SMALL.render("", True, (0,0,0))
            symbol_text = FONT_LARGE.render("?", True, (0,0,0))
            number_text = FONT_SMALL.render("", True, (0,0,0))
            pygame.draw.polygon(screen, (150,150,150), coordenates) 
        else:
            name_text = FONT_SMALL.render(self.element.name, True, (0,0,0))
            symbol_text = FONT_LARGE.render(self.element.symbol, True, (0,0,0))
            number_text = FONT_SMALL.render(f"{self.element.atomic_number}", True, (0,0,0))
            pygame.draw.polygon(screen, self.element.color, coordenates) 

        
        number_rect_text = number_text.get_rect(center=(self.xpos+SQUARE_WIDTH//8+coef, self.ypos+SQUARE_HEIGHT//8+coef))
        symbol_rect_text = symbol_text.get_rect(center=(self.xpos+SQUARE_WIDTH//2, self.ypos+SQUARE_HEIGHT//2))
        
        screen.blit(number_text, number_rect_text)
        screen.blit(symbol_text, symbol_rect_text)

        if coef != 1:
            name_rect_text = name_text.get_rect(center=(self.xpos+SQUARE_WIDTH//2, self.ypos+7*SQUARE_HEIGHT//8-coef))
            screen.blit(name_text, name_rect_text)
        



class Ball:
    def __init__():
        pass
    pass

