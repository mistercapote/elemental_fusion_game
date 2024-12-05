import unittest
from src.models.fusion import *


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


# Todos os nomes de elementos estão como Hidrogênio pois é um elemento fictício, no qual só importa a massa para os cálculos
class TestGetEnergy(unittest.TestCase):
    def test_get_energy_positive(self):
        # Criando objetos necessários
        element_a = Isotope("Hidrogênio", "H", 1, 1, 1, 25.0, [255,255,255], "Gasoso", 1, 4, False, 99.9,"null") 
        element_b = Isotope("Hidrogênio", "H", 1, 1, 1, 25.0, [255,255,255], "Gasoso", 1, 3, False, 99.9,"null") 
        product1 = Isotope("Hidrogênio", "H", 1, 1, 1, 25.0, [255,255,255], "Gasoso", 1, 2, False, 99.9,"null") 
        product2 = Isotope("Hidrogênio", "H", 1, 1, 1, 25.0, [255,255,255], "Gasoso", 1, 1.5, False, 99.9,"null") 
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
        element_a = Isotope("Hidrogênio", "H", 1, 1, 1, 25.0, [255,255,255], "Gasoso", 1, 0, False, 99.9,"null") 
        element_b = Isotope("Hidrogênio", "H", 1, 1, 1, 25.0, [255,255,255], "Gasoso", 1, 3, False, 99.9,"null") 
        product1 = Isotope("Hidrogênio", "H", 1, 1, 1, 25.0, [255,255,255], "Gasoso", 1, 2, False, 99.9,"null") 
        product2 = Isotope("Hidrogênio", "H", 1, 1, 1, 25.0, [255,255,255], "Gasoso", 1, 1.5, False, 99.9,"null") 
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
        element_a = Isotope("Hidrogênio", "H", 1, 1, 1, 25.0, [255,255,255], "Gasoso", 1, 0.5, False, 99.9,"null") 
        element_b = Isotope("Hidrogênio", "H", 1, 1, 1, 25.0, [255,255,255], "Gasoso", 1, 2.5, False, 99.9,"null") 
        product1 = Isotope("Hidrogênio", "H", 1, 1, 1, 25.0, [255,255,255], "Gasoso", 1, 2.0, False, 99.9,"null") 
        product2 = Isotope("Hidrogênio", "H", 1, 1, 1, 25.0, [255,255,255], "Gasoso", 1, 1.0, False, 99.9,"null") 
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

