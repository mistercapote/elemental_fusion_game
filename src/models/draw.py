import pygame
from constants import *
from models.button import PopUpButton

class Card:
    def __init__(self, entity, x, y):
        self.entity = entity
        self.xpos = x
        self.ypos = y

    def draw_card(self, screen, coef=1):
        coordenates = [(self.xpos+coef,self.ypos+coef), 
                       (self.xpos+SQUARE_WIDTH-coef, self.ypos+coef), 
                       (self.xpos+SQUARE_WIDTH-coef, self.ypos+SQUARE_HEIGHT-coef), 
                       (self.xpos+coef, self.ypos+SQUARE_HEIGHT-coef)]
        if not self.entity:
            name_text = FONT_SMALL.render("", True, BLACK)
            symbol_text = FONT_LARGE.render("?", True, BLACK)
            pygame.draw.polygon(screen, GRAY, coordenates) 
        else:
            name_text = FONT_SMALL.render(self.entity.name, True, BLACK)
            symbol_text = FONT_LARGE.render(self.entity.symbol, True, BLACK)
            pygame.draw.polygon(screen, self.entity.color, coordenates) 
        
        if coef != 1:
            name_rect_text = name_text.get_rect(center=(self.xpos+SQUARE_WIDTH//2, self.ypos+7*SQUARE_HEIGHT//8-coef))
            screen.blit(name_text, name_rect_text)
        
        symbol_rect_text = symbol_text.get_rect(center=(self.xpos+SQUARE_WIDTH//2, self.ypos+SQUARE_HEIGHT//2))
        screen.blit(symbol_text, symbol_rect_text)

        if isinstance(self.entity, Element):
            number_text = FONT_SMALL.render(f"{self.entity.atomic_number}", True, BLACK)
            number_rect_text = number_text.get_rect(center=(self.xpos+SQUARE_WIDTH//8+coef, self.ypos+SQUARE_HEIGHT//8+coef))
            screen.blit(number_text, number_rect_text)
            if isinstance(self.entity, Isotope):
                mass_text = FONT_SMALL.render(f"{self.entity.mass_number}", True, BLACK)
                mass_rect_text = mass_text.get_rect(center=(self.xpos+7*SQUARE_WIDTH//8-coef, self.ypos+SQUARE_HEIGHT//8+coef))
                screen.blit(mass_text, mass_rect_text)


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
        
        #Mensagem varia, 
        title_text = FONT_LARGE.render("Novo isótopo descoberto!", True, WHITE)
        rect_title_text = title_text.get_rect(center=(CENTER_X,CENTER_Y-100))
        screen.blit(title_text, rect_title_text)

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

        message_text = FONT_LARGE.render("O deuterio é...", True, WHITE)
        rect_message_text = message_text.get_rect(center=(CENTER_X,CENTER_Y+75))
        screen.blit(message_text, rect_message_text)

        self.button.draw(screen)


class PopIsotopes:
    def __init__(self, element):
        if element:
            self.isotopes = [obj for obj in ISOTOPES if (obj.atomic_number == element.atomic_number)]
        else:
            self.isotopes = None
        self.button = None

    def draw(self, screen):
        if self.isotopes:
            i  = len(self.isotopes) * SQUARE_WIDTH // 2
            h = len(self.isotopes) * SQUARE_HEIGHT // 20

            pygame.draw.rect(screen, BLACK, (CENTER_X-i-50, CENTER_Y-h-80, 2*i+100, 2*h+160))
            pygame.draw.rect(screen, WHITE, (CENTER_X-i-50, CENTER_Y-h-80, 2*i+100, 2*h+160), 5)
            
            #Mensagem varia, 
            title_text = FONT_LARGE.render(f"Isotopos do {self.isotopes[0].name}", True, WHITE)
            rect_title_text = title_text.get_rect(center=(CENTER_X,CENTER_Y-h//2-40))
            screen.blit(title_text, rect_title_text)
            
            hover_card = None
            for card in self.isotopes:
                card = Card(card, CENTER_X-i, CENTER_Y-h)
                i -= SQUARE_WIDTH
                if not hover_card:
                    xm, ym = pygame.mouse.get_pos()
                    if xm > card.xpos and xm < card.xpos + SQUARE_WIDTH and ym > card.ypos and ym < card.ypos + SQUARE_HEIGHT:
                        hover_card = card
                        continue
                card.draw_card(screen)
            if hover_card: hover_card.draw_card(screen, -10)

            if not self.button:
                self.button = PopUpButton(screen, "OK", CENTER_X-i, CENTER_Y+h+50)
            self.button.draw(screen)

        
        

    