#Constant
from models.element import Element, Isotope, FundamentalParticle
from models.fusion import Fusion
import pygame
pygame.init()

#Funcoes
def write(screen, text, font, color, center):
    render = font.render(text, True, color)
    rect = render.get_rect(center=center)
    screen.blit(render, rect)

#Tamanhos
WIDTH_MAX = 1280
HEIGHT_MAX = 720
CENTER_X = WIDTH_MAX // 2
CENTER_Y = HEIGHT_MAX // 2
SQUARE_WIDTH = WIDTH_MAX // 20
SQUARE_HEIGHT = HEIGHT_MAX // 12

#Cores
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

#Fontes
FONT_GIGANT = pygame.font.Font("assets/font/Bungee_Inline/BungeeInline-Regular.ttf", 90)
FONT_BUTTON_HOVER = pygame.font.Font("assets/font/Bungee_Inline/BungeeInline-Regular.ttf", 50)
FONT_BUTTON = pygame.font.Font("assets/font/Bungee_Inline/BungeeInline-Regular.ttf", 40)
FONT_STORY = pygame.font.Font("assets/font/Bungee_Inline/BungeeInline-Regular.ttf", 35)
FONT_LARGE = pygame.font.Font("assets/font/Roboto_Slab/static/RobotoSlab-Regular.ttf", 20)
FONT_SMALL= pygame.font.Font("assets/font/Roboto_Slab/static/RobotoSlab-Regular.ttf", 12)

#Dados
PARTICLES = FundamentalParticle.load_elements_from_json("data/json/fundamental_particles.json")
ELEMENTS = Element.load_elements_from_json("data/json/element.json")
ISOTOPES = Isotope.load_elements_from_json_2(ELEMENTS, "data/json/isotope.json")
FUSIONS = Fusion.load_elements_from_json(ISOTOPES, PARTICLES, "data/json/fusion.json")
