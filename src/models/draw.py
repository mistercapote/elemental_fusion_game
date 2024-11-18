import pygame
from constants import *
from models.game import Game
from abc import ABC, abstractmethod

class Button(ABC):
    def __init__(self, screen, text, x, y, action=None):
        self.text = text
        self.xpos = x
        self.ypos = y
        self.hovered = False
        self.color = WHITE
        self.rect = self.rects(screen)
        self.action = action

    def draw(self, screen):
        if self.rect.collidepoint(pygame.mouse.get_pos()): self.hovered = True
        else: self.hovered = False
        self.rects(screen)

    def rects(self, screen):
        if self.hovered: surface = FONT_BUTTON_HOVER.render(self.text, True, GRAY)
        else: surface = FONT_BUTTON.render(self.text, True, WHITE)
        rect = surface.get_rect(center=(self.xpos,self.ypos))
        screen.blit(surface, rect)
        return rect
    
    @abstractmethod
    def check_click(self):
        pass

class OpeningButton(Button):
    def check_click(self, event, game, video_clip):
        if self.rect.collidepoint(event.pos):
            if self.action:
                game.stop_media(video_clip)
                resultado = self.action(game)
                video_clip = game.start_media()
                return resultado, video_clip
        return game, video_clip
    
class StartingButton(Button):
    def check_click(self, event, *parameters):
        if self.rect.collidepoint(event.pos):
            if self.action:
                resultado = self.action(*parameters)
                return resultado
        if len(parameters) == 1:
            return parameters[0]
        return parameters
    
class CleaningButton(Button):
    def check_click(self, event):
        if self.rect.collidepoint(event.pos):
            if self.action:
                self.action()
    
class BackingButton(Button):
    def check_click(self, event, running):
        if self.rect.collidepoint(event.pos):
            pygame.mixer.stop()
            pygame.mixer.music.stop()
            return not running
        return running

class PopUpButton(Button):
    def check_click(self, event, game):
        if self.rect.collidepoint(event.pos):
            game.popup.pop(0)
        return game
    
class Card:
    def __init__(self, entity, x, y):
        self.entity = entity
        self.xpos = x
        self.ypos = y

    def check_click():
        #Abrir janela com os isotopos
        pass

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

class Ball(ABC):
    def __init__(self, entity):
        self.entity = entity
        self.drag_center = None
        self.dragging = False
        self.xpos, self.ypos = self.position()

    def check_down(self): 
        mouse = pygame.mouse.get_pos()
        #Confere se a posicao do mouse está sobre a ball
        distance = ((mouse[0] - self.xpos) ** 2 + (mouse[1] - self.ypos) ** 2) ** 0.5
        if distance < self.radius:
            self.dragging = True 
            self.drag_center = [self.xpos, self.ypos]

    def check_up(self, nucleo): 
        self.dragging = False
        if self.drag_center:
            if self.drag_center[0] > CENTER_X:
                if nucleo.reacting_lenght() < 2:
                    nucleo.reacting_append(self)
                self.drag_center = None
            else:
                #é desfeito, efeito de encolher
                self.drag_center = None
                pass
        return nucleo
    
    def check_motion(self, event): 
        #Atualiza a ball arrastavel para a posicao do mouse
        if self.dragging:
            new_pos = list(event.pos)
            #Lógica para colidir com os limites da tela
            new_pos[0] = max(self.radius, min(new_pos[0], WIDTH_MAX - self.radius))
            new_pos[1] = max(self.radius, min(new_pos[1], HEIGHT_MAX - self.radius))
            self.drag_center = new_pos

    @staticmethod
    def turn_ball(entity):
        if isinstance(entity, Element): 
            return ElementBall(entity) 
        elif isinstance(entity, FundamentalParticle): 
            return ParticleBall(entity)

    @staticmethod
    def start_draw():
        ElementBall.start_draw()
        ParticleBall.start_draw()

    def draw_ball(self, screen):
        self.draw(screen, self.xpos, self.ypos)

    def draw_drag_ball(self, screen):
        self.draw(screen, self.drag_center[0], self.drag_center[1])

    @abstractmethod
    def draw(self, screen, x, y):
        pass

    @abstractmethod
    def position(self):
        pass


class ElementBall(Ball):

    @staticmethod
    def start_draw():
        ElementBall.www = WIDTH_MAX//20
        ElementBall.hhh = HEIGHT_MAX//3
        ElementBall.line_break = 0
        ElementBall.radius = 25
    
    def position(self):
        if ElementBall.line_break % 9 == 0:
            ElementBall.www = WIDTH_MAX//20
            ElementBall.hhh += HEIGHT_MAX//12
        else:
            ElementBall.www += WIDTH_MAX//20
        ElementBall.line_break +=1
        return ElementBall.www, ElementBall.hhh

    def draw(self, screen, x, y):
        pygame.draw.circle(screen, self.entity.color, (x, y), self.radius)
        
        mass_number_text = FONT_SMALL.render(f"{self.entity.mass_number}", True, BLACK)
        rect_mass_number_text = mass_number_text.get_rect(center=(x-self.radius//2, y-self.radius//3))
        screen.blit(mass_number_text, rect_mass_number_text)
        
        symbol_text = FONT_LARGE.render(self.entity.symbol, True, BLACK)
        rect_symbol_text = symbol_text.get_rect(center=(x,y))
        screen.blit(symbol_text, rect_symbol_text)

class ParticleBall(Ball):

    @staticmethod
    def start_draw():
        ParticleBall.www = WIDTH_MAX//20
        ParticleBall.hhh = HEIGHT_MAX//7
        ParticleBall.line_break = 0
        ParticleBall.radius = 15

    def position(self):
        if ParticleBall.line_break % 9 == 0:
            ParticleBall.www = WIDTH_MAX//20
            ParticleBall.hhh += HEIGHT_MAX//14
        else:
            ParticleBall.www += WIDTH_MAX//20
        ParticleBall.line_break +=1
        return ParticleBall.www, ParticleBall.hhh

    def draw(self, screen, x, y):
        pygame.draw.circle(screen, self.entity.color, (x, y), self.radius)
        symbol_text = FONT_SMALL.render(self.entity.symbol, True, BLACK)
        rect_symbol_text = symbol_text.get_rect(center=(x,y))
        screen.blit(symbol_text, rect_symbol_text)

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

    #Hover elements
        
        


        message_text = FONT_LARGE.render("O deuterio é...", True, WHITE)
        rect_message_text = message_text.get_rect(center=(CENTER_X,CENTER_Y+75))
        screen.blit(message_text, rect_message_text)

        self.button.draw(screen)

    