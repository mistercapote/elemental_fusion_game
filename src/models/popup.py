import pygame
from constants import *
from models.button import PopUpButton
from models.card import Card

class PopUp:
    def __init__(self, fusion, game):
        self.fusion = fusion
        self.button = PopUpButton(game.screen, "OK", CENTER_X+150, CENTER_Y+120)

    def __eq__(self, other):
        if not isinstance(other, PopUp): return False
        return self.fusion == other.fusion
    
    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (CENTER_X-200, CENTER_Y-150, 400, 300))
        pygame.draw.rect(screen, WHITE, (CENTER_X-200, CENTER_Y-150, 400, 300), 5)
        write(screen,"Novo isótopo descoberto!",  FONT_LARGE, WHITE, (CENTER_X,CENTER_Y-100))
        #lembrar de variar a mensagem

        hover_card = None
        i  = -len(self.fusion.product) * (SQUARE_WIDTH+5) // 2
        for card in self.fusion.product:
            card = Card(card, CENTER_X+i, CENTER_Y-60)
            i += SQUARE_WIDTH+5
            if not hover_card:
                xm, ym = pygame.mouse.get_pos()
                if xm > card.xpos and xm < card.xpos + SQUARE_WIDTH and ym > card.ypos and ym < card.ypos + SQUARE_HEIGHT:
                    hover_card = card
                    continue
            card.draw_card(screen)
        if hover_card: hover_card.draw_card(screen, -10)
        
        write(screen, f"{self.fusion.get_energy()}", FONT_LARGE, WHITE, (CENTER_X,CENTER_Y+55))
        write(screen, "Mensagem sobre esta reação", FONT_LARGE, WHITE, (CENTER_X,CENTER_Y+75))
        self.button.draw(screen)

