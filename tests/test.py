import pygame
import unittest
import src.models.achievement as achievement
from models.fusion import *
import constants


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
        resultado = FundamentalParticle.from_dict(dados)
        
        # Verificar se o retorno é uma instância da classe Element
        self.assertIsInstance(resultado, FundamentalParticle)


class TestGetEnergy(unittest.TestCase):
    def test_get_energy_positive(self):
        # Criando objetos necessários
        element_a = Isotope(mass=4.0) 
        element_b = Isotope(mass=3.0) 
        product1 = Isotope(mass=2.0)  
        product2 = Isotope(mass=1.5)  
        product = [product1, product2]

        # Instância da classe Fusion
        fusion = Fusion(
            process="Fusão de Teste",
            element_a=element_a,
            element_b=element_b,
            product=product,
            description="Descrição para fusão de teste."
        )

        # Valor esperado
        expected_energy = 3260.4858

        # Obter o resultado da função
        result = fusion.get_energy()

        # Verificar se o resultado corresponde ao esperado
        self.assertEqual(result, expected_energy)


    def test_get_energy_negative(self):
        # Criando objetos necessários
        element_a = Isotope(mass=0) 
        element_b = Isotope(mass=3.0) 
        product1 = Isotope(mass=2.0)  
        product2 = Isotope(mass=1.5)  
        product = [product1, product2]

        # Instância da classe Fusion
        fusion = Fusion(
            process="Fusão de Teste",
            element_a=element_a,
            element_b=element_b,
            product=product,
            description="Descrição para fusão de teste."
        )

        # Valor esperado
        expected_energy = -465.7837

        # Obter o resultado da função
        result = fusion.get_energy()

        # Verificar se o resultado corresponde ao esperado
        self.assertEqual(result, expected_energy)


    def test_get_energy_equal_zero(self):
        # Criando objetos necessários
        element_a = Isotope(mass=0.5) 
        element_b = Isotope(mass=2.5) 
        product1 = Isotope(mass=2.0)  
        product2 = Isotope(mass=1.0)  
        product = [product1, product2]

        # Instância da classe Fusion
        fusion = Fusion(
            process="Fusão de Teste",
            element_a=element_a,
            element_b=element_b,
            product=product,
            description="Descrição para fusão de teste."
        )

        # Obter o resultado da função
        result = fusion.get_energy()

        # Verificar se o resultado corresponde ao esperado
        self.assertEqual(result, 0)


class TestFromJson(unittest.TestCase):

    def test_from_json(self):
        # Criar um arquivo JSON de exemplo
        test_data = [{
        "name": "Hidrogênio",
        "symbol": "H",
        "atomic_number": 1,
        "group": 1,
        "period": 1,
        "atomic_radius": 25.0,
        "color": [
            255,
            255,
            255
        ],
        "description": "Elemento químico gasoso, incolor e inodoro. É o elemento mais leve e abundante do universo. Presente na água e em todos os compostos orgânicos. Reage quimicamente com a maioria dos elementos. Descoberto por Henry Cavendish em 1776."
    },
    {
        "name": "Hélio",
        "symbol": "He",
        "atomic_number": 2,
        "group": 18,
        "period": 1,
        "atomic_radius": 120.0,
        "color": [
            123,
            100,
            204
        ],
        "description": "Elemento gasoso incolor e inodoro, não metálico. Pertence ao grupo 18 da tabela periódica. Possui o ponto de ebulição mais baixo de todos os elementos e só pode ser solidificado sob pressão. Quimicamente inerte, sem compostos conhecidos. Descoberto no espectro solar em 1868 por Lockyer."
    }]
        
        with open('test_data.json', 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False)

        result = constants.from_json(Element, 'test_data.json')

        # Verifica se o retorno é uma lista
        self.assertIsInstance(result, list)

        # Verifica se todos os itens da lista são instâncias de Element
        for item in result:
            self.assertIsInstance(item, Fusion)

        # Limpeza: Deleta o arquivo de teste após o teste
        import os
        os.remove('test_data.json')