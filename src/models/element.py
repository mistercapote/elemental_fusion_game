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
        self.name_isotope = name_isotope if name_isotope else f"{symbol}-{mass_number}"
        self.neutrons = mass_number - atomic_number
        
    def __eq__(self, other):
        if not isinstance(other, Isotope): return False
        return self.atomic_number == other.atomic_number and self.mass_number == other.mass_number
    
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
            name_isotope = data["name_isotope"] if data["name_isotope"] else f"{element.symbol}-{data['mass_number']}"
        )
            
class FundamentalParticle:
    def __init__(self, name, symbol, mass, charge, spin, color):
        self.name = name
        self.symbol = symbol
        self.mass = mass
        self.charge = charge
        self.spin = spin
        self.color = color
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            name = data["name"],
            symbol = data["symbol"],
            mass = data["mass"],
            charge = data["charge"],
            spin = data["spin"],
            color = data["color"],
        )

    @staticmethod
    def load_elements_from_json(filepath):
        with open(filepath, "r") as f:
            particles_data = json.load(f)
        return [FundamentalParticle.from_dict(data) for data in particles_data]