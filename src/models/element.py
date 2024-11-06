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
    def __init__(self, name, symbol, atomic_number, group, period, atomic_radius, color, description, mass_number, mass, is_radioactive, abundance, name_isotope):
        super().__init__(name, symbol, atomic_number, group, period, atomic_radius, color, description)
        self.mass_number = mass_number
        self.mass = mass # em U
        self.is_radioactive = is_radioactive
        self.abundance = abundance # em %
        self.name_isotope = name_isotope if name_isotope else f"{name}-{mass_number}"
        self.neutrons = mass_number - atomic_number
        
    def __str__(self):
        # get card
        pass

    def draw_ball(self, screen, x, y, raio=25):
        font_large = pygame.font.Font("assets/font/Roboto_Slab/static/RobotoSlab-Regular.ttf", 20)
        font_small= pygame.font.Font("assets/font/Roboto_Slab/static/RobotoSlab-Regular.ttf", 12)
        pygame.draw.circle(screen, self.color, (x,y), raio)
        mass_number_text = font_small.render(f"{self.mass_number}", True, (0,0,0))
        symbol_text = font_large.render(self.symbol, True, (0,0,0))


        rect_mass_number_text = mass_number_text.get_rect(center=(x-1*raio//2,y-raio//3))
        rect_symbol_text = symbol_text.get_rect(center=(x,y))

        screen.blit(mass_number_text, rect_mass_number_text)
        screen.blit(symbol_text, rect_symbol_text)

        return
    
    @staticmethod
    def load_elements_from_json_2(ELEMENTS, isotope_path):
        with open(isotope_path, "r") as f:
            isotope_data = json.load(f)

        lista = []
        for isotope in isotope_data:
            element = list(filter(lambda x: x.atomic_number == isotope["atomic_number"], ELEMENTS))[0]
            lista.append(Isotope.from_dict_2(isotope, element))
        
        return lista

    @classmethod
    def from_dict_2(cls, data, element):
        """Cria uma instância da classe a partir de um dicionário."""
        return cls(
            name=element.name,
            symbol=element.symbol,
            atomic_number=element.atomic_number,
            group=element.group,
            period=element.period,
            atomic_radius=element.atomic_radius,
            color=element.color,
            description=element.description,
            mass_number = data["mass_number"],
            mass = data["mass"], # em U
            is_radioactive = data["is_radioactive"],
            abundance = data["abundance"], # em %
            name_isotope = data["name_isotope"] if data["name_isotope"] else f"{element.name}-{data['mass_number']}"
        )
            


class FundamentalParticle:
    pass

