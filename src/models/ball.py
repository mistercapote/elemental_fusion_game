import pygame
from constants import *
from abc import ABC, abstractmethod

class Ball(ABC):
    def __init__(self, entity):
        self.entity = entity
        self.drag_center = None
        self.dragging = False
        self.xpos, self.ypos = self.position()

    def check_down(self): 
        xm, ym = pygame.mouse.get_pos()
        #Confere se a posicao do mouse está sobre a ball
        distance = ((xm - self.xpos) ** 2 + (ym - self.ypos) ** 2) ** 0.5
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
                #é desfeito
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
        write(screen, f"{self.entity.mass_number}", FONT_SMALL, BLACK, (x-self.radius//2, y-self.radius//3))
        write(screen, self.entity.symbol, FONT_LARGE, BLACK, (x,y))
    
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
        write(screen, self.entity.symbol, FONT_SMALL, BLACK, (x,y))

