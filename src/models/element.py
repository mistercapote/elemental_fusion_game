import pygame
from constants import *
import json
import random

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


    def __str__(self):
        return f"{self.symbol}"

    def draw_ball(self, screen, x, y, raio=25):
        font = pygame.font.Font("assets/font/Roboto_Slab/static/RobotoSlab-Regular.ttf", 20)
        surface = font.render(self.symbol, True, (0,0,0))
        pygame.draw.circle(screen, self.color, (x,y), raio)
        rect_text = surface.get_rect(center=(x,y))
        screen.blit(surface, rect_text)
        return rect_text


    def draw_card(self, screen, x, y, coef=1):
        WIDTH_MAX = 1280
        HEIGHT_MAX = 720
        SQUARE_WIDTH = WIDTH_MAX // 20
        SQUARE_HEIGHT = HEIGHT_MAX // 12
        font = pygame.font.Font("assets/font/Roboto_Slab/static/RobotoSlab-Regular.ttf", 20)
        surface = font.render(self.symbol, True, (0,0,0))
        #desenhar forma card
        pygame.draw.polygon(screen, self.color, [(x+coef,y+coef), (x+SQUARE_WIDTH-coef, y+coef), (x+SQUARE_WIDTH-coef, y+SQUARE_HEIGHT-coef), (x+coef, y+SQUARE_HEIGHT-coef)])
        rect_text = surface.get_rect(center=(x+SQUARE_WIDTH//2,y+SQUARE_HEIGHT//2))
        screen.blit(surface, rect_text)
        return rect_text

    @classmethod
    def from_dict(cls, data):
        """Cria uma instância da classe a partir de um dicionário."""
        return cls(
            name = data["name"],
            symbol = data["symbol"],
            atomic_number = data["atomic_number"],
            group = data["group"], # 1 a 18
            period = data["period"], # 1 a 7
            atomic_radius = data["atomic_radius"], # em pm
            color = data["color"],
            description = data["description"]
        )

    @staticmethod
    def load_elements_from_json(filepath):
        """Carrega dados de elementos a partir de um arquivo JSON e cria objetos Element."""
        with open(filepath, "r") as f:
            elements_data = json.load(f)
        return [Element.from_dict(data) for data in elements_data]

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

