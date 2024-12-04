#Constant
from models.fusion import Fusion, Element, Isotope, FundamentalParticle
from models.achievement import Achievement
import pygame
import json

pygame.init()

#Funcoes
def write(screen, text, font, color, center):
    render = font.render(text, True, color)
    rect = render.get_rect(center=center)
    screen.blit(render, rect)

def from_json(class_, filepath, *args):
    with open(filepath, "r", encoding="utf-8") as f: dict_data = json.load(f)
    return [class_.from_dict(data, *args) for data in dict_data]

#Tamanhos
WIDTH_MAX = 1280
HEIGHT_MAX = 720
CENTER_X = WIDTH_MAX // 2
CENTER_Y = HEIGHT_MAX // 2
SQUARE_WIDTH = WIDTH_MAX // 20
SQUARE_HEIGHT = HEIGHT_MAX // 12
ACHIE_WIDTH = WIDTH_MAX // 5
ACHIE_HEIGHT = HEIGHT_MAX // 3.5

#Cores
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

#Fontes
FONT_GIGANT = pygame.font.Font("assets/font/Bungee_Inline/BungeeInline-Regular.ttf", 90)
FONT_BUTTON_HOVER = pygame.font.Font("assets/font/Bungee_Inline/BungeeInline-Regular.ttf", 50)
FONT_BUTTON = pygame.font.Font("assets/font/Bungee_Inline/BungeeInline-Regular.ttf", 40)
FONT_STORY = pygame.font.Font("assets/font/Bungee_Inline/BungeeInline-Regular.ttf", 35)
FONT_LARGE = pygame.font.Font("assets/font/Roboto_Slab/static/RobotoSlab-Regular.ttf", 20)
FONT_SMALL= pygame.font.Font("assets/font/Roboto_Slab/static/RobotoSlab-Regular.ttf", 12)

#Dados
PARTICLES = from_json(FundamentalParticle, "data/json/fundamental_particles.json")
ELEMENTS = from_json(Element, "data/json/element.json")
ISOTOPES = from_json(Isotope, "data/json/isotope.json", ELEMENTS)
FUSIONS = from_json(Fusion, "data/json/fusion.json", PARTICLES, ISOTOPES)
ACHIEVEMENTS = from_json(Achievement, "data/json/achievement.json")

SUPERNOVA = [Ni-56, Fe-54, Fe-56, Co-56, Ag-107, Ag-109, Au-197, Pt-195, Pt-196, Pt-198, U-235, U-238, Th-232, Pu-239, Pu-244, Sr-88, Sr-89, Y-89, Tc-99, Ba-137, Ba-138, Ce-140, Ce-142, Nd-144, Nd-146, I-129, Rh-103, Rh-105, Ru-106, Sm-150, Sm-152, Eu-151, Eu-153, Gd-155, Gd-157, Ni-57, Co-57, Fe-57, Ni-58, Co-59, Fe-58, Fe-60, Zn-64, Zn-66, Zn-68, Ge-70, Ge-72, Al-26, Ca-41, Sc-46, La-139, La-140, Ac-227, Pa-231, Rh-102, Ag-108, Cd-113, Te-130, Xe-136, Cm-247, Cf-249, Sb-123, Sb-125, Hf-182, Os-187]

