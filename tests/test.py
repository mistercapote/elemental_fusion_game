import pygame
import unittest
import src.models.achievement as achievement
from models.fusion import *


class TestFamilyList(unittest.TestCase):
    def test_tipo_retorno_familylist(self):
        resultado = achievement.Achievement().family_list()

        # Verifica se o retorno é uma tupla
        self.assertIsInstance(resultado, tuple)

        # Verifica se o primeiro elemento é do tipo `str`
        self.assertIsInstance(resultado[0], (str))

        # Verifica se o segundo elemento é uma lista
        self.assertIsInstance(resultado[1], list)

        # Verifica se todos os itens da lista são strings
        for item in resultado[1]:
            self.assertIsInstance(item, str)


class TestElement(unittest.TestCase):
    def test_tipo_retorno_element(self):
          # Definir os dados do exemplo
        dados = {
            "name": "Hidrogênio",
            "symbol": "H",
            "atomic_number": 1,
            "group": 1,
            "period": 1,
            "atomic_radius": 25,
            "color": "White",
            "description": "Colourless, odourless gaseous chemical element. Lightest and most abundant element in the universe. Present in water and in all organic compounds. Chemically reacts with most elements. Discovered by Henry Cavendish in 1776."
        }
        
        # Chamar o método from_dict da classe Element
        resultado = Element.from_dict(dados)
        
        # Verificar se o retorno é uma instância da classe Element
        self.assertIsInstance(resultado, Element)


class TestFundamentalParticle(unittest.TestCase):
    def test_tipo_retorno_fundamentalparticle(self):
          # Definir os dados do exemplo
        dados = {
            "name": "Proton",
            "symbol": "p",
            "mass": 1.00727647,
            "charge": 1, 
            "spin": 0.5,
            "color": "Red"
        }

        # Chamar o método from_dict da classe FundamentalParticle
        resultado = fusion.FundamentalParticle.from_dict(dados)
        
        # Verificar se o retorno é uma instância da classe Element
        self.assertIsInstance(resultado, fusion.FundamentalParticle)

class TestGetEnergy(unittest.TestCase):
    def test_get_energy(self):
        # Mock dos objetos necessários
        product1 = Isotope(mass=2.0)
        product2 = Isotope(mass=1.0)

        # Definir valores de massa
        element_a.mass = 4.0
        element_b.mass = 3.0

        # Lista de produtos
        product = [product1, product2]

        # Criar a instância da classe Reaction
        reaction = Fusion("", element_a, element_b, product, "")

        # Calcular a energia esperada
        U_TO_KG = 1.66053906660e-27
        J_TO_MEV = 6.242e12
        C_2 = (2.99792458e8)**2
        m_initial = element_a.mass + element_b.mass
        m_final = sum([product1.mass, product2.mass])
        expected_energy = round((m_initial - m_final) * U_TO_KG * C_2 * J_TO_MEV, 4)

        # Executar a função
        result = reaction.get_energy()

        # Verificar se o resultado é o esperado
        self.assertEqual(result, expected_energy)