import pygame
from constants import *
from models.button import PopUpButton
import math

class Card:
    def __init__(self, entity, x, y):
        self.entity = entity
        self.xpos = x
        self.ypos = y
        self.button = None
        if isinstance(entity, Element):
            self.isotopes = [obj for obj in ISOTOPES if (obj.atomic_number == entity.atomic_number)]
        else: self.isotopes = None

    def draw_card(self, screen, coef=1):
        coordenates = [(self.xpos+coef,self.ypos+coef), 
                       (self.xpos+SQUARE_WIDTH-coef, self.ypos+coef), 
                       (self.xpos+SQUARE_WIDTH-coef, self.ypos+SQUARE_HEIGHT-coef), 
                       (self.xpos+coef, self.ypos+SQUARE_HEIGHT-coef)]
        
        if not self.entity:
            name_text, symbol_text = "", "?"
            pygame.draw.polygon(screen, GRAY, coordenates) 
        else:
            name_text, symbol_text = self.entity.name, self.entity.symbol
            pygame.draw.polygon(screen, self.entity.color, coordenates) 
        
        if coef != 1: write(screen, name_text, FONT_SMALL, BLACK, (self.xpos+SQUARE_WIDTH//2, self.ypos+7*SQUARE_HEIGHT//8-coef))
        write(screen, symbol_text, FONT_LARGE, BLACK, (self.xpos+SQUARE_WIDTH//2, self.ypos+SQUARE_HEIGHT//2))
        
        if isinstance(self.entity, Element):
            write(screen, f"{self.entity.atomic_number}", FONT_SMALL, BLACK, (self.xpos+SQUARE_WIDTH//8+coef, self.ypos+SQUARE_HEIGHT//8+coef))
            if isinstance(self.entity, Isotope):
                write(screen, f"{self.entity.mass_number}", FONT_SMALL, BLACK, (self.xpos+7*SQUARE_WIDTH//8-coef, self.ypos+SQUARE_HEIGHT//8+coef))

    def draw_popup(self, game):
        iW = (SQUARE_WIDTH * min(12, len(self.isotopes)+2))
        iH = (SQUARE_HEIGHT * math.ceil(len(self.isotopes)/10 + 2))
        pygame.draw.rect(game.screen, BLACK, (CENTER_X-iW//2, CENTER_Y-iH//2, iW, iH))
        pygame.draw.rect(game.screen, WHITE, (CENTER_X-iW//2, CENTER_Y-iH//2, iW, iH), 5)
        write(game.screen, f"Isotopos do {self.isotopes[0].name}", FONT_LARGE, WHITE, (CENTER_X,CENTER_Y-(iH-SQUARE_HEIGHT)//2))
        
        www = CENTER_X-iW//2 + SQUARE_WIDTH
        hhh = CENTER_Y-iH//2 + SQUARE_HEIGHT

        hover_card = None
        contador = 0
        for isotope in self.isotopes:
            if isotope in game.isotopes_found: 
                card = Card(isotope, www, hhh)
            else: 
                card = Card(None, www, hhh)
            
            contador +=1
            if contador % 10 == 0: 
                www = CENTER_X-iW//2 + SQUARE_WIDTH
                hhh += SQUARE_HEIGHT
            else:
                www += SQUARE_WIDTH

            if not hover_card:
                xm, ym = pygame.mouse.get_pos()
                if xm > card.xpos and xm < card.xpos + SQUARE_WIDTH and ym > card.ypos and ym < card.ypos + SQUARE_HEIGHT:
                    hover_card = card
                    continue
            card.draw_card(game.screen)
        if hover_card: hover_card.draw_card(game.screen, -10)

        if not self.button:
            self.button = PopUpButton(game.screen, "OK", CENTER_X+iW//2-40, CENTER_Y+iH//2-30)
        self.button.draw(game.screen)

        
        

    