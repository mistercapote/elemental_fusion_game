import pygame
from constants import *

class Element:
    def __init__(self, name, symbol, atomic_number, group, period, atomic_radius, color, description):
        self.name = name
        self.symbol = symbol
        self.atomic_number = atomic_number
        self.group = group # 1 a 18
        self.period = period # 1 a 7
        self.atomic_radius = atomic_radius # em pm
        self.color = color
        self.description = description

    def draw_element(self, screen, x, y):
        font = pygame.font.Font("assets/font/Roboto_Slab/static/RobotoSlab-Regular.ttf", self.atomic_radius//2)
        surface = font.render(self.symbol, True, BLACK)
        pygame.draw.circle(screen, self.color, (x,y), self.atomic_radius)
        rect_text = surface.get_rect(center=(x,y))
        screen.blit(surface, rect_text)
        

class Isotope(Element):
    def __init__(self, name, symbol, atomic_number, group, period, description, mass_number, mass, is_radioactive, abundance, name_isotope):
        super().__init__(self, name, symbol, atomic_number, group, period, description)
        self.mass_number = mass_number
        self.mass = mass # em U
        self.is_radioactive = is_radioactive
        self.abundance = abundance # em %
        self.name_isotope = name_isotope if name_isotope else f"{name}-{mass_number}"
        self.neutrons = mass_number - atomic_number
        
    def __str__(self):
        # get card
        pass


class FundamentalParticle:
    pass

